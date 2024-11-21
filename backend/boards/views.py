from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
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
