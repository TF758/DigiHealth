# Generated by Django 4.2.6 on 2023-11-12 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('district', models.CharField(choices=[('ALR', 'Anse La Raye'), ('CAN', 'Canaries'), ('CAS', 'Castries'), ('CHO', 'Choiseul'), ('DEN', 'Dennery'), ('GI', 'Gros Islet'), ('LAB', 'Laborie'), ('MIC', 'Micoud'), ('SOU', 'Soufirere'), ('VF', 'Vieux Fort')], max_length=150, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=255, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=150, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='healthapp.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
