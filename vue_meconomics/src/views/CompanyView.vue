<template>
  <div class="companies">
    <TopNav />
    <div class="main">
      <div
        class="add-sign"
        @mouseover="showTooltip = true"
        @mouseleave="showTooltip = false"
        @click="toggleModal"
      >
        <i class="fas fa-plus"></i>
      </div>
      <AddCompanyModal
        :isVisible="showModal"
        @close="toggleModal"
        @companyAdded="handleCompanyAdded"
      ></AddCompanyModal>
      <div v-if="showTooltip" class="tooltip">Add New Company</div>
      <TableView
        :visibleColumns="visibleColumns"
        :items="companies"
        :detailsRouteName="'company-details'"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import AddCompanyModal from "../components/AddCompanyModal.vue";
import TableView from "../components/TableView.vue";
export default {
  name: "CompanyView",
  components: {
    TopNav,
    AddCompanyModal,
    TableView,
  },
  data() {
    return {
      columns: [],
      companies: [],
      showTooltip: false,
      showModal: false,
    };
  },
  computed: {
    visibleColumns() {
      return this.columns.slice(1);
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "https://meconomics.com:8000/api/company/companies/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        if (response.data.length > 0) {
          const firstCompany = response.data[0];
          this.columns = Object.keys(firstCompany).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
            search: "",
            sortDirection: "asc",
          }));
        }

        this.companies = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
    handleCompanyAdded(company) {
      this.companies.push(company);
    },
  },
};
</script>
