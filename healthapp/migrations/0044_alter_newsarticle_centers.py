# Generated by Django 4.2.6 on 2024-02-23 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0043_alter_newsarticle_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='centers',
            field=models.ManyToManyField(blank=True, null=True, to='healthapp.center'),
        ),
    ]
