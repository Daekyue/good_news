from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from .document_store import NewsDocumentStore
from datetime import datetime, timedelta  # 여기에 임포트 추가

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-date', '-id')
    serializer_class = NewsArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    # 조회수 증가 액션
    @action(detail=True, methods=['post'])
    def increase_views(self, request, pk=None):
        article = get_object_or_404(NewsArticle, pk=pk)
        article.views_count += 1
        article.save()
        return Response({'views_count': article.views_count}, status=status.HTTP_200_OK)

    # 좋아요 토글 액션
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        article = get_object_or_404(NewsArticle, pk=pk)
        user = request.user

        if user in article.liked_users.all():
            article.liked_users.remove(user)
            article.likes_count -= 1
            liked = False
        else:
            article.liked_users.add(user)
            article.likes_count += 1
            liked = True

        article.save()
        return Response({'likes_count': article.likes_count, 'liked': liked}, status=status.HTTP_200_OK)

    # 유저가 좋아요 누른 기사 리스트 가져오기
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def liked(self, request):
        user = request.user
        liked_articles = user.liked_articles.all()
        serializer = self.get_serializer(liked_articles, many=True)
        return Response(serializer.data)

    # 기사 상세 정보 조회 (retrieve)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 유저가 로그인한 경우 해당 기사에 좋아요를 눌렀는지 여부를 추가
        if request.user.is_authenticated:
            data['liked'] = request.user in instance.liked_users.all()
        else:
            data['liked'] = False

        return Response(data)
        
        # FAISS를 활용한 관련 기사 가져오기
    @action(detail=True, methods=['get'])
    def related_articles(self, request, pk=None):
        # 특정 기사 가져오기
        article = get_object_or_404(NewsArticle, pk=pk)
        
        # NewsDocumentStore 초기화
        doc_store = NewsDocumentStore(index_file="faiss_index.pkl")

        # 기준 기사를 딕셔너리로 변환
        reference_article = {
            'title': article.title,
            'content': article.content,
            'keywords': article.keywords
        }

        # 유사도 검색 수행
        relevant_docs = doc_store.find_similar_articles(reference_article, k=3)

        # 유사한 기사의 정보를 가져오기

        print(relevant_docs)

        related_articles = [
            {
                "title": doc['title'],
            }
            for doc in relevant_docs
        ]

        return Response({"related_articles": related_articles}, status=status.HTTP_200_OK)

    # 일주일간 조회수가 높은 기사 가져오기 (6번 섹션)
    @action(detail=False, methods=['get'])
    def top_articles(self, request):
        one_week_ago = datetime.now() - timedelta(days=7)
        top_articles = NewsArticle.objects.filter(date__gte=one_week_ago).order_by('-views_count')[:5]
        serializer = self.get_serializer(top_articles, many=True)
        return Response(serializer.data)

    # 추천 기사 가져오기 (2, 3, 4번 섹션)
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommend(self, request):
        user = request.user
        liked_articles = user.liked_articles.all()

        if not liked_articles:
            return Response({'message': '좋아요를 누른 기사가 없어 추천을 제공할 수 없습니다.'}, status=status.HTTP_200_OK)

        # NewsDocumentStore 초기화
        doc_store = NewsDocumentStore(index_file="faiss_index.pkl")

        # 사용자가 좋아요를 누른 기사로부터 추천 기사 추출
        recommended_docs = []
        for article in liked_articles:
            reference_article = {
                'title': article.title,
                'content': article.content,
                'keywords': article.keywords
            }
            similar_docs = doc_store.find_similar_articles(reference_article, k=2)
            recommended_docs.extend(similar_docs)

        # 중복 제거 및 사용자가 이미 좋아요 누른 기사 제외
        recommended_article_ids = set(doc['id'] for doc in recommended_docs)
        liked_article_ids = set(liked_articles.values_list('id', flat=True))
        recommended_article_ids -= liked_article_ids

        recommended_articles = NewsArticle.objects.filter(id__in=recommended_article_ids)[:3]
        serializer = self.get_serializer(recommended_articles, many=True)
        return Response(serializer.data)
