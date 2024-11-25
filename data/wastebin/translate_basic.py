import json
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = "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"

# 영어로 된 제목과 정보
title = ''
article = ''


def translate_to_korean(query_text):
    # OpenAI의 GPT-4 모델을 불러옵니다.
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # 시스템 메시지를 통해 모델의 역할을 지정 
    system_message = SystemMessage(content="당신은 번역가 입니다. 영어를 한국어로 번역해주세요. -입니다. 가 아닌 -다. 라고 끝나는 문장을 사용해야합니다. 제목과 같은 짧은 문장의 경우 -다.가 아닌 명사형으로 끝나야 합니다.")
    
    # 유저의 질문과 검색된 문서를 담은 메시지 생성
    human_message = HumanMessage(content=f"질문: 다음의 문장을 번역해야 합니다. 영화, 감독, 배우, 영화제등의 영화와 관련된 명사는 번역하지 말아주세요. 매끄럽지 않은 부분은 한국어의 문맥에 맞게 수정하고, 문맥에 너무 맞지 않는 부분은 제거해주세요. \n\n{query_text}")
    
    # 대화에 시스템 메시지와 유저 질문 추가
    conversation = [system_message, human_message]
    
    # 모델에게 대화를 전달하여 답변 생성
    response = llm.invoke(conversation)
    
    return response.content  # 생성된 답변 반환



# 제목과 기사 번역
translated_title = translate_to_korean(title)
translated_article = translate_to_korean(article)


# 번역된 결과 출력
print(f"Original Title: {title}")
print(f"Translated Title: {translated_title}")
print(f"Original Article: {article}")
print(f"Translated Article: {translated_article}")


# 파일에 저장
translated_data = {
    "title": translated_title,
    "article": translated_article
}

with open('translated_article.json', 'w', encoding='utf-8') as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=4)

