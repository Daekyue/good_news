from django.db import models

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('NEWS', '뉴스'),
        ('FEATURE', '기획'),
        ('REVIEW', '리뷰'),
        ('INTERVIEW', '인터뷰'),
        ('COLUMN', '칼럼'),
        ('CRITIC', '평론'),
        ('FESTIVAL', '영화제'),
    ]

    title = models.CharField(max_length=255)  # 기사 제목
    content = models.TextField()  # 기사 내용
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 분류
    date = models.DateField()  # 작성 날짜
    keywords = models.TextField(blank=True, null=True)  # 키워드, 추후 저장

    def __str__(self):
        return self.title
