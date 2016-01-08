from django.contrib import admin

# Register your models here.

from .models import Event, EventRSVP, EventComment, EventReport, EventTag

admin.site.register(Event)
admin.site.register(EventRSVP)
admin.site.register(EventComment)
admin.site.register(EventReport)
admin.site.register(EventTag)
