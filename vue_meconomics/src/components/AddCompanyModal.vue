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
      <h3>Add New Company</h3>
      <form @submit.prevent="addCompany">
        <div>
          <label><span class="required">*</span>Company Name:</label>
          <input
            type="text"
            id="name"
            v-model="newCompany.name"
            placeholder="Name of the Company"
            required
          />
        </div>
        <div>
          <label for="established">Established Date:</label>
          <input
            type="date"
            id="established"
            v-model="newCompany.established"
            required
          />
        </div>
        <div>
          <label><span class="required">*</span>Invoice Prefix:</label>
          <input
            type="text"
            id="invoice_prefix"
            v-model="newCompany.invoice_prefix"
            placeholder="Letters to use in front of invoice/workorder"
            required
          />
        </div>
        <div class="select-wrapper">
          <label>Owner Type:</label>
          <select v-model="newCompany.owner_type" required>
            <option disabled value="">Please select one</option>
            <option value="0">Private</option>
            <option value="1">Company</option>
            <option value="2">Government Institution</option>
          </select>
          <i class="fas fa-chevron-down select-icon"></i>
        </div>
        <div class="select-wrapper" v-if="newCompany.owner_type === '1'">
          <label>Owner Company:</label>
          <select v-model="newCompany.owner_com" required>
            <option disabled value="">Please select one</option>
            <option
              v-for="company in companies"
              :key="company.id"
              :value="company.id"
            >
              {{ company.name }} - {{ company.registration_number }}
            </option>
          </select>
          <i class="fas fa-chevron-down select-icon"></i>
        </div>
        <div class="select-wrapper" v-if="newCompany.owner_type === '0'">
          <label>Owner Citizen:</label>
          <select v-model="newCompany.owner_pp" required>
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
        <div class="checkbox-out mt-3" @click="toggleWarehouse">
          <i
            v-if="newCompany.warehouse"
            class="fa-duotone fa-square-check fa-xl"
            style="
              --fa-primary-color: white;
              --fa-secondary-color: #3e5c20;
              --fa-secondary-opacity: 1;
            "
          ></i>
          <i
            v-else
            class="fa-duotone fa-square-xmark fa-xl"
            style="
              --fa-primary-color: #fafafa;
              --fa-secondary-color: #b30000;
              --fa-secondary-opacity: 1;
            "
          ></i>
          <label>Warehouse</label>
        </div>
        <div>
          <label>Street Adress 1:</label>
          <input
            type="text"
            id="street_adress_1"
            v-model="newCompany.street_adress_1"
            placeholder="House Number, Appartment Number etc."
          />
        </div>
        <div>
          <label>Street Adress 2:</label>
          <input
            type="text"
            id="street_adress_2"
            v-model="newCompany.street_adress_2"
            placeholder="Street, Road, Name"
          />
        </div>
        <div>
          <label>City:</label>
          <input
            type="text"
            id="city"
            v-model="newCompany.city"
            placeholder="City, Town"
          />
        </div>
        <div>
          <label>Postal Code:</label>
          <input
            type="text"
            id="post_code"
            v-model="newCompany.post_code"
            placeholder="Postal Code / Index"
          />
        </div>
        <div>
          <label>Country:</label>
          <input
            type="text"
            id="country"
            v-model="newCompany.country"
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
  components: {},
  props: ["isVisible", "companies"],
  data() {
    return {
      newCompany: {
        name: "",
        invoice_prefix: "",
        owner_type: "",
        warehouse: "true",
        street_adress_1: "",
        street_adress_2: "",
        city: "",
        post_code: "",
        country: "",
      },
      citizens: [],
    };
  },
  created() {
    this.fetchCitizens();
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
      this.newCompany = {
        name: "",
        established: this.dateForInputField,
        invoice_prefix: "",
        owner_type: "",
        warehouse: true,
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
    toggleWarehouse() {
      this.newCompany.warehouse = !this.newCompany.warehouse;
    },
    addCompany() {
      axios
        .post(
          "https://meconomics.com:8000/api/company/companies/",
          this.newCompany,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        )
        .then((response) => {
          this.$emit("companyAdded", response.data);
          this.resetForm();
          this.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
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
  },
};
</script>

<style>
.checkbox-out {
  height: 25px;
  width: 25px;
  display: flex;
  align-items: center;
  cursor: pointer;
}
.checkbox-out label {
  margin-left: 15px;
}
</style>
