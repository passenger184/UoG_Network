# Generated by Django 3.2.9 on 2023-01-28 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uog', '0011_alter_profile_idcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]