import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import store from "./store";
import router from "./router";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./assets/css/global.css";
import "./assets/css/colors.css";
import Cookies from "js-cookie";

axios.defaults.withCredentials = true;
const csrfTokenValue = Cookies.get("csrftoken");

if (csrfTokenValue) {
  axios.defaults.headers.common["X-CSRFToken"] = csrfTokenValue;
}

// Check authentication and create the app
store.dispatch("checkAuthentication").then(() => {
  createApp(App).use(store).use(router).mount("#app");
});
