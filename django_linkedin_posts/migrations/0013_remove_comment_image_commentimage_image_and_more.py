# Generated by Django 4.2.7 on 2023-11-28 21:10

from django.db import migrations, models
import django.db.models.deletion
import django_linkedin_posts.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "django_linkedin_posts",
            "0012_comment_commentimage_rename_comment_post_text_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="image",
        ),
        migrations.AddField(
            model_name="commentimage",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=django_linkedin_posts.models.comment_image_path,
            ),
        ),
        migrations.AlterField(
            model_name="commentimage",
            name="comment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="django_linkedin_posts.comment",
            ),
        ),
    ]