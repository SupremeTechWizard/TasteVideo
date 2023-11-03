import { reactive, readonly } from 'vue';

const state = reactive({
  user: null,
  token: localStorage.getItem('token'),
  isLoggedIn: false
});

const setUser = (user) => {
  state.user = user;
  state.isLoggedIn = true;
};

const setToken = (token) => {
  state.token = token;
  localStorage.setItem('token', token);
  state.isLoggedIn = true;
};

const setLoggedIn = (isLoggedIn) => {
  state.isLoggedIn = isLoggedIn;
};

const checkAuth = async () => {
  if (state.token) {
    try {
      const response = await fetch('http://localhost:8000/VerifyToken', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.token}`
        }
      });
      state.isLoggedIn = response.ok;
      if (!state.isLoggedIn) {
        localStorage.removeItem('token');
        state.token = null;
      }
    } catch (error) {
      console.error('验证token失败：', error);
      state.isLoggedIn = false;
      localStorage.removeItem('token');
      state.token = null;
    }
  }
};

const logout = () => {
  state.user = null;
  state.token = null;
  state.isLoggedIn = false;
  localStorage.removeItem('token');
};

export const useUserStore = () => {
  return {
    state: readonly(state),
    setUser,
    setToken,
    setLoggedIn,
    checkAuth,
    logout
  };
};
