# Generated by Django 4.0.4 on 2022-12-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdmissionSystem', '0027_alter_contacted_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillstudent',
            name='created_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='skillstudent',
            name='updated_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
