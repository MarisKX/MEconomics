import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "../views/HomeView.vue";
import CitizenView from "../views/CitizenView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/citizens",
    name: "citizens",
    component: CitizenView,
    meta: { requiresAuth: true },
  },
  {
    path: "/citizens-details/:id",
    name: "citizens-details",
    component: () =>
      import(
        /* webpackChunkName: "citizens" */ "../views/CitizensDetailsView.vue"
      ),
    meta: { requiresAuth: true },
    props: true, // This line is important
  },
  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/LoginView.vue"),
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated;

  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !isAuthenticated
  ) {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
