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
      <div v-if="recommendedMovies.length > 0">
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
      <div v-if="recommendedDirectors.length > 0">
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
      <div v-if="recommendedActors.length > 0">
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
.home-page-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto auto auto;
  grid-template-areas:
    'wordcloud wordcloud wordcloud'
    'recommend1 recommend2 recommend3'
    'liked liked top-articles';
  gap: 20px;
  padding: 20px;
  background-color: #f0f2f5;
}

/* 워드클라우드 섹션 */
.wordcloud-section {
  grid-area: wordcloud;
  text-align: center;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.wordcloud-image {
  max-width: 100%;
  height: auto;
}

/* 추천 시스템 섹션 */
.recommend-section {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

#recommend1 {
  grid-area: recommend1;
}

#recommend2 {
  grid-area: recommend2;
}

#recommend3 {
  grid-area: recommend3;
}

.recommend-section h2 {
  font-size: 1.5em;
  margin-bottom: 15px;
  color: #333;
}

.recommend-section .news-article h3 {
  font-size: 1.2em;
  margin-bottom: 10px;
  color: #007bff;
}

.recommend-section .news-article p {
  font-size: 1em;
  color: #555;
}

/* 내가 좋아요 누른 뉴스 섹션 */
.liked-articles-section {
  grid-area: liked;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.liked-articles-section h1 {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #333;
}

.news-article {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.news-article h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: #007bff;
}

.news-article h2 a {
  text-decoration: none;
}

.news-article h2 a:hover {
  text-decoration: underline;
}

.article-info {
  font-size: 0.9em;
  color: #777;
  margin-bottom: 10px;
  display: flex;
  gap: 15px;
}

.news-article p {
  font-size: 1em;
  color: #555;
}

/* 일주일간 조회수가 높은 기사 섹션 */
.top-articles-section {
  grid-area: top-articles;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.top-articles-section h1 {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #333;
}
</style>
