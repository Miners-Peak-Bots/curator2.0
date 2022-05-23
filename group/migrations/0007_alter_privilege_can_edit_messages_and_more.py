# Generated by Django 4.0.4 on 2022-05-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_group_privilege_specialgroup_flair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privilege',
            name='can_edit_messages',
            field=models.BooleanField(default=False, help_text='Only for channels'),
        ),
        migrations.AlterField(
            model_name='privilege',
            name='can_post_messages',
            field=models.BooleanField(default=False, help_text='Only for channels'),
        ),
        migrations.AlterField(
            model_name='specialgroup',
            name='flair',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='specialgroup',
            name='link',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='specialgroup',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='specialgroup',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
