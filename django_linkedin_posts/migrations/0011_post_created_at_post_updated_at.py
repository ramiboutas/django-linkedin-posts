# Generated by Django 4.2.7 on 2023-11-30 19:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("django_linkedin_posts", "0010_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created_at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="updated_at"),
        ),
    ]
