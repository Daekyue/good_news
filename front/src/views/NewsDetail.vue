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
        <p>보고 계신 뉴스에 대해 궁금한 점이 있으시면 언제든지 질문해 주세요!</p>
        <div class="chat-container">
          <div v-for="(message, index) in chatbotMessages" :key="index" :class="['chat-message', message.role]">
            <div class="message-bubble">
              {{ message.content }}
            </div>
          </div>
        </div>
        <div class="chat-input-container">
          <input v-model="chatbotInput" @keyup.enter="sendChatbotMessage" type="text"
            placeholder="Enter your question..." />
          <button @click="sendChatbotMessage" class="send-button">
            <span class="send-button-icon">📨</span>
          </button>
        </div>
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
          content:
            '안녕하세요! 😊 어떻게 도와드릴까요? 보고 계신 뉴스에 대해 궁금한 점이 있으시면 언제든지 질문해 주세요!',
        },
      ],
      relatedArticles: [], // 관련 기사 데이터를 저장할 곳
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
            Authorization: `Token ${localStorage.getItem('token')}`, // 인증 토큰 추가
          },
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
      axios
        .post(`http://localhost:8000/api/news/${this.id}/increase_views/`)
        .catch((error) => {
          console.error('Error increasing views:', error);
        });
    },
    toggleLike() {
      axios
        .post(
          `http://localhost:8000/api/news/${this.id}/toggle_like/`,
          {},
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`, // 인증 토큰 추가
            },
          }
        )
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
        content: this.chatbotInput,
      };
      this.chatbotMessages.push(userMessage);

      axios
        .post(
          `http://localhost:8000/api/chatbot/`,
          {
            user_input: this.chatbotInput,
            movie_id: this.id, // movie_id 추가
          },
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`,
            },
          }
        )
        .then((response) => {
          const botMessage = {
            role: 'assistant',
            content: response.data.answer,
          };
          this.chatbotMessages.push(botMessage);
          this.chatbotInput = '';
        })
        .catch((error) => {
          console.error('Error communicating with chatbot:', error);
          const errorMessage = {
            role: 'assistant',
            content: '죄송합니다, 응답을 생성하는 데 문제가 발생했습니다.',
          };
          this.chatbotMessages.push(errorMessage);
        });
    },
  },
};
</script>

<style scoped>
/* 뉴스 페이지 전체 레이아웃 */
.news-page-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  padding: 20px;
  background-color: #000;
  color: #f5f5f5;
  font-family: 'Arial', sans-serif;
}

/* 왼쪽 섹션 래퍼 (뉴스 상세보기 및 챗봇) */
.left-section-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 뉴스 상세보기 섹션 스타일 */
.news-detail-section {
  background-color: #222;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.news-detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.news-detail-title {
  font-size: 2.8em;
  font-weight: bold;
  margin-bottom: 15px;
  color: #e0b534;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.news-detail-info {
  color: #bbbbbb;
  font-size: 0.9em;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.news-detail-content {
  line-height: 1.8;
  font-size: 1.2em;
  margin-bottom: 20px;
  color: #dddddd;
}

/* 키워드 태그 스타일 */
.news-detail-keywords {
  margin-top: 20px;
}

.keyword-tag {
  display: inline-block;
  background-color: #444;
  color: #e0b534;
  padding: 8px 12px;
  margin: 5px 5px 0 0;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* 좋아요 버튼 섹션 */
.like-button-container {
  margin-top: 20px;
}

.like-button {
  background-color: #c62828;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
  font-size: 1em;
}

.like-button.liked {
  background-color: #e0b534;
  color: #1a1a1a;
}

.like-button:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* AI 뉴스비서 섹션 스타일 */
.chatbot-section {
  background-color: #222;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.chatbot-section h2 {
  font-size: 2em;
  margin-bottom: 10px;
  color: #e0b534;
}

.chatbot-section p {
  margin-bottom: 20px;
  color: #bbbbbb;
}

.chat-container {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #333;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.chat-message {
  display: flex;
  margin-bottom: 10px;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 20px;
  word-wrap: break-word;
  position: relative;
}

.chat-message.user .message-bubble {
  background-color: #d1e7dd;
  color: #0f5132;
  border-bottom-right-radius: 5px;
}

.chat-message.assistant .message-bubble {
  background-color: #444;
  color: #e0b534;
  border-bottom-left-radius: 5px;
}

/* 입력창 및 버튼 스타일 */
.chat-input-container {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.chat-input-container input[type='text'] {
  flex: 1;
  padding: 12px 20px;
  font-size: 1em;
  border-radius: 25px;
  border: 1px solid #555;
  outline: none;
  background-color: #333;
  color: #f5f5f5;
  transition: border-color 0.3s;
}

.chat-input-container input[type='text']:focus {
  border-color: #e0b534;
}

.send-button {
  background-color: #e0b534;
  color: #1a1a1a;
  border: none;
  margin-left: 10px;
  padding: 12px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #c62828;
  color: #ffffff;
}

.send-button-icon {
  font-size: 1.2em;
}

/* 관련 기사 섹션 스타일 */
.related-articles-section {
  background-color: #222;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  position: sticky;
  top: 20px;
  align-self: start;
}

.related-articles-section h2 {
  font-size: 1.8em;
  margin-bottom: 15px;
  color: #e0b534;
}

.related-articles-list {
  list-style: none;
  padding: 0;
}

.related-article-item {
  margin-bottom: 15px;
}

.related-article-item h3 {
  font-size: 1.1em;
  margin: 0 0 5px;
  color: #007bff;
}

.related-article-item h3 a {
  text-decoration: none;
  color: #e0b534;
  transition: color 0.3s;
}

.related-article-item h3 a:hover {
  color: #f5f5f5;
}

.related-article-item p {
  font-size: 0.9em;
  color: #bbbbbb;
  margin: 0;
}

</style>
