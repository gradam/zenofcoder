from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', 'comments')

    fieldsets = (
        ('Information', {
            'fields': ('author', 'title', 'timestamp', 'publication_date', 'tags')
        }),
        ('Content', {
            'classes': ('collapse', ),
            'fields': ('content', )
        }),
        ('Comments', {
            'classes': ('collapse', ),
            'fields': ('comments', )
        })
    )

    list_display = ('author', 'title')
    search_fields = ('author', 'title')
    ordering = ('author', '-timestamp')

admin.site.register(Article, ArticleAdmin)
