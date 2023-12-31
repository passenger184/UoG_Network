# Generated by Django 3.2.9 on 2023-01-14 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uog', '0004_followerscount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('msg_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to='uog.profile')),
                ('msg_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to='uog.profile')),
            ],
        ),
    ]
