import pandas as pd
import json


file_path = "articles.json"

df = pd.read_json(file_path)

print(df.head(

df.columns.lower()

df.rename(columns = {'Title': 'title', 'Content': 'content', 'Category': 'category', 'Date': 'date', 'URL': 'url', 'Keywords': 'keywords'}, inplace=True)

print(df.head())
print(df.info())


df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

df_dict = df.to_dict(orient='records')


print(df.info())

# 딕셔너리를 JSON 파일로 저장
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(df_dict, f, ensure_ascii=False, indent=4)