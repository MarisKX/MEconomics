<template>
  <div v-if="isVisible" class="modal">
    <div class="modal-content">
      <span class="close-button" @click="closeModal">x</span>
      <h3>Add New Company</h3>
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
        <button class="submit-modal-btn" type="submit">Save</button>
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
