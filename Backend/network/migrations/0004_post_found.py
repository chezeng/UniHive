# Generated by Django 4.2.16 on 2024-11-15 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0003_remove_post_likes_post_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="post", name="found", field=models.BooleanField(default=False),
        ),
    ]
