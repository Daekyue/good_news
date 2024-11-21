from django.db import models

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
    url = models.TextField()

    def __str__(self):
        return self.title
