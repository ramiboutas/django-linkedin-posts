# Generated by Django 4.2.7 on 2023-11-28 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "django_linkedin_posts",
            "0008_remove_poll_response_code_remove_poll_response_text_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="postimage",
            old_name="file",
            new_name="image",
        ),
        migrations.RemoveField(
            model_name="postcomment",
            name="image",
        ),
        migrations.AddField(
            model_name="postcomment",
            name="imageobj",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="django_linkedin_posts.postimage",
            ),
        ),
    ]
