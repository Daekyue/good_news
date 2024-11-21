<script>
import axios from 'axios';

export default {
  name: 'NewsList',
  data() {
    return {
      newsList: [],
      filteredNews: [],
      selectedCategory: '전체',
      categories: ['전체', '뉴스', '기획', '리뷰', '인터뷰', '칼럼', '평론', '영화제'],
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
          this.newsList = response.data;
          this.filteredNews = response.data; // 처음에는 모든 뉴스 표시
        })
        .catch((error) => {
          console.error('Error fetching news articles:', error);
        });
    },
    filterByCategory(category) {
      this.selectedCategory = category;
      if (category === '전체') {
        this.filteredNews = this.newsList;
      } else {
        this.filteredNews = this.newsList.filter(article => 
          article.category.toLowerCase() === category.toLowerCase()
        );
      }
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

    <!-- 카테고리 선택 버튼 -->
    <div class="category-buttons">
      <button v-for="(category, index) in categories" :key="index"
        :class="['category-button', { active: selectedCategory === category }]" @click="filterByCategory(category)">
        {{ category }}
      </button>
    </div>

    <!-- 뉴스 리스트 -->
    <div v-if="filteredNews.length > 0">
      <div v-for="article in filteredNews" :key="article.id" class="news_article">
        <!-- 뉴스 제목과 내용 -->
        <h2>
          <router-link :to="{ name: 'NewsDetail', params: { id: article.id } }">
            {{ article.title }}
          </router-link>
        </h2>
        <p>{{ article.content }}</p>
        <!-- 키워드 태그 섹션 -->
        <div class="news-keywords">
          <span v-for="(keyword, index) in article.keywords.split(',')" :key="index" class="keyword-tag">
            {{ keyword.trim() }}
          </span>
        </div>
        <small>{{ article.date }}</small>
      </div>
    </div>
    <div v-else>
      <p>현재 표시할 뉴스가 없습니다.</p>
    </div>
  </div>
</template>

<style scoped>
.news_list_head {
  margin-bottom: 10px;
}

.news_separator {
  border-top: 1px solid #e0e0e0;
}

.news_article {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 키워드 태그 스타일 */
.news-keywords {
  margin-bottom: 10px;
}

.keyword-tag {
  display: inline-block;
  background-color: #e0e0e0;
  color: #333;
  padding: 5px 10px;
  margin: 5px 5px 0 0;
  border-radius: 15px;
  font-size: 0.9em;
}

/* 카테고리 버튼 스타일 */
.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0;
  border: 1px solid #e0e0e0;
  padding: 10px;
  border-radius: 10px;
}

.category-button {
  padding: 10px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background-color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.category-button:hover {
  background-color: #f0f0f0;
}

.category-button.active {
  background-color: #007bff;
  color: #ffffff;
  border-color: #007bff;
}
</style>
