# Generated by Django 4.0.4 on 2023-03-28 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_teleuser_msg_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teleuserlog',
            name='reason',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
