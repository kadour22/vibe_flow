# Generated by Django 4.2 on 2025-03-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
