# Generated by Django 4.0.4 on 2022-12-09 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0028_alter_skillstudent_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='static/default-images/default-staff-female.png', upload_to='static/admissionsystem/user-images'),
        ),
    ]
