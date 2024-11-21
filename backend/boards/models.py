from django.db import models
from django.conf import settings  # 추가

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('뉴스', '뉴스'),
        ('기획', '기획'),
        ('리뷰', '리뷰'),
        ('인터뷰', '인터뷰'),
        ('칼럼', '칼럼'),
        ('평론', '평론'),
        ('영화제', '영화제'),
    ]

    title = models.CharField(max_length=255)  # 기사 제목
    content = models.TextField()  # 기사 내용
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 분류
    date = models.DateField()  # 작성 날짜
    keywords = models.TextField(blank=True, null=True)  # 키워드, 추후 저장
    views_count = models.PositiveIntegerField(default=0)  # 조회수
    likes_count = models.PositiveIntegerField(default=0)  # 좋아요 수
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)  # 좋아요 누른 유저

    def __str__(self):
        return self.title
