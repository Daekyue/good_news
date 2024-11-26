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
    truncateText(text, maxLength) {
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
  },
};
</script>

<template>
  <div class="news_list_entire">
    <h1 class="news_list_head">뉴스 리스트</h1>

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
        <p>{{ truncateText(article.content, 500) }}</p>
        <!-- 키워드 태그 섹션 -->
        <div class="news-keywords">
          <span v-for="(keyword, index) in article.keywords.split(',')" :key="index" class="keyword-tag">
            {{ keyword.trim() }}
          </span>
        </div>
        <!-- 좋아요 수와 조회수 섹션 -->
        <div class="likes-views-container">
          <span class="like-count">❤️ {{ article.likes_count }}</span>
          <span class="view-count">👁️ {{ article.views_count }}</span>
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
/* 뉴스 리스트 스타일 - CSS */
.news_list_entire{
  background-color: #1a1a1a;
}

body {
  background-color: #1a1a1a; /* 전체 배경을 검은색으로 설정 */
  color: #f5f5f5; /* 기본 글씨색을 밝게 */
  font-family: 'Arial', sans-serif;
}

.news_list_head {
  margin-bottom: 10px;
  font-size: 2.8em;
  font-weight: bold;
  color: #e0b534;
  text-align: center;
  background: linear-gradient(to right, #e0b534, #ffb84d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-color: #222;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.news_separator {
  border-top: 2px solid #e0b534;
  margin: 20px 0;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.news_description {
  font-size: 1.5em;
  color: #bbbbbb;
  margin-bottom: 30px;
  text-align: center;
  background-color: #333;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.news_article {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #444;
  border-radius: 15px;
  background-color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s, box-shadow 0.3s;
}

.news_article:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.7);
}

.news_article h2 {
  font-size: 1.8em;
  margin-bottom: 10px;
  color: #e0b534;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.news_article h2 a {
  text-decoration: none;
  color: #e0b534;
  transition: color 0.3s;
}

.news_article h2 a:hover {
  color: #f5f5f5;
}

.news_article p {
  font-size: 1em;
  color: #dddddd;
  margin-bottom: 10px;
}

/* 좋아요 수와 조회수 섹션 */
.likes-views-container {
  margin-top: 10px;
  font-size: 0.9em;
  color: #aaaaaa;
  display: flex;
  gap: 15px;
}

.like-count, .view-count {
  display: inline-block;
}

/* 키워드 태그 스타일 */
.news-keywords {
  margin-bottom: 10px;
}

.keyword-tag {
  display: inline-block;
  background-color: #444;
  color: #e0b534;
  padding: 5px 10px;
  margin: 5px 5px 0 0;
  border-radius: 15px;
  font-size: 0.9em;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* 카테고리 버튼 스타일 */
.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0;
  border: 1px solid #444;
  padding: 15px;
  border-radius: 15px;
  background-color: #2b2b2b;
}

.category-button {
  padding: 10px 20px;
  border: 1px solid #e0b534;
  border-radius: 15px;
  background-color: #333;
  color: #e0b534;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, transform 0.2s;
  font-weight: bold;
}

.category-button:hover {
  background-color: #e0b534;
  color: #1a1a1a;
  transform: scale(1.05);
}

.category-button.active {
  background-color: #e0b534;
  color: #1a1a1a;
  border-color: #e0b534;
  font-weight: bold;
}


</style>
