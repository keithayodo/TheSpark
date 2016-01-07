from django.contrib import admin

# Register your models here.

from .models import (MyAbstractUser, CounsellorUser, SparkUser)

admin.site.register(MyAbstractUser)
admin.site.register(CounsellorUser)
admin.site.register(SparkUser)
