# Generated by Django 4.2.2 on 2023-07-24 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]