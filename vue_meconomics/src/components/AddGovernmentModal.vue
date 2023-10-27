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
      <h3>Add New Government Institution</h3>
      <form @submit.prevent="addGovernmentInstitution">
        <div>
          <label><span class="required">*</span>Name:</label>
          <input
            type="text"
            id="name"
            v-model="newGovernmentInstitution.name"
            placeholder="Name of the Government Institution"
            required
          />
        </div>
        <div>
          <label for="established">Established Date:</label>
          <input
            type="date"
            id="established"
            v-model="newGovernmentInstitution.established"
            required
          />
        </div>
        <div>
          <label>Authority:</label>
          <input
            type="text"
            id="authority"
            v-model="newGovernmentInstitution.authority"
            placeholder="Contrywide, Citywide etc"
          />
        </div>
        <div>
          <label>Street Adress 1:</label>
          <input
            type="text"
            id="street_adress_1"
            v-model="newGovernmentInstitution.street_adress_1"
            placeholder="House Number, Appartment Number etc."
          />
        </div>
        <div>
          <label>Street Adress 2:</label>
          <input
            type="text"
            id="street_adress_2"
            v-model="newGovernmentInstitution.street_adress_2"
            placeholder="Street, Road, Name"
            required
          />
        </div>
        <div>
          <label>City:</label>
          <input
            type="text"
            id="city"
            v-model="newGovernmentInstitution.city"
            placeholder="City, Town"
            required
          />
        </div>
        <div>
          <label>Postal Code:</label>
          <input
            type="text"
            id="post_code"
            v-model="newGovernmentInstitution.post_code"
            placeholder="Postal Code / Index"
            required
          />
        </div>
        <div>
          <label>Country:</label>
          <input
            type="text"
            id="country"
            v-model="newGovernmentInstitution.country"
            placeholder="Country"
            required
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
      newGovernmentInstitution: {
        name: "",
        established: "",
        authority: "",
        street_adress_1: "",
        street_adress_2: "",
        city: "",
        post_code: "",
        country: "",
      },
    };
  },
  created() {
    this.resetForm();
  },
  computed: {
    dateToday() {
      const dateToday = this.$store.state.dateToday;
      console.log(dateToday);
      return dateToday;
    },
    dateForInputField() {
      const [year, month, day] = this.dateToday.split("-");
      return `${day}-${month}-${year}`;
    },
  },
  methods: {
    resetForm() {
      this.newGovernmentInstitution = {
        name: "",
        established: this.dateForInputField,
        authority: "",
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
    addGovernmentInstitution() {
      axios
        .post(
          "https://meconomics.com:8000/api/company/governmentinstitutions/",
          this.newGovernmentInstitution,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        )
        .then((response) => {
          this.$emit("governmentInstitutionAdded", response.data);
          this.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
