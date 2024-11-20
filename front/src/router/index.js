import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewsFeed from '../views/NewsFeed.vue';
import ChatbotPage from '../views/ChatbotPage.vue';
import NewsArticle from '../views/NewsArticle.vue';
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/Login',
    name: 'Login',
    component: Login
  },
  {
    
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/news-feed',
    name: 'NewsFeed',
    component: NewsFeed,
  },
  {
    path: '/chatbot',
    name: 'Chatbot',
    component: ChatbotPage,
  },
  {
    path: '/news-article',
    name: 'NewsArticle',
    component: NewsArticle,
  }
];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

export default router;