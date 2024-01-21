# Generated by Django 4.2.6 on 2024-01-21 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0040_alter_openingtimes_weekday'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openingtimes',
            options={'ordering': ['weekday'], 'verbose_name': 'Opening Time', 'verbose_name_plural': 'Opening Times'},
        ),
        migrations.DeleteModel(
            name='OpeningHours',
        ),
    ]
