<template>
  <div class="home-page-container">
    <!-- 워드클라우드 섹션 (1번) -->
    <section class="wordcloud-section">
      <h2>지난 7일간 키워드 워드클라우드</h2>
      <div v-if="wordCloudImageUrl">
        <img :src="wordCloudImageUrl" alt="Word Cloud" class="wordcloud-image" />
      </div>
      <div v-else>
        <p>워드클라우드를 불러오는 중입니다...</p>
      </div>
    </section>

    <!-- 추천 시스템 섹션 (2, 3, 4번) -->
    <section class="recommend-section" id="recommend1">
      <h2>추천 영화</h2>
      <div v-if="recommendedMovies && recommendedMovies.length > 0">
        <div v-for="movie in recommendedMovies" :key="movie.id" class="movie-item">
          <h3>{{ movie.title }}</h3>
          <p>{{ truncateText(movie.overview, 100) }}</p>
        </div>
      </div>
      <div v-else>
        <p>추천할 영화가 없습니다.</p>
      </div>
    </section>

    <!-- 추천 감독 섹션 (3번) -->
    <section class="recommend-section" id="recommend2">
      <h2>추천 감독</h2>
      <div v-if="recommendedDirectors && recommendedDirectors.length > 0">
        <ul>
          <li v-for="director in recommendedDirectors" :key="director.id">
            {{ director.name }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>추천할 감독이 없습니다.</p>
      </div>
    </section>

    <!-- 추천 배우 섹션 (4번) -->
    <section class="recommend-section" id="recommend3">
      <h2>추천 배우</h2>
      <div v-if="recommendedActors && recommendedActors.length > 0">
        <ul>
          <li v-for="actor in recommendedActors" :key="actor.id">
            {{ actor.name }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>추천할 배우가 없습니다.</p>
      </div>
    </section>

    <!-- 내가 좋아요 누른 뉴스 섹션 (5번) -->
    <section class="liked-articles-section">
      <h1>내가 좋아요 누른 뉴스</h1>
      <div v-if="likedArticles.length > 0">
        <div v-for="article in likedArticles" :key="article.id" class="news-article">
          <h2>
            <router-link :to="{ name: 'NewsDetail', params: { id: article.id } }">
              {{ article.title }}
            </router-link>
          </h2>
          <div class="article-info">
            <span>작성일: {{ article.date }}</span>
            <span>조회수: 👁️ {{ article.views_count }}</span>
            <span>좋아요: ❤️ {{ article.likes_count }}</span>
          </div>
          <p>{{ truncateText(article.content, 200) }}</p>
        </div>
      </div>
      <div v-else>
        <p>좋아요를 누른 뉴스가 없습니다.</p>
      </div>
    </section>

    <!-- 일주일간 조회수가 높은 기사 섹션 (6번) -->
    <section class="top-articles-section">
      <h1>일주일간 조회수가 높은 기사</h1>
      <div v-if="topArticles.length > 0">
        <div v-for="article in topArticles" :key="article.id" class="news-article">
          <h2>
            <router-link :to="{ name: 'NewsDetail', params: { id: article.id } }">
              {{ article.title }}
            </router-link>
          </h2>
          <div class="article-info">
            <span>작성일: {{ article.date }}</span>
            <span>조회수: 👁️ {{ article.views_count }}</span>
            <span>좋아요: ❤️ {{ article.likes_count }}</span>
          </div>
          <p>{{ truncateText(article.content, 200) }}</p>
        </div>
      </div>
      <div v-else>
        <p>인기 기사를 불러오는 중입니다...</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      likedArticles: [],
      wordCloudImageUrl: '',
      topArticles: [],
      recommendedMovies: [],
      recommendedDirectors: [],
      recommendedActors: [],
    };
  },
  created() {
    this.fetchLikedArticles();
    this.fetchWordCloud();
    this.fetchRecommendations();
    this.fetchTopArticles();
  },
  methods: {
    fetchLikedArticles() {
      axios
        .get('http://localhost:8000/api/news/liked/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          this.likedArticles = response.data;
        })
        .catch((error) => {
          console.error('Error fetching liked articles:', error);
        });
    },
    fetchWordCloud() {
      axios
        .get('http://localhost:8000/api/news/wordcloud/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
          responseType: 'blob',
        })
        .then((response) => {
          const url = URL.createObjectURL(response.data);
          this.wordCloudImageUrl = url;
        })
        .catch((error) => {
          console.error('Error fetching word cloud:', error);
        });
    },
    fetchRecommendations() {
      axios
        .get('http://localhost:8000/api/news/recommend/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          this.recommendedMovies = response.data.movies;
          this.recommendedDirectors = response.data.directors;
          this.recommendedActors = response.data.actors;
        })
        .catch((error) => {
          console.error('Error fetching recommendations:', error);
          this.recommendedMovies = [];
          this.recommendedDirectors = [];
          this.recommendedActors = [];
        });
    },
    fetchTopArticles() {
      axios
        .get('http://localhost:8000/api/news/top_articles/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          this.topArticles = response.data;
        })
        .catch((error) => {
          console.error('Error fetching top articles:', error);
        });
    },
    truncateText(text, maxLength) {
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
  },
};
</script>

