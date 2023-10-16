<template>
  <div class="citizens">
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
        <i class="fas fa-plus"></i>
      </div>
      <AddCitizenModal
        :isVisible="showModal"
        @close="toggleModal"
        @citizenAdded="handleCitizenAdded"
      ></AddCitizenModal>
      <div v-if="showTooltip" class="tooltip">Add New Citizen</div>
      <TableView
        :visibleColumns="visibleColumns"
        :items="citizens"
        :detailsRouteName="'citizen-details'"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import DataRow from "../components/DataRow.vue";
import AddCitizenModal from "../components/AddCitizenModal.vue";
import TableView from "../components/TableView.vue";
export default {
  name: "CitizenView",
  components: {
    TopNav,
    AddCitizenModal,
    TableView,
    DataRow,
  },
  data() {
    return {
      columns: [],
      citizens: [],
      showTooltip: false,
      showModal: false,
    };
  },
  computed: {
    visibleColumns() {
      return this.columns.slice(2);
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "https://meconomics.com:8000/api/citizen/citizens/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        if (response.data.length > 0) {
          const firstCitizen = response.data[0];
          this.columns = Object.keys(firstCitizen).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
            search: "",
            sortDirection: "asc",
          }));
        }

        this.citizens = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
    handleCitizenAdded(citizen) {
      this.citizens.push(citizen);
    },
  },
};
</script>
