from django.contrib import admin
from .models import *


class TitleAdmin(admin.ModelAdmin):
    search_fields = ['title','author']

# Register your models here.
admin.site.register(Title, TitleAdmin)
admin.site.register(Books)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(ID)
admin.site.register(Log)

