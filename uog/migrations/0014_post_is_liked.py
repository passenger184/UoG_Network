# Generated by Django 3.2.9 on 2023-02-05 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uog', '0013_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_liked',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]