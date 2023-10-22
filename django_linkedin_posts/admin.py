from django.contrib import admin

# Register your models here.


from .models import Post
from .models import PostShare


admin.site.register(PostShare)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "comment",
        "post_urn",
        "post_code",
        "image_urn",
        "image_code",
        "url",
    )
    readonly_fields = ("post_urn", "post_code", "image_urn", "image_code")
    list_filter = ("post_code", "image_code")
