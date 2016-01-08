from django.contrib import admin

# Register your models here.

from .models import Conversation, ChatMessage

admin.site.register(Conversation)
admin.site.register(ChatMessage)
