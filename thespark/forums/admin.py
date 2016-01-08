from django.contrib import admin

# Register your models here.

from .models import Forum, ForumMember, ForumMessage

admin.site.register(Forum)
admin.site.register(ForumMember)
admin.site.register(ForumMessage)
