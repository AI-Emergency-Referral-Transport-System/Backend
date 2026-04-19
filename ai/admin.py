from django.contrib import admin

from ai.models import AIMessage, RAGKnowledge


admin.site.register(AIMessage)
admin.site.register(RAGKnowledge)
