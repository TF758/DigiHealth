# Generated by Django 4.2.6 on 2024-01-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0037_delete_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='local_address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]