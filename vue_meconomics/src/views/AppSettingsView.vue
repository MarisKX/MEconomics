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
      <AddAppSettingsModal
        :isVisible="showModal"
        @close="toggleModal"
        @settingsAdded="handleAppSettingsAdded"
      ></AddAppSettingsModal>
      <div v-if="showTooltip" class="tooltip">Add New App Settings</div>
      <TableView
        :visibleColumns="visibleColumns"
        :items="appSettings"
        :detailsRouteName="'appsettings-details'"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import DataRow from "../components/DataRow.vue";
import AddAppSettingsModal from "../components/AddAppSettingsModal.vue";
import TableView from "../components/TableView.vue";
export default {
  name: "AppSettingsView",
  components: {
    TopNav,
    AddAppSettingsModal,
    TableView,
    DataRow,
  },
  data() {
    return {
      columns: [],
      appSettings: [],
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
          "https://meconomics.com:8000/api/user/app-settings/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        if (response.data.length > 0) {
          const firstAppSettings = response.data[0];
          this.columns = Object.keys(firstAppSettings).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
            search: "",
            sortDirection: "asc",
          }));
        }

        this.appSettings = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
    async handleAppSettingsAdded(appSetting) {
      this.appSettings.unshift(appSetting);
      await this.fetchData();
    },
  },
};
</script>
