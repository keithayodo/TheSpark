from django.contrib import admin

# Register your models here.

from .models import Forum, Member, ForumMessage

admin.site.register(Forum)
admin.site.register(Member)
admin.site.register(ForumMessage)
