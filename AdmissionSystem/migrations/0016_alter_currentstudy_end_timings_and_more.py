# Generated by Django 4.0.4 on 2022-12-02 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0015_alter_currentstudy_cgpa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstudy',
            name='end_timings',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='currentstudy',
            name='start_timings',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
