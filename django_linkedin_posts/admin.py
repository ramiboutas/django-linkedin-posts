from django.contrib import admin

# Register your models here.


from .models import Post
from .models import PostShare


# TODO: make it better
admin.site.register(Post)
admin.site.register(PostShare)
