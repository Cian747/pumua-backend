from django.contrib import admin
from .models import WellbeingProfile, KnowledgeQuestion, KnowledgeAttempt

admin.site.register(WellbeingProfile)
admin.site.register(KnowledgeQuestion)
admin.site.register(KnowledgeAttempt)