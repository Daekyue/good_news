from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import NewsArticle
from movies.models import Movie, Director, Actor
from .serializers import NewsArticleSerializer, MovieSerializer, DirectorSerializer, ActorSerializer
from .document_store import NewsDocumentStore
from datetime import datetime, timedelta  # 여기에 임포트 추가
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

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

        # 1. 사용자가 좋아요한 기사들 가져오기
        user_liked_articles = user.liked_articles.all()

        if not user_liked_articles.exists():
            return Response({
                'movies': [],
                'directors': [],
                'actors': [],
                'message': '좋아요를 누른 기사가 없어 추천을 제공할 수 없습니다.'
            }, status=status.HTTP_200_OK)

        # 2. 그 기사들을 좋아요한 다른 사용자들 (현재 사용자 제외)
        other_users = User.objects.filter(liked_articles__in=user_liked_articles).exclude(id=user.id).distinct()

        if not other_users.exists():
            return Response({
                'movies': [],
                'directors': [],
                'actors': [],
                'message': '유사한 관심사를 가진 사용자가 없습니다.'
            }, status=status.HTTP_200_OK)

        # 3. 다른 사용자들이 좋아요한 기사들 (사용자가 이미 좋아요한 기사 제외)
        other_articles = NewsArticle.objects.filter(liked_users__in=other_users).exclude(id__in=user_liked_articles.values_list('id', flat=True)).distinct()

        if not other_articles.exists():
            return Response({
                'movies': [],
                'directors': [],
                'actors': [],
                'message': '추천할 기사가 없습니다.'
            }, status=status.HTTP_200_OK)

        # 4. 그 기사들의 키워드 수집
        keywords = set()
        for article in other_articles:
            if article.keywords:
                # 키워드가 쉼표로 구분된 문자열이라고 가정
                article_keywords = article.keywords.split(',')
                keywords.update([k.strip() for k in article_keywords])

        if not keywords:
            return Response({
                'movies': [],
                'directors': [],
                'actors': [],
                'message': '추천할 키워드가 없습니다.'
            }, status=status.HTTP_200_OK)

        # 5. 키워드로 영화, 감독, 배우 검색
        # 영화 검색
        movie_query = Q()
        for keyword in keywords:
            movie_query |= Q(title__icontains=keyword) | Q(overview__icontains=keyword)
        recommended_movies = Movie.objects.filter(movie_query).distinct()[:5]  # 최대 5개 추천

        # 감독 검색
        director_query = Q()
        for keyword in keywords:
            director_query |= Q(name__icontains=keyword)
        recommended_directors = Director.objects.filter(director_query).distinct()[:5]

        # 배우 검색
        actor_query = Q()
        for keyword in keywords:
            actor_query |= Q(name__icontains=keyword)
        recommended_actors = Actor.objects.filter(actor_query).distinct()[:5]

        # 6. 데이터 직렬화
        movie_serializer = MovieSerializer(recommended_movies, many=True)
        director_serializer = DirectorSerializer(recommended_directors, many=True)
        actor_serializer = ActorSerializer(recommended_actors, many=True)

        return Response({
            'movies': movie_serializer.data,
            'directors': director_serializer.data,
            'actors': actor_serializer.data,
            'message': '추천 결과를 제공합니다.'
        }, status=status.HTTP_200_OK)