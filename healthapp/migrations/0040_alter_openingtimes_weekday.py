# Generated by Django 4.2.6 on 2024-01-21 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0039_openingtimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openingtimes',
            name='weekday',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'), (7, 'Holidays')]),
        ),
    ]
