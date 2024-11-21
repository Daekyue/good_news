# movies/management/commands/fetch_movies.py
# TMDB에서 영화 데이터를 가져와 DB에 저장할 때 쓰는 코드

import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from django.conf import settings
import time  # API 호출 간 딜레이를 위해 사용

class Command(BaseCommand):
    help = 'TMDB로부터 영화 데이터를 가져옵니다.'

    def handle(self, *args, **options):
        api_key = 'TMDB_개인_API_KEY'
        base_url = 'https://api.themoviedb.org/3'

        # 1. 장르 데이터 가져오기
        genre_url = f'{base_url}/genre/movie/list?api_key={api_key}&language=ko-KR'
        genre_response = requests.get(genre_url)
        if genre_response.status_code == 200:
            genres = genre_response.json().get('genres', [])
            for genre_data in genres:
                Genre.objects.update_or_create(
                    tmdb_id=genre_data['id'],
                    defaults={'name': genre_data['name']}
                )
            self.stdout.write(self.style.SUCCESS('장르 데이터를 성공적으로 가져왔습니다.'))
        else:
            self.stderr.write(self.style.ERROR('장르 데이터를 가져오는 데 실패했습니다.'))
            return

        # 2. 영화 데이터 가져오기
        start_pages = 27
        total_pages = 5 # 가져올 페이지 수
        for page in range(start_pages, start_pages + total_pages):
            movie_url = f'{base_url}/movie/popular?api_key={api_key}&language=ko-KR&page={page}'
            movie_response = requests.get(movie_url)
            if movie_response.status_code == 200:
                movies = movie_response.json().get('results', [])
                for movie_data in movies:
                    # 영화 데이터 저장 또는 업데이트
                    movie, created = Movie.objects.update_or_create(
                        tmdb_id=movie_data['id'],
                        defaults={
                            'title': movie_data['title'],
                            'overview': movie_data.get('overview', ''),
                            'release_date': movie_data.get('release_date') or None,
                            'popularity': movie_data.get('popularity'),
                            'poster_path': movie_data.get('poster_path'),
                            'backdrop_path': movie_data.get('backdrop_path'),
                            'vote_average': movie_data.get('vote_average'),
                            'vote_count': movie_data.get('vote_count'),
                        }
                    )

                    # 장르 연결
                    genre_ids = movie_data.get('genre_ids', [])
                    for genre_id in genre_ids:
                        try:
                            genre = Genre.objects.get(tmdb_id=genre_id)
                            movie.genres.add(genre)
                        except Genre.DoesNotExist:
                            self.stderr.write(self.style.ERROR(f'장르 ID {genre_id}를 찾을 수 없습니다.'))

                self.stdout.write(self.style.SUCCESS(f'페이지 {page}/{start_pages + total_pages} 데이터를 가져왔습니다.'))
                # API 호출 간 딜레이 설정 (TMDB API 정책 준수)
                time.sleep(0.25)
            else:
                self.stderr.write(self.style.ERROR(f'페이지 {page} 데이터를 가져오는 데 실패했습니다.'))
                # 에러 발생 시 다음 페이지로 넘어갑니다.
                continue

        self.stdout.write(self.style.SUCCESS('모든 영화 데이터를 성공적으로 가져왔습니다.'))
