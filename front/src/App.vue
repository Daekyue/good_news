<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
  },
};
</script>

<style>
/* 전역 스타일은 여기에 작성 */
#app {
  background-color: #1a1a1a;
  font-family: Arial, sans-serif;
  color: #2c3e50;
  margin-top: 60px;
}
</style>