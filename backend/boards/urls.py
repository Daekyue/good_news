from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet
from .views_chatbot import ChatbotAPIView

router = DefaultRouter()
router.register(r'news', NewsArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
]
