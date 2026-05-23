from django.contrib import admin
from .models import Study, StudyMember, StudySchedule

admin.site.register(Study)
admin.site.register(StudyMember)
admin.site.register(StudySchedule)