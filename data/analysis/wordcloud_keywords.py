import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta


# JSON 파일에서 데이터 로드``
with open('indiewire_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# 키워드 추출
all_keywords = []
for article in data:

    today = datetime.today()
    min_date = today - timedelta(days=7)
    date = datetime.strptime(article['date'], "%Y-%m-%d")

    if min_date <= date <= today:
        all_keywords += article['keywords'].split(', ')


# 키워드 빈도 계산
keyword_freq = Counter(all_keywords)


# 워드클라우드 생성
wordcloud = WordCloud(
    width=2000, 
    height=1000, 
    background_color='white'
).generate_from_frequencies(keyword_freq)


# 워드클라우드 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
