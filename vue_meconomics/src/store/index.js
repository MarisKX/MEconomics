import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    isAuthenticated: false,
    userEmail: null,
  },
  mutations: {
    setIsAuthenticated(state, value) {
      state.isAuthenticated = value;
    },
    setUserEmail(state, value) {
      state.userEmail = value;
    },
    setDate(state, value) {
      state.dateToday = value;
    },
  },
  actions: {
    async checkAuthentication({ commit }) {
      try {
        const response = await axios.get(
          "https://meconomics.com:8000/api/user/check-auth/",
          {
            withCredentials: true,
          }
        );

        if (response.data.authenticated) {
          commit("setIsAuthenticated", true);
          commit("setUserEmail", response.data.username);
          commit("setDate", response.data.dateToday);
          console.log(response.data.dateToday);
        } else {
          commit("setIsAuthenticated", false);
        }
      } catch (err) {
        console.error("Error:", err);
      }
    },
  },
  modules: {},
});
