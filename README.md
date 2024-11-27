# good_news

## 가상환경
### 가상 환경 생성 (Windows)
python -m venv venv

### 가상 환경 생성 (Mac/Linux)
python3 -m venv venv

### 가상 환경 활성화 (Windows)
source venv/Scripts/activate

### 가상 환경 활성화 (Mac/Linux)
source venv/bin/activate

### requirements.txt 작성법
pip freeze > requirements.txt

### 패키지 목록이 존재할 때 그것들을 설치하는 방법
pip install -r requirements.txt

sudo service postgresql start   # 서버 시작
sudo service postgresql stop    # 서버 종료
sudo service postgresql restart # 서버 재시작


---
테이블 구조
// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table users {
  id integer [primary key]
  username varchar
  email varchar
  password varchar
  nickname varchar [note: 'Custom Field, max_length=100']
  created_at timestamp

  Indexes {
    (email) [unique]
  }
}

Table news_articles {
  id integer [primary key]
  title varchar [note: 'max_length=255']
  content text
  category varchar [note: 'choices=[뉴스, 기획, 리뷰, 인터뷰, 칼럼, 평론, 영화제]']
  date date [null]
  url varchar [note: 'max_length=255']
  keywords text [null]
  views_count integer [default: 0]
  likes_count integer [default: 0]
  created_at timestamp
}

Table genres {
  id integer [primary key]
  tmdb_id integer [unique]
  name varchar [note: 'max_length=100']
}

Table directors {
  id integer [primary key]
  tmdb_id integer [unique]
  name varchar [note: 'max_length=255']
}

Table actors {
  id integer [primary key]
  tmdb_id integer [unique]
  name varchar [note: 'max_length=255']
  character varchar [null, note: 'max_length=255']
}

Table movies {
  id integer [primary key]
  tmdb_id integer [unique]
  title varchar [note: 'max_length=255']
  overview text
  release_date date [null]
  popularity float [null]
  vote_average float [null]
  vote_count integer [null]
  poster_path varchar [null, note: 'max_length=255']
  backdrop_path varchar [null, note: 'max_length=255']
  created_at timestamp
}

Table user_liked_articles {
  user_id integer
  article_id integer

  Indexes {
    (user_id, article_id) [unique]
  }
}

Table movie_genres {
  movie_id integer
  genre_id integer

  Indexes {
    (movie_id, genre_id) [unique]
  }
}

Table movie_directors {
  movie_id integer
  director_id integer

  Indexes {
    (movie_id, director_id) [unique]
  }
}

Table movie_actors {
  movie_id integer
  actor_id integer

  Indexes {
    (movie_id, actor_id) [unique]
  }
}

Ref: user_liked_articles.user_id > users.id
Ref: user_liked_articles.article_id > news_articles.id

Ref: movie_genres.movie_id > movies.id
Ref: movie_genres.genre_id > genres.id

Ref: movie_directors.movie_id > movies.id
Ref: movie_directors.director_id > directors.id

Ref: movie_actors.movie_id > movies.id
Ref: movie_actors.actor_id > actors.id
