# Generated by Django 4.0.6 on 2022-12-28 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0037_courseapplication_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseapplication',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_section_id', to='AdmissionSystem.coursesection'),
        ),
    ]