# Generated by Django 4.2.6 on 2023-12-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0027_alter_article_tags_alter_center_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='subtitle',
            field=models.CharField(default='this is dummy text', max_length=200),
        ),
    ]