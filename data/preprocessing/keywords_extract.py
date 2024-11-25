from transformers import pipeline
import pandas as pd
import json



# BERT NER 파이프라인 로드
nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")


def keywords_extract(text):

    # NER 실행
    entities = nlp(text)

    # 스코어 기준으로 정렬
    sorted_entities = sorted(entities, key=lambda x: x['score'], reverse=True)
    ent_df = pd.DataFrame(sorted_entities)


    # 따옴표 제거
    ent_df['word'] = ent_df['word'].str.replace(r"‘ |“ | ”| ’ | ‘| “|” |’ ", "", regex=True)

    # # 제거
    ent_df = ent_df[~ent_df['word'].str.contains('#')]

    # 중복 제거
    ent_df = ent_df.drop_duplicates(subset=['word'])

    # 성 또는 이름만 존재하는 PER 제거
    ent_df = ent_df[~((ent_df['entity_group'] == 'PER') & (~ent_df['word'].str.contains(' ')))]

    # 길이가 1인 문자열 필터링
    ent_df = ent_df[ent_df['word'].str.len() > 1]


    # 공백, 중복 전처리
    words_with_space = ent_df[ent_df['word'].str.contains(' ')]
    words_without_space = ent_df[~ent_df['word'].str.contains(' ')]

    # 공백이 없는 문자열이 공백이 있는 문자열에 포함되는지 확인
    words_to_remove = []
    for word in words_without_space['word']:
        if any(word in full_word for full_word in words_with_space['word']):
            words_to_remove.append(word)

    # words_to_remove 리스트에 포함되지 않은 행만 남김
    ent_df = ent_df[~ent_df['word'].isin(words_to_remove)]


    keywords = []

    filtered_df = ent_df[ent_df['score'] > 0.988]
    if len(filtered_df) > 5:
        if len(filtered_df) > 10:
            keywords = list(filtered_df.head(10)['word'])
        else:  
            keywords = list(filtered_df['word'])
    else:
        keywords = list(ent_df.head()['word'])
    

    print(keywords)

    return keywords


def process_and_translate_json(input_file, output_file):
    # JSON 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for d in data:

        content = d["content"]
        
        keywords = keywords_extract(content)
        
        d['keywords'] = ', '.join(keywords)
    
    # 번역된 데이터를 다시 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 입력 파일과 출력 파일 경로 설정
input_json_path = "indiewire_crawling_1.json"  # 입력 JSON 파일 경로
output_json_path = "keywords_test_1.json"  # 출력 JSON 파일 경로


# JSON 번역 처리 실행
process_and_translate_json(input_json_path, output_json_path)