# Generated by Django 4.0.6 on 2023-03-04 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0041_rename_salary_job_monthly_income_job_employment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstudy',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='phoneno',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
    ]