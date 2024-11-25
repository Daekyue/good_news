import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewsFeed from '../views/NewsFeed.vue';
import NewsList from '../views/NewsList.vue';
import NewsDetail from '../views/NewsDetail.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    
    path: '/Home',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/news-feed',
    name: 'NewsFeed',
    component: NewsFeed,
  },
  {
    path: '/news',
    name: 'NewsList',
    component: NewsList  
  },
  {
    path: '/news-article/:id',
    name: 'NewsDetail',
    component: NewsDetail,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

export default router;