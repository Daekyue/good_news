<script>
import axios from 'axios';

export default {
  name: 'NewsDetail',
  props: ['id'],
  data() {
    return {
      article: null,
      liked: false,
      chatbotInput: '', // 사용자 입력 값
      chatbotMessages: [
        {
          role: 'assistant',
          content: '안녕하세요! 😊 어떻게 도와드릴까요? 보고 계신 뉴스에 대해 궁금한 점이 있으시면 언제든지 질문해 주세요!'
        }
      ],
      relatedArticles: [] // 관련 기사 데이터를 저장할 곳
    };
  },
  created() {
    this.fetchArticle();
    this.increaseViews();
    this.fetchRelatedArticles(); // 관련 기사 데이터 가져오기
  },
  methods: {
    fetchArticle() {
      axios
        .get(`http://localhost:8000/api/news/${this.id}/`, {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}` // 인증 토큰 추가
          }
        })
        .then((response) => {
          this.article = response.data;
          this.liked = response.data.liked; // 서버에서 받아온 liked 상태를 반영
        })
        .catch((error) => {
          console.error('Error fetching article:', error);
        });
    },
    fetchRelatedArticles() {
      // 관련 기사 데이터를 가져오기 위한 API 호출
      axios
        .get(`http://localhost:8000/api/news/${this.id}/related_articles/`)
        .then((response) => {
          this.relatedArticles = response.data.related_articles; // 관련 기사 데이터 저장
        })
        .catch((error) => {
          console.error('Error fetching related articles:', error);
        });
    },
    increaseViews() {
      axios.post(`http://localhost:8000/api/news/${this.id}/increase_views/`)
        .catch((error) => {
          console.error('Error increasing views:', error);
        });
    },
    toggleLike() {
      axios.post(`http://localhost:8000/api/news/${this.id}/toggle_like/`, {}, {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}` // 인증 토큰 추가
        }
      })
        .then((response) => {
          this.article.likes_count = response.data.likes_count;
          this.liked = response.data.liked; // 좋아요 상태 업데이트
        })
        .catch((error) => {
          console.error('Error toggling like:', error);
        });
    },
    sendChatbotMessage() {
      if (this.chatbotInput.trim() === '') return;

      const userMessage = {
        role: 'user',
        content: this.chatbotInput
      };
      this.chatbotMessages.push(userMessage);

      axios.post(`http://localhost:8000/api/chatbot/`, {
        user_input: this.chatbotInput
      }, {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then((response) => {
          const botMessage = {
            role: 'assistant',
            content: response.data.answer
          };
          this.chatbotMessages.push(botMessage);
          this.chatbotInput = '';
        })
        .catch((error) => {
          console.error('Error communicating with chatbot:', error);
          const errorMessage = {
            role: 'assistant',
            content: 'Sorry, there was an issue generating a response.'
          };
          this.chatbotMessages.push(errorMessage);
        });
    }
  }
};
</script>

<template>
  <div class="news-page-container">
    <!-- 뉴스 상세보기 및 챗봇 섹션 래퍼 -->
    <div class="left-section-wrapper">
      <!-- 뉴스 상세보기 섹션 -->
      <section class="news-detail-section">
        <div v-if="article" class="news-detail-container">
          <h1 class="news-detail-title">{{ article.title }}</h1>
          <div class="news-detail-info">
            <p>작성일: {{ article.date }}</p>
            <p>조회수: 👁️ {{ article.views_count }}</p>
          </div>
          <div class="news-detail-content">
            <p>{{ article.content }}</p>
          </div>
          <!-- 키워드 태그 섹션 -->
          <div class="news-detail-keywords">
            <span v-for="(keyword, index) in article.keywords.split(',')" :key="index" class="keyword-tag">
              {{ keyword.trim() }}
            </span>
          </div>
          <!-- 좋아요 버튼 섹션 -->
          <div class="like-button-container">
            <button @click="toggleLike" :class="['like-button', { liked: liked }]">
              {{ liked ? '❤️ 좋아요 취소' : '🤍 좋아요' }} ({{ article.likes_count }})
            </button>
          </div>
        </div>
        <div v-else>
          <p>뉴스 기사를 불러오는 중입니다...</p>
        </div>
      </section>

      <!-- AI 뉴스비서 섹션 -->
      <section class="chatbot-section">
        <h2>AI News Assistant</h2>
        <p>Feel free to ask Newbie anything about this article!</p>
        <div class="chat-container">
          <div v-for="(message, index) in chatbotMessages" :key="index" class="chat-message" :class="message.role">
            {{ message.content }}
          </div>
        </div>
        <input v-model="chatbotInput" @keyup.enter="sendChatbotMessage" type="text"
          placeholder="Enter your question..." />
      </section>
    </div>

    <!-- 관련 기사 섹션 -->
    <aside class="related-articles-section">
      <h2>관련 기사</h2>
      <ul class="related-articles-list">
        <li v-for="related in relatedArticles" :key="related.id" class="related-article-item">
          <h3>
            <router-link :to="{ name: 'NewsDetail', params: { id: related.id } }">
              {{ related.title }}
            </router-link>
          </h3>
          <p>{{ related.date }}</p>
        </li>
      </ul>
    </aside>
  </div>
</template>


<style scoped>
/* 뉴스 페이지 전체 레이아웃 */
.news-page-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  /* 왼쪽에 뉴스 상세보기와 챗봇(2)과 오른쪽에 관련 기사(1) */
  gap: 20px;
  padding: 20px;
}

/* 왼쪽 섹션 래퍼 (뉴스 상세보기 및 챗봇) */
.left-section-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 뉴스 상세보기 섹션 스타일 */
.news-detail-section {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.news-detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.news-detail-title {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 15px;
}

.news-detail-info {
  color: #777;
  font-size: 0.9em;
  margin-bottom: 20px;
}

.news-detail-content {
  line-height: 1.6;
  font-size: 1.1em;
  margin-bottom: 20px;
}

/* 키워드 태그 스타일 */
.news-detail-keywords {
  margin-top: 20px;
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

/* 좋아요 버튼 섹션 */
.like-button-container {
  margin-top: 20px;
}

.like-button {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.like-button.liked {
  background-color: #dc3545;
}

.like-button:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* AI 뉴스비서 섹션 스타일 */
.chatbot-section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.chat-container {
  margin-bottom: 10px;
}

.chat-message {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 5px;
}

.chat-message.user {
  background-color: #d9edf7;
  text-align: right;
}

.chat-message.assistant {
  background-color: #f1f1f1;
  text-align: left;
}

/* 관련 기사 섹션 스타일 */
.related-articles-section {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 20px;
  /* 화면에 고정시키기 위해 사용 */
  align-self: start;
}

.related-articles-list {
  list-style: none;
  padding: 0;
}

.related-article-item {
  margin-bottom: 15px;
}

.related-article-item h3 {
  font-size: 1em;
  margin: 0 0 5px;
}

.related-article-item p {
  font-size: 0.9em;
  color: #777;
  margin: 0;
}
</style>
