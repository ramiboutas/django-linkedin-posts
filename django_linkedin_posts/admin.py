from django.contrib import admin

from .models import Post, Poll, PollOption, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("comment", "urn", "response_code", "response_text", "url")
    readonly_fields = ("urn", "response_code", "response_text", "url")
    inlines = (PostImageInline,)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = (PollOptionInline,)
