# Generated by Django 4.2.6 on 2023-11-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0010_openinghours_openinghours_center_operating_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=5)),
            ],
        ),
    ]
