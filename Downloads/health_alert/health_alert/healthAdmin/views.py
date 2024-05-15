from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import AdminUser, Clinic, Disease, Patient, Consultation
from django.db.models import Q
from datetime import datetime, timedelta
import urllib.request
import urllib.parse

# Server IP Address.
serverIP = "192.168.31.106:8000"

# Create your views here.
# -------------------- SMS Code --------------------
def sendSMS(numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': 'CTbMIc8a4Mg-nO0CaKgdBy8BUkLFW6CeA8OkqzdfkB', 'numbers': numbers, 'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

# -------------------- Login Code --------------------
def login(request):
    if 'id' in request.session:
        return redirect('/dashboard/')
    
    if request.method=='POST':
        email = request.POST.get("email","")
        password = request.POST.get("password","")
        
        data = AdminUser.objects.filter(Q(email=email) & Q(password=password))
        if data.count()==1:
            request.session['id'] = email
            request.session['type'] = 'admin'
            return redirect('/clinic/')
        else:
            data = Clinic.objects.filter(Q(email=email) & Q(password=password))
            if data.count()==1:
                request.session['id'] = email
                request.session['type'] = 'clinic'
                return redirect('/patients/')
            else:
                return render(request, "login.html", {"loginError":True,"logoutError":False})
    
    if 'msg' in request.session and request.session['msg'] == "logout":
        logoutError = True
        del request.session['msg']
    else:
        logoutError = False
    return render(request, "login.html", {"loginError":False,"logoutError":logoutError})
            
def logout(request):
    del request.session['id']
    del request.session['type']
    request.session['msg'] = 'logout'
    return redirect('/')

def dashboard(request):
    if 'id' not in request.session or 'type' not in request.session:
        return redirect('/')

    data = AdminUser.objects.raw("SELECT x.id, x.pincode,x.name,MAX(x.count) AS `maxCount`,(SELECT count(*) FROM `healthadmin_patient` WHERE `pincode`=x.pincode) AS `publicCount` FROM (SELECT c.id, d.name,p.pincode, count(p.id) as `count`, sum(p.id) as `sumcount` FROM `healthadmin_patient` p, `healthadmin_disease` d, `healthadmin_consultation` c WHERE c.patient = p.id AND c.disease = d.id AND c.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY p.pincode, d.name) AS x GROUP BY x.pincode")
    startDate = datetime.today() - timedelta(days=30)
    endDate = datetime.today()
    return render(request, "dashboard.html", {"data":data,"startDate":startDate,"endDate":endDate})

def diseaseInfo(request, disease):
    data = Disease.objects.filter(name=disease)
    if data.count()==1:
        return render(request, "dinfo.html", {"data":data})
    else:
        return HttpResponse("<h1>400</h1>Bad Request. Requested data does not exists")

def sendPincodeSMS(request,pincode,disease):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    global serverIP
    data = AdminUser.objects.raw("SELECT `id`,`name`,`mobile` FROM `healthadmin_patient` WHERE `pincode`=" + pincode)
    message = "Aapke area me " + disease + " ki bimari fail rahi hai. Krupiya apne parivaar ka khayal rkhe. Zyada info k liye visit kare http://" + serverIP + "/info/" + disease
    for x in data:
        pass
        # sendSMS(x.mobile, "TXTLCL", message)
    return redirect("/dashboard/")

def sendSMStoAll(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    global serverIP
    data = Patient.objects.raw("SELECT x.id, x.pincode,x.name,MAX(x.count) AS `maxCount` FROM (SELECT c.id, d.name,p.pincode, count(p.id) as `count` FROM `healthadmin_patient` p, `healthadmin_disease` d, `healthadmin_consultation` c WHERE c.patient = p.id AND c.disease = d.id AND c.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY p.pincode, d.name) AS x GROUP BY x.pincode")
    for x in data:
        data2 = Patient.objects.raw("SELECT `id`,`name`,`mobile` FROM `healthadmin_patient` WHERE `pincode`=" + str(x.pincode))
        message = "Aapke area me " + x.name + " ki bimari fail rahi hai. Krupiya apne parivaar ka khayal rkhe. Zyada info k liye visit kare http://" + serverIP + "/info/" + x.name 
        for y in data2:
            pass
            # sendSMS(y.mobile, "TXTLCL", message)
    return redirect("/dashboard/")

def changePassword(request):
    if 'id' not in request.session or 'type' not in request.session:
        return redirect('/')
    
    if request.method=="POST":
        oldPassword = request.POST.get("oldPassword","")
        newPassword = request.POST.get("newPassword","")

        data = AdminUser.objects.filter(Q(email=request.session['id']) & Q(password=oldPassword))
        if data.count()==1:
            for x in data:
                x.password = newPassword
                x.save()
                saveSuccess = "changed"
        else:
            saveSuccess = "incorrect"
    else:
        saveSuccess = False
    return render(request, "change-password.html", {"saveSuccess":saveSuccess})

# -------------------- Clinic Code --------------------
def clinic(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        doctorname = request.POST.get("doctorname","")
        doctorqualification = request.POST.get("doctorqualification","")
        address = request.POST.get("address","")
        zipcode = request.POST.get("zipcode","")
        email = request.POST.get("email","")
        password = request.POST.get("password","")

        Clinic(name = name, doctorname = doctorname, doctorqualification = doctorqualification, address = address, zipcode = zipcode, email = email, password = password).save()
        saveSuccess = True
    else:
        saveSuccess = False
    data = Clinic.objects.all()
    return render(request, "clinic.html", {"saveSuccess":saveSuccess,"data":data})

def editClinic(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        doctorname = request.POST.get("doctorname","")
        doctorqualification = request.POST.get("doctorqualification","")
        address = request.POST.get("address","")
        zipcode = request.POST.get("zipcode","")
        email = request.POST.get("email","")
        password = request.POST.get("password","")

        data = Clinic.objects.get(pk=id)
        data.name = name
        data.doctorname = doctorname
        data.doctorqualification = doctorqualification
        data.address = address
        data.zipcode = zipcode
        data.email = email
        data.password = password
        data.save()
        return redirect('/clinic/')
    
    data = Clinic.objects.filter(pk=id)
    return render(request, "edit-clinic.html", {"data":data})

def deleteClinic(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    data = Clinic.objects.filter(pk=id)
    data.delete()
    return redirect("/clinic/")

# -------------------- Disease Code --------------------
def disease(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        cure = request.POST.get("cure","")
        precautions = request.POST.get("precautions","")
        symptoms = request.POST.get("symptoms","")

        Disease(name = name, cure = cure, precautions = precautions, symptoms = symptoms).save()
        saveSuccess = True
    else:
        saveSuccess = False
    
    data = Disease.objects.all()
    return render(request, "disease.html", {"saveSuccess":saveSuccess,"data":data})

def editDisease(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        cure = request.POST.get("cure","")
        precautions = request.POST.get("precautions","")
        symptoms = request.POST.get("symptoms","")

        data = Disease.objects.get(pk=id)
        data.name = name
        data.cure = cure
        data.precautions = precautions
        data.symptoms = symptoms
        data.save()
        return redirect('/disease/')
    
    data = Disease.objects.filter(pk=id)
    return render(request, "edit-disease.html", {"data":data})

def deleteDisease(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    data = Disease.objects.filter(pk=id)
    data.delete()
    return redirect("/disease/")

# -------------------- Admin Code --------------------
def adminManager(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        password = request.POST.get("password","")

        AdminUser(name = name, email = email, password = password).save()
        saveSuccess = True
    else:
        saveSuccess = False
    
    data = AdminUser.objects.all()
    return render(request, "admin.html", {"saveSuccess":saveSuccess,"data":data})

def editAdminManager(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")

        data = AdminUser.objects.get(pk=id)
        data.name = name
        data.email = email
        data.save()
        return redirect('/adminManager/')
    
    data = AdminUser.objects.filter(pk=id)
    return render(request, "edit-admin.html", {"data":data})

def deleteAdminManager(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='admin':
        return redirect('/')
    
    data = AdminUser.objects.filter(pk=id)
    data.delete()
    return redirect("/adminManager/")

# -------------------- Patients Code --------------------
def patients(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='clinic':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        mobile = request.POST.get("mobile","")
        address = request.POST.get("address","")
        pincode = request.POST.get("pincode","")

        Patient(name = name, mobile=mobile, address = address, pincode = pincode, clinicID = request.session['id']).save()
        saveSuccess = True
    else:
        saveSuccess = False
    
    data = Patient.objects.filter(clinicID = request.session['id'])
    return render(request, "patients.html", {"saveSuccess":saveSuccess,"data":data})

def editPatients(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='clinic':
        return redirect('/')
    
    if request.method=="POST":
        name = request.POST.get("name","")
        mobile = request.POST.get("mobile","")
        address = request.POST.get("address","")
        pincode = request.POST.get("pincode","")

        data = Patient.objects.get(pk=id)
        data.name = name
        data.mobile = mobile
        data.address = address
        data.pincode = pincode
        data.save()
        return redirect('/patients/')
    
    data = Patient.objects.filter(pk=id)
    return render(request, "edit-patients.html", {"data":data})

def deletePatients(request, id):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='clinic':
        return redirect('/')
    
    data = Patients.objects.filter(pk=id)
    data.delete()
    return redirect("/patients/")

# -------------------- Consultation Code --------------------
def consultation(request):
    if 'id' not in request.session or 'type' not in request.session or request.session['type']!='clinic':
        return redirect('/')
    
    if request.method=="POST":
        patient = request.POST.get("patient","")
        disease = request.POST.get("disease","")
        date = request.POST.get("date","")

        Consultation(patient = patient, disease=disease, date=date, clinicID = request.session['id']).save()
        saveSuccess = True
    else:
        saveSuccess = False
    
    data = Consultation.objects.raw("SELECT c.id,p.name as patient,p.mobile,p.pincode,d.name as disease FROM `healthAdmin_consultation` c, `healthAdmin_patient` p, `healthAdmin_disease` d WHERE c.patient = p.id AND c.disease = d.id AND c.clinicID = '" + request.session['id'] + "'")
    patients = Patient.objects.filter(clinicID = request.session['id'])
    diseases = Disease.objects.all()
    return render(request, "consultation.html", {"saveSuccess":saveSuccess,"data":data,"patients":patients,"diseases":diseases})

def editConsultation(request, id):
    if 'id' not in request.session or 'type' not in request.session  or request.session['type']!='clinic':
        return redirect('/')
    
    if request.method=="POST":
        patient = request.POST.get("patient","")
        disease = request.POST.get("disease","")
        date = request.POST.get("date","")
        
        data = Consultation.objects.get(pk=id)
        data.patient = patient
        data.disease = disease
        data.date = date
        data.save()
        return redirect('/consultation/')
    
    data = Consultation.objects.filter(pk=id)
    patients = Patient.objects.all()
    diseases = Disease.objects.all()
    return render(request, "edit-consultation.html", {"data":data,"patients":patients,"diseases":diseases})

def deleteConsultation(request, id):
    if 'id' not in request.session or 'type' not in request.session  or request.session['type']!='clinic':
        return redirect('/')
    
    data = Consultation.objects.filter(pk=id)
    data.delete()
    return redirect("/consultation/")