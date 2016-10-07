from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

    fieldsets = (
        ('Information', {
            'fields': ('author', 'title', 'created', 'publication_date', 'tags')
        }),
        ('Content', {
            'classes': ('collapse', ),
            'fields': ('short', 'text')
        })
    )

    list_display = ('author', 'title', 'tags')
    search_fields = ('author', 'title', 'tags')
    ordering = ('author', 'created')

admin.site.register(Article, ArticleAdmin)
