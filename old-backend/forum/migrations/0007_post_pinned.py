# Generated by Django 4.2.16 on 2024-11-16 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0006_post_latitude_post_longitude"),
    ]

    operations = [
        migrations.AddField(
            model_name="post", name="pinned", field=models.BooleanField(default=False),
        ),
    ]