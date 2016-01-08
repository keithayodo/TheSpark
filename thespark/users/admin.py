from django.contrib import admin

# Register your models here.

from .models import (AllUser, CounsellorUser, SparkUser)

admin.site.register(AllUser)
admin.site.register(CounsellorUser)
admin.site.register(SparkUser)
