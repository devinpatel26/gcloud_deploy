# Generated by Django 5.1.3 on 2024-12-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
