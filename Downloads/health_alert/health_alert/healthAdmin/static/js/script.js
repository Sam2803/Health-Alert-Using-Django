$(document).ready(function() {
    $('#datatable').DataTable();

    $("#inputNewPass,#inputConfirmPass").keyup(function(){
        $("button").attr("disabled", true);
        if($("#inputNewPass").val()==$("#inputConfirmPass").val()&&$("#inputNewPass").val()!="")
        {
            $(".confirm-pass").html("<span class='text-success'>Passwords Match</span>");
            $("button").attr("disabled", false);
        }
        else if($("#inputConfirmPass").val()!="") {
            $(".confirm-pass").html("<span class='text-danger'>*Passwords Does not Match</span>");   
        }
        else {
            $(".confirm-pass").html("");   
        }
    });
} );