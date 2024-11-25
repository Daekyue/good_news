import json
import openai
from openai import OpenAI
import pandas as pd
import os


from transformers import pipeline


os.environ["OPENAI_API_KEY"] = "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"

# BERT NER 파이프라인 로드
nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")



# 예시 텍스트
text = """
Lady Gaga has been born a star but now, she’s transforming into DC comic book character Harley Quinn for “Joker: Folie à Deux.”The Oscar and Grammy winner teased her upcoming role alongside fellow Academy Award winner Joaquin Phoenix in the sequel to 2019 Batman prequel “Joker.” As Phoenix reprises his titular role as Arthur Fleck AKA the Joker, Gaga will play Harley from the “Batman the Animated Series” origins, as a bit different from Margot Robbie’s version of the character.“You know my version of Harley is mine and it’s very authentic to this movie and these characters,” Gaga told Access Hollywood. “I’ve never done anything like I’ve done in this movie before, so it’s all going to be completely brand new and really fun.”Margot Robbie brought Harley to life first in “Suicide Squad,” followed by spinoff “Birds of Prey” and quasi-reboot “The Suicide Squad.” However, Harley’s origin story of being the psychiatrist who treats the Joker in Arkham Asylum was only hinted at in a deleted montage scene from Robbie’s “Suicide Squad” version, with Jared Leto as the Joker.Robbie previously praised Gaga’s casting as Harley, telling MTV News in 2022 that hopefully more iterations of Harley are brought to the big screen.“It makes me so happy because I said from the very beginning that all I want is for Harley Quinn to be one of those characters — the way Macbeth or Batman, always gets passed from great actor to great actor,” Robbie said. “Someone gets to do their Batman, or someone gets to do their Macbeth. It’s such an honor to have built a foundation strong enough that Harley can now be one of those characters that other actors get to have a go at playing. And I think [Gaga] will do something incredible with it.”“Joker: Folie à Deux” is directed by Todd Phillips. The film will have musical elements á la Francis Ford Coppola’s “One From the Heart,” and centers around Arkham Asylum and its inhabitants. Zazie Beetz, “Banshees of Inisherin” Oscar nominee Brendan Gleeson, Catherine Keener, Jacob Lofland, and “Industry” breakout Harry Lawtey appear in the film, which will be released October 4 in theaters.
"""


def keywords_extract(text):

    # NER 실행
    entities = nlp(text)

    # 스코어 기준으로 정렬
    sorted_entities = sorted(entities, key=lambda x: x['score'], reverse=True)
    ent = pd.DataFrame(sorted_entities)

    # 공백이 있는 단어만 추출
    ent_df = ent[ent['word'].str.contains(' ')]

    # 따옴표 제거
    ent_df['word'] = ent_df['word'].str.replace(r"‘ |“ | ”| ’ | ‘| “|” |’ ", "", regex=True)

    # 중복 제거
    ent_df = ent_df.drop_duplicates(subset=['word'])

    return ent_df.iloc[0:5,]['word']




def preprocess_content(content):
    """
    데이터 전처리 - 텍스트 길이 제한
    토큰 수를 제한하여 처리 효율성 확보
    """
    import tiktoken
    
    if not content:
        return ""
        
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    
    if len(tokens) > 5000:
        truncated_tokens = tokens[:5000]
        return encoding.decode(truncated_tokens)
    
    return content



def transform_extract_keywords(text):
    """
    (이 부분 자체 모델 학습 시켜 대체 가능)
    텍스트 데이터 변환 - 키워드 추출
    입력 텍스트에서 핵심 키워드를 추출하는 변환 로직
    """
    text = preprocess_content(text)

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 텍스트에서 주요 키워드를 추출하는 전문가입니다. 다음 텍스트에서 가장 중요한 5개의 키워드를 추출해주세요. 키워드는 쉼표로 구분하여 반환해주세요"},
            {"role": "user", "content": text}
        ],
        max_tokens=100
    )
    keywords = response.choices[0].message.content.strip()
    return keywords.split(',')



print(keywords_extract(text))
print(transform_extract_keywords(text))