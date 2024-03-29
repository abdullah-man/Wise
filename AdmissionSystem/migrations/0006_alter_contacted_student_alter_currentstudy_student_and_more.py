# Generated by Django 4.0.4 on 2022-11-29 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0005_skillstudent_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacted',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='currentstudy',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='job',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='jobposition',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='phoneno',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='shortcoursename',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
        migrations.AlterField(
            model_name='shortcoursestaken',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AdmissionSystem.skillstudent'),
        ),
    ]
