# Generated by Django 3.2.9 on 2023-01-18 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uog', '0006_post_profie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='profie',
            new_name='profile',
        ),
    ]
