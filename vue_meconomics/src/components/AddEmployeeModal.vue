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
      <h3>Add New Employee</h3>
      <form @submit.prevent="addEmployee">
        <div class="select-wrapper">
          <label><span class="required">*</span>Company: </label>
          <select v-model="newEmployee.company" required read-only>
            <option
              :key="companyDetails.id"
              :value="companyDetails.id"
              selected
            >
              {{ companyDetails.name }} -
              {{ companyDetails.registration_number }}
            </option>
          </select>
          <i class="fas fa-chevron-down select-icon"></i>
        </div>
        <div class="select-wrapper">
          <label>Citizen:</label>
          <select v-model="newEmployee.name" required>
            <option disabled value="">Please select one</option>
            <option
              v-for="citizen in citizens"
              :key="citizen.id"
              :value="citizen.id"
            >
              {{ citizen.full_name }} - {{ citizen.bsn_number }}
            </option>
          </select>
          <i class="fas fa-chevron-down select-icon"></i>
        </div>
        <div>
          <label>Role:</label>
          <input
            type="text"
            id="role"
            v-model="newEmployee.role"
            placeholder="Role"
          />
        </div>
        <div>
          <label>Brutto Salary:</label>
          <input
            type="text"
            id="salary_brutto"
            v-model="newEmployee.salary_brutto"
            placeholder="Salary (Brutto)"
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
  props: {
    isVisible: Boolean,
    companyDetails: Object,
  },
  data() {
    return {
      newEmployee: {
        company: "",
        name: "",
        role: "",
        salary_brutto: "",
      },
      citizens: [],
    };
  },
  mounted() {
    this.newEmployee.company = this.companyDetails.id;
  },
  created() {
    this.fetchCitizens();
    this.resetForm();
  },
  methods: {
    resetForm() {
      this.newEmployee = {
        company: this.companyDetails.id,
        name: "",
        role: "",
        salary_brutto: "",
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
    async fetchCitizens() {
      try {
        const response = await axios.get(
          "https://meconomics.com:8000/api/citizen/citizens/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );
        this.citizens = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    addEmployee() {
      axios
        .post(
          "https://meconomics.com:8000/api/company/company-employees/",
          this.newEmployee,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        )
        .then((response) => {
          this.$emit("employeeAdded", response.data);
          this.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
