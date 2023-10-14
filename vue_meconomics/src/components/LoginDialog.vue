<template>
  <div class="backdrop">
    <div class="login">
      <hr />
      <div class="feedback-error" v-if="feedback">{{ feedback }}</div>
      <form @submit.prevent="login">
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

<style scoped>
form {
  max-width: 420px;
  margin: 30px auto;
  background: white;
  text-align: left;
  padding: 20px;
  border-radius: 10px;
}
label {
  color: #aaa;
  display: inline-block;
  margin: 25px 0 15px;
  font-size: 0.6em;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}
input {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}
input[type="checkbox"] {
  display: inline-block;
  width: 16px;
  margin: 0 10px 0 0;
  position: relative;
  top: 2px;
}
button {
  display: block;
  margin: 25px auto;
  width: 30%;
  height: 30px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}
.feedback-error {
  color: red;
  margin-top: 10px; /* Adjust the spacing as needed */
}
</style>
