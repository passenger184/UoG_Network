# Generated by Django 3.2.9 on 2023-01-08 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uog', '0003_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
