# Generated by Django 4.2.6 on 2023-11-26 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0013_alter_center_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicevent',
            name='clinic_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='healthapp.clinictype'),
        ),
    ]
