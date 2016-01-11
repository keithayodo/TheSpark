from django.contrib import admin

# Register your models here.

from .models import Conversation, ChatMessage, LastConvoMessage

class ChatMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Conversation)
admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(LastConvoMessage)
