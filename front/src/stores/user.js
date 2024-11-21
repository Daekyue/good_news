import { ref, watch } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router'; // 라우터 인스턴스 직접 임포트

export const useUserStore = defineStore('user', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(localStorage.getItem('token') || null);
  const loginUsername = ref(localStorage.getItem('loginUsername') || null);

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

        // Store the token and username in localStorage
        localStorage.setItem('token', response.data.key);
        localStorage.setItem('loginUsername', username);

        // Set the Authorization header for future requests
        axios.defaults.headers.common['Authorization'] = `Token ${token.value}`;

        router.push('/Home'); // 로그인 성공 시 '/Home' 경로로 이동
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

  // 로그아웃 함수 추가
  const logOut = function () {
    token.value = null;
    loginUsername.value = null;

    // Remove the token from localStorage and Axios default headers
    localStorage.removeItem('token');
    localStorage.removeItem('loginUsername');
    delete axios.defaults.headers.common['Authorization'];

    router.push('/'); // 로그아웃 후 로그인 페이지로 이동
  };

  // Watch for token changes and update Axios defaults
  watch(token, (newToken) => {
    if (newToken) {
      axios.defaults.headers.common['Authorization'] = `Token ${newToken}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  });

  return { token, loginUsername, logIn, signUp, logOut };
}, { persist: true });
