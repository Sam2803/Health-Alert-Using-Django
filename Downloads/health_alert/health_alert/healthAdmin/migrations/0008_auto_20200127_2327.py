# Generated by Django 3.0 on 2020-01-27 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthAdmin', '0007_auto_20200127_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='clinicID',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='patient',
            name='clinicID',
            field=models.CharField(max_length=30),
        ),
    ]
