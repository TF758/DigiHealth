# Generated by Django 4.2.6 on 2024-01-09 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0036_newsarticle'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
    ]