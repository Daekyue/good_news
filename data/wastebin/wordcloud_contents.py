import json
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter


# JSON 파일에서 데이터 로드``
with open('indiewire_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 키워드 추출
all_contents = ""
for article in data:

    all_contents += article['content']



# 워드클라우드 생성
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white'
).generate(all_contents)


# 워드클라우드 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
