import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "../views/HomeView.vue";
import CitizenView from "../views/CitizenView.vue";
import CompanyView from "../views/CompanyView.vue";

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
    path: "/citizen-details/:id",
    name: "citizen-details",
    component: () =>
      import(
        /* webpackChunkName: "citizens" */ "../views/CitizenDetailsView.vue"
      ),
    meta: { requiresAuth: true },
    props: true, // This line is important
  },
  {
    path: "/companies",
    name: "companies",
    component: CompanyView,
    meta: { requiresAuth: true },
  },
  {
    path: "/company-details/:id",
    name: "company-details",
    component: () =>
      import(
        /* webpackChunkName: "citizens" */ "../views/CompanyDetailsView.vue"
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
