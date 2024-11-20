<template>
  <div>
    <h1>홈 페이지</h1>
    <nav>
      <router-link to="/news-feed">뉴스 피드</router-link> |
      <router-link to="/chatbot">챗봇</router-link> |
      <router-link to="/news-article">뉴스 기사</router-link>
    </nav>
    <div>
      <h2>나의 관심 카테고리</h2>
      <!-- 관심 카테고리 표시 -->
    </div>
    <div>
      <h2>주요 키워드</h2>
      <!-- 주요 키워드 표시 -->
    </div>
    <div>
      <h2>주간 읽은 기사</h2>
      <!-- 주간 읽은 기사 표시 -->
    </div>
    <div>
      <h2>좋아요 누른 기사</h2>
      <!-- 좋아요 누른 기사 표시 -->
    </div>
  </div>
</template>
<script>
export default {
  name: 'HomePage',
};
</script>