<template>
  <div class="home-page-container">
    <!-- 워드클라우드 섹션 -->
    <section class="wordcloud-section">
      <h2>지난 7일간 키워드 워드클라우드</h2>
      <div v-if="wordCloudImageUrl">
        <img :src="wordCloudImageUrl" alt="Word Cloud" class="wordcloud-image" />
      </div>
      <div v-else>
        <p>워드클라우드를 불러오는 중입니다...</p>
      </div>
    </section>

    <!-- 내가 좋아요 누른 뉴스 섹션 -->
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
          <p>{{ article.content }}</p>
        </div>
      </div>
      <div v-else>
        <p>좋아요를 누른 뉴스가 없습니다.</p>
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
      wordCloudImageUrl: '', // 워드클라우드 이미지 URL을 저장할 변수
    };
  },
  created() {
    this.fetchLikedArticles();
    this.fetchWordCloud(); // 워드클라우드 이미지를 가져옴
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
          responseType: 'blob', // 이미지 데이터를 가져오기 위해 responseType 설정
        })
        .then((response) => {
          const url = URL.createObjectURL(response.data);
          this.wordCloudImageUrl = url; // 이미지 URL 설정
        })
        .catch((error) => {
          console.error('Error fetching word cloud:', error);
        });
    },
  },
};
</script>

<style scoped>
.home-page-container {
  display: grid;
  grid-template-areas:
    'wordcloud wordcloud'
    'liked liked';
  gap: 20px;
  padding: 20px;
  background-color: #f0f2f5; /* 전체 배경색 추가 */
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
</style>
