<template>
  <div v-if="isVisible" class="modal">
    <div class="modal-content">
      <span class="close-button" @click="closeModal">x</span>
      <h3>Add New Citizen</h3>
      <form @submit.prevent="addCitizen">
        <div>
          <label><span class="required">*</span>First Name:</label>
          <input
            type="text"
            id="first_name_display"
            v-model="newCitizen.first_name"
            placeholder="First Name (Names)"
            required
          />
        </div>
        <div>
          <label><span class="required">*</span>Last Name:</label>
          <input
            type="text"
            id="last_name_display"
            v-model="newCitizen.last_name"
            placeholder="Last Name"
            required
          />
        </div>
        <div>
          <label>Street Adress 1:</label>
          <input
            type="text"
            id="street_adress_1"
            v-model="newCitizen.street_adress_1"
            placeholder="House Number, Appartment Number etc."
          />
        </div>
        <div>
          <label>Street Adress 2:</label>
          <input
            type="text"
            id="street_adress_2"
            v-model="newCitizen.street_adress_2"
            placeholder="Street, Road, Name"
          />
        </div>
        <div>
          <label>City:</label>
          <input
            type="text"
            id="city"
            v-model="newCitizen.city"
            placeholder="City, Town"
          />
        </div>
        <div>
          <label>Postal Code:</label>
          <input
            type="text"
            id="post_code"
            v-model="newCitizen.post_code"
            placeholder="Postal Code / Index"
          />
        </div>
        <div>
          <label>Country:</label>
          <input
            type="text"
            id="country"
            v-model="newCitizen.country"
            placeholder="Country"
          />
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["isVisible"],
  data() {
    return {
      newCitizen: {
        first_name: "",
        last_name: "",
      },
    };
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    addCitizen() {
      // Post the new citizen to the API, then emit an event to the parent component to inform it
      axios
        .post(
          "https://meconomics.com:8000/api/citizen/citizens/",
          this.newCitizen,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        )
        .then((response) => {
          this.$emit("citizenAdded", response.data);
          this.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  max-width: 420px;
  margin: 30px auto;
  background: white;
  text-align: left;
  padding: 20px;
  border-radius: 10px;
  position: relative; /* for the close-button */
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}

label {
  color: #aaa;
  display: block;
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

button {
  display: block;
  margin: 25px auto;
  width: 30%;
  height: 30px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}
</style>
