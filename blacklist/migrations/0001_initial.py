# Generated by Django 4.0.4 on 2022-06-22 15:09

from django.db import migrations, models
import regex_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex', regex_field.fields.RegexField(max_length=128)),
            ],
            options={
                'db_table': 'blacklist',
            },
        ),
    ]
