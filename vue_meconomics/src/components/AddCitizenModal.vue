<template>
  <div v-if="isVisible" class="modal" @click="closeModalOnBackdrop">
    <div class="modal-content">
      <i
        class="fa-duotone fa-square-xmark fa-xl close-button"
        @click="closeModal"
        style="
          --fa-primary-color: #fafafa;
          --fa-secondary-color: #b30000;
          --fa-secondary-opacity: 1;
        "
      ></i>
      <h3>Add New Citizen</h3>
      <form @submit.prevent="addCitizen">
        <div>
          <label><span class="required">*</span>First Name:</label>
          <input
            type="text"
            id="first_name"
            v-model="newCitizen.first_name"
            placeholder="First Name (Names)"
            required
          />
        </div>
        <div>
          <label><span class="required">*</span>Last Name:</label>
          <input
            type="text"
            id="last_name"
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
        street_adress_1: "",
        street_adress_2: "",
        city: "",
        post_code: "",
        country: "",
      },
    };
  },
  methods: {
    resetForm() {
      this.newCitizen = {
        first_name: "",
        last_name: "",
        street_adress_1: "",
        street_adress_2: "",
        city: "",
        post_code: "",
        country: "",
      };
    },
    closeModalOnBackdrop(event) {
      if (event.target === event.currentTarget) {
        this.resetForm();
        this.$emit("close");
      }
    },
    closeModal() {
      this.resetForm();
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
