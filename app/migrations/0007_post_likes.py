# Generated by Django 4.2.6 on 2023-11-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
