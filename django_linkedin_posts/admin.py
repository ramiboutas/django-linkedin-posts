from django.contrib import admin

from .models import Post, Poll, PollOption, PostImage, Comment, CommentImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    max_num = 20


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2
    max_num = 4
    min_num = 2


class CommentImageInline(admin.TabularInline):
    model = CommentImage
    extra = 1


@admin.action(description="Share objects")
def share(modeladmin, request, queryset):
    for obj in queryset:
        obj.share()


@admin.action(description="Upload image and comment")
def upload_image_and_share_comment(modeladmin, request, queryset):
    for obj in queryset:
        obj.upload_image_and_share()


@admin.action(description="Upload images and share objects")
def upload_images_and_share(modeladmin, request, queryset):
    for obj in queryset:
        obj.upload_images_and_share()


@admin.action(description="Upload image")
def upload(modeladmin, request, queryset):
    for obj in queryset:
        obj.upload()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = (share, upload_images_and_share)
    list_display = ("text", "urn", "response_code", "response_text")
    readonly_fields = ("urn", "response_code", "response_text")
    inlines = (PostImageInline,)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    actions = (share,)
    list_display = ("question_text", "urn", "response_code", "response_text")
    inlines = (PollOptionInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = (share, upload_image_and_share_comment)
    list_display = ("text", "urn", "response_code", "response_text")
    inlines = (CommentImageInline,)
