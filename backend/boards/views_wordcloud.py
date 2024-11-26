# backend/boards/views_wordcloud.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta
from django.http import FileResponse
import os
from .models import NewsArticle

class WordCloudAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 특정 기간(예: 7일) 내의 키워드를 추출합니다.
        today = datetime.today()
        min_date = today - timedelta(days=7)
        
        articles = NewsArticle.objects.filter(date__range=[min_date, today])
        
        all_keywords = []
        for article in articles:
            all_keywords += article.keywords.split(', ')
        
        # 키워드 빈도 계산
        keyword_freq = Counter(all_keywords)

        # 워드클라우드 생성
        wordcloud = WordCloud(width=1500, height=800, background_color='white').generate_from_frequencies(keyword_freq)
        image_path = "/tmp/wordcloud.png"
         
        # 워드클라우드 이미지 저장
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(image_path)
        plt.close()

        # 이미지 파일을 응답으로 전송
        return FileResponse(open(image_path, 'rb'), content_type='image/png')
