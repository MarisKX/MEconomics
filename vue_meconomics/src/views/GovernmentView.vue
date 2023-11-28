<template>
  <div class="government">
    <TopNav />
    <hr class="top-data-seperator" />
    <DataRow />
    <hr class="top-data-seperator" />
    <div class="main">
      <div
        class="add-sign"
        @mouseover="showTooltip = true"
        @mouseleave="showTooltip = false"
        @click="toggleModal"
      >
        <div v-if="showTooltip">Add New Government Institutution</div>
        <i v-else class="fas fa-plus"></i>
      </div>
      <AddGovernmentModal
        :isVisible="showModal"
        @close="toggleModal"
        @governmentInstitutionAdded="handleGovernmentInstitutionAdded"
        :governmentInstitutions="governmentInstitutions"
      ></AddGovernmentModal>
      <TableView
        :visibleColumns="visibleColumns"
        :items="governmentInstitutions"
        :detailsRouteName="'government-details'"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import DataRow from "../components/DataRow.vue";
import AddGovernmentModal from "../components/AddGovernmentModal.vue";
import TableView from "../components/TableView.vue";
export default {
  name: "GovernmentView",
  components: {
    TopNav,
    AddGovernmentModal,
    TableView,
    DataRow,
  },
  data() {
    return {
      columns: [],
      governmentInstitutions: [],
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
          "https://meconomics.com:8000/api/company/governmentinstitutions/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        if (response.data.length > 0) {
          const firstGovernmentInstitution = response.data[0];
          this.columns = Object.keys(firstGovernmentInstitution).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
            search: "",
            sortDirection: "asc",
          }));
        }

        this.governmentInstitutions = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
    async handleGovernmentInstitutionAdded(governmentInstitution) {
      this.governmentInstitutions.unshift(governmentInstitution);
      await this.fetchData();
    },
  },
};
</script>

<style scoped>
.tooltip {
  left: 240px;
}
</style>
