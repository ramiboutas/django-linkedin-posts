# Generated by Django 4.2.4 on 2023-09-07 21:19

from django.db import migrations, models
import django.db.models.deletion
import django_linkedin_posts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "post_urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=django_linkedin_posts.models._get_image_upload_path,
                    ),
                ),
                ("image_title", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "image_urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "image_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code when uploading image",
                    ),
                ),
                (
                    "post_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code when posting",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PostShare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("share", models.BooleanField(default=False)),
                ("upload_image", models.BooleanField(default=False)),
                (
                    "post",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_linkedin_posts.post",
                    ),
                ),
            ],
        ),
    ]
