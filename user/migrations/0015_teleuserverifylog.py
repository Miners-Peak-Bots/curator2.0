# Generated by Django 4.0.4 on 2023-03-28 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_teleuserlog_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeleUserVerifyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=256, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vlogs', to='user.teleuser')),
            ],
        ),
    ]
