from django.urls import path

from ai.views import AIMessageListCreateAPIView


urlpatterns = [
    path("messages/", AIMessageListCreateAPIView.as_view(), name="ai-message-list-create"),
]
