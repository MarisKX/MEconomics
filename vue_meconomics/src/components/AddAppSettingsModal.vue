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
      <h3>Add New App Settings</h3>
      <form @submit.prevent="addCitizen">
        <div>
          <label for="established">Valid From:</label>
          <input
            type="date"
            id="valid_from"
            v-model="newAppSettings.valid_from"
            required
          />
        </div>
        <div>
          <label for="established">Valid Till:</label>
          <input
            type="date"
            id="valid_till"
            v-model="newAppSettings.valid_till"
            required
          />
        </div>
        <div>
          <label>Actions per day:</label>
          <input
            type="text"
            id="actions_per_day"
            v-model="newAppSettings.actions_per_day"
            placeholder="Allowed actions per day"
          />
        </div>
        <div>
          <label>VSAOI From Employer:</label>
          <input
            type="text"
            id="vsaoi_dn"
            v-model="newAppSettings.vsaoi_dn"
            placeholder="VSAOI From Employer"
            required
          />
        </div>
        <div>
          <label>IIN Rate:</label>
          <input
            type="text"
            id="iin_rate"
            v-model="newAppSettings.iin_rate"
            placeholder="IIN Rate"
            required
          />
        </div>
        <div>
          <label>IIN Exempt value:</label>
          <input
            type="text"
            id="no_iin_level"
            v-model="newAppSettings.no_iin_level"
            placeholder="Value till which IN is not taxable"
            required
          />
        </div>
        <div>
          <label>UIN Rate:</label>
          <input
            type="text"
            id="uin_rate"
            v-model="newAppSettings.uin_rate"
            placeholder="UIN Rate"
            required
          />
        </div>
        <div>
          <label>Environment Base Tax:</label>
          <input
            type="text"
            id="enviroment_tax_base"
            v-model="newAppSettings.enviroment_tax_base"
            placeholder="Environment Base Tax"
            required
          />
        </div>
        <div>
          <label>BTW:</label>
          <input
            type="text"
            id="btw"
            v-model="newAppSettings.btw"
            placeholder="BTW Rate"
            required
          />
        </div>
        <div>
          <label>VSAOI Employee:</label>
          <input
            type="text"
            id="vsaoi_dd"
            v-model="newAppSettings.vsaoi_dd"
            placeholder="VSAOI From Employee"
            required
          />
        </div>
        <div>
          <label>Base Cadaster Value:</label>
          <input
            type="text"
            id="base_cadastre_value"
            v-model="newAppSettings.base_cadastre_value"
            placeholder="Base Cadaster Value"
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
      newAppSettings: {
        valid_from: "",
        valid_till: "",
        actions_per_day: "",
        vsaoi_dn: "",
        iin_rate: "",
        no_iin_level: "",
        uin_rate: "",
        enviroment_tax_base: "",
        btw: "",
        vsaoi_dd: "",
        base_cadastre_value: "",
        valid: "true",
      },
    };
  },
  methods: {
    resetForm() {
      this.newCitizen = {
        valid_from: "",
        valid_till: "",
        actions_per_day: "",
        vsaoi_dn: "",
        iin_rate: "",
        no_iin_level: "",
        uin_rate: "",
        enviroment_tax_base: "",
        btw: "",
        vsaoi_dd: "",
        base_cadastre_value: "",
        valid: "true",
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
          "https://meconomics.com:8000/api/user/app-settings/",
          this.newAppSettings,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        )
        .then((response) => {
          this.$emit("settingsAdded", response.data);
          this.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
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
