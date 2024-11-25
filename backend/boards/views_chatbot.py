from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .document_store import ChatbotDocumentStore  # pgvector를 사용한 챗봇 문서 저장소
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("user_input")
        if not user_input:
            return Response({"error": "No user input provided"}, status=400)

        # ChatbotDocumentStore 인스턴스 생성
        doc_store = ChatbotDocumentStore()

        # 유사도 검색 수행 (사용자 입력을 기준으로 유사한 문서 검색)
        relevant_docs = doc_store.similarity_search(user_input, k=3)

        # 관련 문서의 내용을 합쳐서 컨텍스트 생성
        context = "\n\n".join([doc['content'] for doc in relevant_docs])

        # 시스템 메시지 설정
        system_prompt = """당신은 유용하고 전문적인 AI 어시스턴트입니다. 제공된 문서 정보를 사용하여 사용자의 질문에 답변하며, 문서 내용 범위를 벗어나지 않도록 하세요. 답변은 한국어로 제공하되, 전문적이면서도 이해하기 쉽게 작성해주세요."""

        # LLM에 전달할 메시지 구성
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"다음 문서 정보를 참고하여 질문에 답변하세요.\n\n{context}\n\n질문: {user_input}")
        ]

        # OpenAI LLM 인스턴스 생성 및 응답 생성
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        response = llm(messages)

        return Response({"answer": response.content})
