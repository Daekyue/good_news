from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .document_store import NewsDocumentStore
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_input = request.data.get("user_input")
        if not user_input:
            return Response({"error": "No user input provided"}, status=400)

        # Initialize NewsDocumentStore instance
        doc_store = NewsDocumentStore()

        # Perform similarity search
        relevant_docs = doc_store.similarity_search(user_input, k=3)

        # Combine relevant document contents
        context = "\n\n".join([doc['content'] for doc in relevant_docs])

        # System prompt setup
        system_prompt = """당신은 유용하고 전문적인 AI 어시스턴트입니다. 제공된 문서 정보를 사용하여 사용자의 질문에 답변하며, 문서 내용 범위를 벗어나지 않도록 하세요. 답변은 한국어로 제공하되, 전문적이면서도 이해하기 쉽게 작성해주세요."""

        # Create messages for LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"다음 문서 정보를 참고하여 질문에 답변하세요.\n\n{context}\n\n질문: {user_input}")
        ]

        llm = ChatOpenAI(model_name="gpt-4-mini", temperature=0.7)
        response = llm(messages)

        return Response({"answer": response.content})
