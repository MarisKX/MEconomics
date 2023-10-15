<template>
  <div class="backdrop">
    <div class="login">
      <hr />
      <div class="feedback-error" v-if="feedback">{{ feedback }}</div>
      <form class="login-form" @submit.prevent="login">
        <label>Email:</label>
        <input type="email" required v-model="email" />
        <label>Password</label>
        <input type="password" required v-model="password" />
        <div class="remember-me">
          <input type="checkbox" />
          <label>Remember Me</label>
        </div>
        <button type="submit">LOGIN</button>
      </form>
      <hr />
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      email: "",
      password: "",
      feedback: "",
    };
  },
  methods: {
    async login() {
      axios
        .post(
          "https://meconomics.com:8000/api/user/token/",
          {
            email: this.email,
            password: this.password,
          },
          {
            withCredentials: true,
          }
        )
        .then((response) => {
          console.log(response);
          this.$store.commit("setIsAuthenticated", true);
          this.$store.commit("setUserEmail", response.data.username);
          this.$router.push("/");
        })
        .catch((error) => {
          console.log("Auth failed: ", error);
          if (error.response) {
            if (error.response.status === 400) {
              // Incorrect username/password
              this.feedback = "Incorrect username/email and/or password";
            } else {
              // Other server-related errors
              this.feedback = "Service unavailable. Please try again later.";
            }
          } else {
            // Network or client-side errors
            this.feedback = "An error occurred. Please check your connection.";
          }
        });
    },
  },
};
</script>
