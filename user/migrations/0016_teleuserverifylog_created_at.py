# Generated by Django 4.0.4 on 2023-03-28 20:47

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_teleuserverifylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='teleuserverifylog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True,
                                       default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
