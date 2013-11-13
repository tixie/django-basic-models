import basic_models


from django.contrib import admin

from test_project.models import *

admin.site.register(Category, admin.ModelAdmin)

class PostAdmin(basic_models.SlugModelAdmin):
    class CommentInline(admin.TabularInline):
        model = Comment
        fields = ('name','slug','body')
        extra = 2
    inlines = [CommentInline]
admin.site.register(Post, PostAdmin)

admin.site.register(Comment, admin.ModelAdmin)
