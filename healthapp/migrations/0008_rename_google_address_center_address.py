# Generated by Django 4.2.6 on 2023-11-20 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0007_alter_article_article_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='center',
            old_name='google_address',
            new_name='address',
        ),
    ]
