# Generated by Django 4.0.4 on 2022-12-02 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0016_alter_currentstudy_end_timings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstudy',
            name='CGPA',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
