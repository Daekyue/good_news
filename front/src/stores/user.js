import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router'; // 라우터 인스턴스 직접 임포트

export const useUserStore = defineStore('user', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(null);
  const loginUsername = ref(null);

  const logIn = function (payload) {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/login/`,
      data: {
        username,
        password
      }
    })
      .then((response) => {
        console.log('response = ', response);
        token.value = response.data.key;
        loginUsername.value = username;

        router.push('/Home'); // 로그인 성공 시 '/' 경로로 이동
      })
      .catch((error) => {
        console.log('error = ', error);
      });
  };

  const signUp = function (payload) {
    const { username, password1, password2 } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/registration/`,
      data: {
        username,
        password1,
        password2
      }
    })
      .then((response) => {
        alert('회원가입 성공!');
        logIn({ username, password: password1 });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return { token, loginUsername, logIn, signUp };
}, { persist: true });
