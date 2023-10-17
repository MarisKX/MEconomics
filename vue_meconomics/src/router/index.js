import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "../views/HomeView.vue";
import CitizenView from "../views/CitizenView.vue";
import CompanyView from "../views/CompanyView.vue";
import GovernmentView from "../views/GovernmentView.vue";

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
    props: true,
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
    props: true,
  },
  {
    path: "/government",
    name: "government",
    component: GovernmentView,
    meta: { requiresAuth: true },
  },
  {
    path: "/government-details/:id",
    name: "government-details",
    component: () =>
      import(
        /* webpackChunkName: "citizens" */ "../views/GovernmentDetailsView.vue"
      ),
    meta: { requiresAuth: true },
    props: true,
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

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (!requiresAuth) {
    next();
    return;
  }

  try {
    await store.dispatch("checkAuthentication");
    const isAuthenticated = store.state.isAuthenticated;

    if (!isAuthenticated) {
      next({ name: "login" });
    } else {
      next();
    }
  } catch (error) {
    console.error("Error during route guard execution:", error);
    next(false);
  }
});

export default router;
