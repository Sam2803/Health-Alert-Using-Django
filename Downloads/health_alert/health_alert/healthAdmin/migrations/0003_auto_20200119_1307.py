# Generated by Django 3.0 on 2020-01-19 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthAdmin', '0002_clinic_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cure', models.CharField(max_length=200)),
                ('precautions', models.CharField(max_length=200)),
                ('symptoms', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
