# Generated by Django 4.2.7 on 2023-11-28 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "django_linkedin_posts",
            "0009_rename_file_postimage_image_remove_postcomment_image_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="postcomment",
            name="imageobj",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="django_linkedin_posts.postimage",
            ),
        ),
    ]
