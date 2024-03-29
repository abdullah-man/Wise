# Generated by Django 4.0.6 on 2023-03-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0040_alter_job_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='salary',
            new_name='monthly_income',
        ),
        migrations.AddField(
            model_name='job',
            name='employment_type',
            field=models.CharField(blank=True, choices=[('Job', 'Job'), ('Freelancer', 'Freelancer'), ('Own Business', 'Own Business')], max_length=100, null=True),
        ),
    ]
