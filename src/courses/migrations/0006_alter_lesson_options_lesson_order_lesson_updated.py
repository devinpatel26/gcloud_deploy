# Generated by Django 5.1.3 on 2024-11-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_lesson_can_preview_lesson_status_lesson_thumbnail_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order', '-updated']},
        ),
        migrations.AddField(
            model_name='lesson',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
