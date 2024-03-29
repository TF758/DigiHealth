# Generated by Django 4.2.6 on 2023-12-31 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0031_alter_article_article_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='center_description',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='subtitle',
            field=models.CharField(blank=True, default='This is a placeholder subtitle', max_length=200, null=True),
        ),
    ]