<style scoped>
/* 영화 웹페이지 스타일 - CSS */
/* 영화 웹페이지 스타일 - CSS */
.home-page-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto auto auto;
  grid-template-areas:
    'wordcloud wordcloud wordcloud'
    'recommend1 recommend2 recommend3'
    'liked liked top-articles';
  gap: 30px;
  padding: 40px;
  background-color: #1a1a1a; /* 영화관 느낌의 어두운 배경 */
  color: #f5f5f5; /* 전체적인 글씨색을 밝게 */
  font-family: 'Arial', sans-serif;
}

/* 워드클라우드 섹션 */
.wordcloud-section {
  grid-area: wordcloud;
  text-align: center;
  background-color: #2b2b2b; /* 어두운 배경 색상 */
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

.wordcloud-section h2 {
  font-size: 2.2em;
  margin-bottom: 20px;
  color: #e0b534; /* 금색으로 영화 시상식 느낌 */
  font-weight: bold;
}

.wordcloud-image {
  max-width: 100%;
  height: auto;
  border-radius: 15px;
  border: 3px solid #e0b534; /* 이미지 테두리에 금색 효과 */
}

/* 추천 시스템 섹션 */
.recommend-section {
  background-color: #2b2b2b;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

.recommend-section h2 {
  font-size: 1.8em;
  margin-bottom: 15px;
  color: #e0b534;
  font-weight: bold;
}

.movie-item h3 {
  font-size: 1.6em;
  margin-bottom: 10px;
  color: #f5f5f5;
  font-weight: bold;
  font-style: italic;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.movie-item p {
  font-size: 1em;
  color: #bbbbbb;
}

ul {
  list-style: none;
  padding-left: 0;
}

li {
  font-size: 1.3em;
  margin: 10px 0;
  color: #f5f5f5;
  font-weight: bold;
  font-style: italic;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* 내가 좋아요 누른 뉴스 섹션 */
.liked-articles-section {
  grid-area: liked;
  background-color: #2b2b2b;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

.liked-articles-section h1 {
  font-size: 2.2em;
  margin-bottom: 20px;
  color: #e0b534;
  font-weight: bold;
}

.news-article {
  margin-bottom: 25px;
  padding: 20px;
  border: 1px solid #444;
  border-radius: 15px;
  background-color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s;
}

.news-article:hover {
  transform: translateY(-5px);
}

.news-article h2 {
  font-size: 1.6em;
  margin-bottom: 10px;
  color: #e0b534;
  font-weight: bold;
}

.news-article h2 a {
  text-decoration: none;
  color: #e0b534;
  transition: color 0.3s;
}

.news-article h2 a:hover {
  color: #f5f5f5;
}

.article-info {
  font-size: 0.9em;
  color: #aaaaaa;
  margin-bottom: 10px;
  display: flex;
  gap: 20px;
}

.news-article p {
  font-size: 1em;
  color: #dddddd;
}

/* 일주일간 조회수가 높은 기사 섹션 */
.top-articles-section {
  grid-area: top-articles;
  background-color: #2b2b2b;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

.top-articles-section h1 {
  font-size: 2.2em;
  margin-bottom: 20px;
  color: #e0b534;
  font-weight: bold;
}

/* 전반적인 스타일 향상 */
h1, h2, h3, p, span, li {
  letter-spacing: 0.5px;
}

a {
  transition: color 0.3s, transform 0.2s;
}

a:hover {
  color: #e0b534;
  transform: scale(1.05);
}

.box-shadow:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.7);
}

/* 버튼 스타일 */
button {
  background-color: #e0b534;
  color: #1a1a1a;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #f5f5f5;
  transform: translateY(-3px);
}

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.pagination button {
  margin: 0 5px;
  padding: 10px 15px;
  border: 1px solid #e0b534;
  border-radius: 5px;
  background-color: #2b2b2b;
  color: #e0b534;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.pagination button:hover {
  background-color: #e0b534;
  color: #1a1a1a;
}

.pagination button.active {
  background-color: #e0b534;
  color: #1a1a1a;
  font-weight: bold;
}


</style>
