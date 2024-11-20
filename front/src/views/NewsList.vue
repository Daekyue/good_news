<script>
import axios from 'axios';

export default {
  name: 'NewsList',
  data() {
    return {
      newsArticles: [],
    };
  },
  created() {
    this.fetchNewsArticles();
  },
  methods: {
    fetchNewsArticles() {
      axios
        .get('http://localhost:8000/api/news/')
        .then((response) => {
          this.newsArticles = response.data;
        })
        .catch((error) => {
          console.error('Error fetching news articles:', error);
        });
    },
  },
};
</script>

<template>
  <div>
    <h1 class="news_list_head">뉴스 리스트</h1>
    <div class="news_separator"></div>
    <div class="news_description">
      당신이 원하는 뉴스, 이제 AI가 직접 추천해드립니다!
    </div>
    <div v-if="newsArticles.length > 0">
      <div v-for="article in newsArticles" :key="article.id" class="news_article">
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
      <p>현재 표시할 뉴스가 없습니다.</p>
    </div>
  </div>
</template>

<style>
.news_list_head {
  margin-bottom: 10px;
}
.news_separator {
  border-top: 1px solid #e0e0e0;
}
.news_article {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
}
</style>
