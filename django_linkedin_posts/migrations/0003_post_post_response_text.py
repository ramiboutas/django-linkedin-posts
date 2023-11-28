# Generated by Django 4.2.4 on 2023-10-31 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_linkedin_posts", "0002_alter_post_image_code_alter_post_post_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="post_response_text",
            field=models.TextField(
                blank=True,
                editable=False,
                null=True,
                verbose_name="Share response text",
            ),
        ),
    ]
