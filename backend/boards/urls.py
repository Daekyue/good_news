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

    # 새로운 API 엔드포인트 추가
    path('news/recommendations/', NewsArticleViewSet.as_view({'get': 'recommendations'}), name='recommendations'),
    path('news/top/', NewsArticleViewSet.as_view({'get': 'top'}), name='top_articles'),
]
