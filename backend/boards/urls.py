# backend/boards/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet
from .views_chatbot import ChatbotAPIView
from .views_wordcloud import WordCloudAPIView

router = DefaultRouter()
router.register(r'news', NewsArticleViewSet)

urlpatterns = [
    path('news/wordcloud/', WordCloudAPIView.as_view(), name='wordcloud'),
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
    path('', include(router.urls)),
]
