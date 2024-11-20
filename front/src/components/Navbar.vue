<template>
  <nav>
    <div class="nav-left">
      <router-link to="/Home">홈</router-link> |
      <router-link to="/news-feed">뉴스 피드</router-link> |
      <router-link to="/chatbot">챗봇</router-link> |
      <router-link to="/news-article">뉴스 기사</router-link>
    </div>
    <div class="nav-right">
      <router-link to="/login">로그아웃</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
};
</script>

<style scoped>
nav {
  display: flex; /* Flexbox 사용 */
  justify-content: space-between; /* 좌우 끝으로 요소 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  background-color: #333;
  padding: 1em;
}

.nav-left a,
.nav-right a {
  color: #fff;
  margin-right: 1em;
  text-decoration: none;
}

.nav-right a {
  margin-right: 0; /* 오른쪽 끝 정렬에서 간격 제거 */
}

.nav-left a:hover,
.nav-right a:hover {
  text-decoration: underline;
}
</style>
