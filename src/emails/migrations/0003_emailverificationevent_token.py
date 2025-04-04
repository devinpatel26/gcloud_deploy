# Generated by Django 5.1.3 on 2024-12-31 10:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverificationevent',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
