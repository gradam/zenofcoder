from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('content_object', 'content_type', 'object_id', 'parent', 'timestamp')

    fieldsets = (
        ('Information', {
            'fields': ('user', 'content_object', 'parent', 'timestamp')
        }),
        ('content', {
            'classes': ('collapse', ),
            'fields': ('content', )
        })
    )

    list_display = ('content_object', 'user', 'timestamp')
    search_fields = ('content_object', 'user', 'timestamp')
    ordering = ('content_object', 'user', '-timestamp')
