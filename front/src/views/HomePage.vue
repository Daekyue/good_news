<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      likedArticles: [],
    };
  },
  created() {
    this.fetchLikedArticles();
  },
  methods: {
    fetchLikedArticles() {
      axios
        .get('http://localhost:8000/api/news/liked/')
        .then((response) => {
          this.likedArticles = response.data;
        })
        .catch((error) => {
          console.error('Error fetching liked articles:', error);
        });
    },
  },
};
</script>

<template>
  <div>
    <h1>내가 좋아요 누른 뉴스</h1>
    <div v-if="likedArticles.length > 0">
      <div v-for="article in likedArticles" :key="article.id" class="news_article">
        <h2>
          <router-link :to="{ name: 'NewsDetail', params: { id: article.id } }">
            {{ article.title }}
          </router-link>
        </h2>
        <p>{{ article.content }}</p>
        <small>{{ article.date }}</small>
      </div>
    </div>
    <div v-else>
      <p>좋아요를 누른 뉴스가 없습니다.</p>
    </div>
  </div>
</template>

<style scoped>
div {
  margin: 20px;
}
h1 {
  color: #2c3e50;
}
</style>