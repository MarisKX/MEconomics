<template>
  <div class="citizens">
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
      <AddCitizenModal
        :isVisible="showModal"
        @close="toggleModal"
        @citizenAdded="handleCitizenAdded"
      ></AddCitizenModal>
      <div v-if="showTooltip" class="tooltip">Add New Citizen</div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th v-for="(column, index) in visibleColumns" :key="index">
                <div class="header-content">
                  <transition name="fade" mode="out-in">
                    <div
                      class="label-sort"
                      v-if="index !== activeSearchColumnIndex"
                      key="label-sort"
                    >
                      <div
                        class="label"
                        v-show="column.sortable"
                        @click="activateSearch(index)"
                      >
                        {{ column.label }}
                      </div>
                      <div
                        class="sort"
                        v-show="column.sortable"
                        @click="toggleSort(column)"
                      >
                        <span
                          class="up-arrow"
                          :class="{ active: column.sortDirection === 'asc' }"
                          >▲</span
                        >
                        <span
                          class="down-arrow"
                          :class="{ active: column.sortDirection === 'desc' }"
                          >▼</span
                        >
                      </div>
                    </div>
                    <input
                      v-else
                      class="search"
                      v-model="column.search"
                      @input="filterData"
                      key="search-input"
                      :ref="'searchInput-' + index"
                    />
                  </transition>
                </div>
              </th>
            </tr>
          </thead>
          <tbody ref="tbodyElement">
            <tr v-for="citizen in filteredCitizens" :key="citizen.id">
              <td v-for="(column, colIndex) in visibleColumns" :key="colIndex">
                <router-link
                  :to="{
                    name: 'citizens-details',
                    params: { id: citizen.id },
                  }"
                  class="citizen-link"
                >
                  <template
                    v-if="column.field !== 'color' && column.field !== 'user'"
                  >
                    {{ citizen[column.field] }}
                  </template>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import AddCitizenModal from "../components/AddCitizenModal.vue";
export default {
  name: "CitizenView",
  components: {
    TopNav,
    AddCitizenModal,
  },
  data() {
    return {
      columns: [],
      citizens: [],
      filteredCitizens: [],
      activeSearchColumnIndex: null,
      showTooltip: false,
      showModal: false,
    };
  },
  computed: {
    filteredData() {
      return this.citizens;
    },
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
        this.filteredCitizens = [...this.citizens];
        this.sortData();
      } catch (error) {
        console.error(error);
      }
    },
    toggleSort(column) {
      column.sortDirection = column.sortDirection === "asc" ? "desc" : "asc";
      this.sortData(column);
      this.filteredCitizens = [...this.citizens];
    },
    sortData(sortableColumn) {
      sortableColumn =
        sortableColumn || this.columns.find((column) => column.sortDirection);
      if (!sortableColumn) return;

      this.citizens.sort((a, b) => {
        const field = sortableColumn.field;
        const valA = a[field];
        const valB = b[field];

        if (!isNaN(valA) && !isNaN(valB)) {
          const sortResult =
            sortableColumn.sortDirection === "asc" ? valA - valB : valB - valA;
          return sortResult;
        }

        // Handle null or undefined values
        if (!valA) return sortableColumn.sortDirection === "asc" ? 1 : -1;
        if (!valB) return sortableColumn.sortDirection === "asc" ? -1 : 1;

        const regex = /[^a-zA-Z0-9]/g;
        const strA = valA.replace(regex, "").toUpperCase();
        const strB = valB.replace(regex, "").toUpperCase();

        const stringSortResult =
          sortableColumn.sortDirection === "asc"
            ? strA.localeCompare(strB)
            : strB.localeCompare(strA);
        return stringSortResult;
      });
      this.filteredCitizens = [...this.citizens];
    },
    activateSearch(index) {
      if (this.activeSearchColumnIndex !== null) {
        this.deactivateSearch();
      }
      this.activeSearchColumnIndex = index;
      this.$nextTick(() => {
        setTimeout(() => {
          this.$el.querySelector(".search").focus();
          // Add a click event listener to the document
          document.addEventListener("click", this.handleDocumentClick);
        }, 550);
      });
    },
    clearSearchInput() {
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
    },
    deactivateSearch() {
      this.activeSearchColumnIndex = null;
      this.filteredCitizens = [...this.citizens];
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
      // Remove the click event listener from the document
      document.removeEventListener("click", this.handleDocumentClick);
    },
    filterData() {
      const searchColumn = this.visibleColumns[this.activeSearchColumnIndex];
      const searchTerm = searchColumn.search.toLowerCase();
      this.filteredCitizens = this.citizens.filter((citizen) =>
        String(citizen[searchColumn.field]).toLowerCase().startsWith(searchTerm)
      );
    },
    handleDocumentClick(event) {
      // Check if the click event target is outside both the input and the table body
      const isOutsideInput =
        event.target !== this.$el.querySelector(".search") &&
        !event.target.closest(".search"); // Check for input and its descendants
      const isOutsideTableBody =
        event.target !== this.$refs.tbodyElement &&
        !event.target.closest(".table-container tbody"); // Check for tbody and its descendants

      if (isOutsideInput && isOutsideTableBody) {
        // Deactivate the search when clicking outside
        this.deactivateSearch();
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
    handleCitizenAdded(citizen) {
      this.citizens.push(citizen);
      this.filteredCitizens = [...this.citizens];
      this.sortData();
    },
  },
  watch: {
    activeSearchColumnIndex: {
      handler(newValue) {
        if (newValue !== null) {
          this.$nextTick(() => {
            setTimeout(() => {
              const refArray = this.$refs["searchInput-" + newValue];
              if (refArray && refArray[0]) {
                refArray[0].focus();
              } else {
                console.warn("Reference to search input not found");
              }
            }, 550);
          });
        }
      },
      immediate: false,
    },
  },
};
</script>

<style scoped>
.label-sort {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  flex-grow: 1;
}

.sort {
  display: flex;
  flex-direction: column;
  align-items: center;
}

td,
th {
  min-width: 150px;
  padding: 5px 5px;
}
.fade-enter-active {
  transition: opacity 0.2s ease-in 0.2s; /* ease-in and delay */
}
.fade-leave-active {
  transition: opacity 0.2s ease-out;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
input {
  width: 120px;
}
</style>
