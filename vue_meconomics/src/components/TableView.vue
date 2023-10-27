<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th
            @click="toggleSelectAll"
            :class="{ 'icon-clickable': true }"
            class="custom-checkbox"
          >
            <i
              v-if="areAllItemsSelected"
              class="fa-duotone fa-square-check"
              style="
                --fa-primary-color: #ffffff;
                --fa-secondary-color: #75af4a;
                --fa-secondary-opacity: 1;
              "
            ></i>
            <i
              v-else
              class="fa-duotone fa-square-check"
              style="--fa-primary-color: #ffffff; --fa-secondary-color: #ababab"
            ></i>
          </th>
          <th
            v-for="(column, index) in visibleColumns"
            :key="index"
            class="custom-th"
          >
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
                  class="search table-search"
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
        <tr v-for="item in filteredItems" :key="item.id">
          <td
            @click="toggleSelectItem(item)"
            :class="{ 'icon-clickable': true }"
            class="custom-checkbox"
          >
            <i
              v-if="isItemSelected(item)"
              class="fa-duotone fa-square-check"
              style="
                --fa-primary-color: #ffffff;
                --fa-secondary-color: #75af4a;
                --fa-secondary-opacity: 1;
              "
            ></i>
            <i
              v-else
              class="fa-duotone fa-square-check"
              style="--fa-primary-color: #ffffff; --fa-secondary-color: #ababab"
            ></i>
          </td>
          <td
            v-for="(column, colIndex) in visibleColumns"
            :key="colIndex"
            class="custom-td"
          >
            <div v-if="typeof item[column.field] === 'boolean'">
              <!-- The data is a boolean, so we display a checkmark or an 'x' based on the value -->
              <span v-if="item[column.field]"
                ><i class="fa-solid fa-check" style="color: #28b701"></i
              ></span>
              <!-- true -->
              <span v-else
                ><i class="fa-solid fa-xmark" style="color: #ff0000"></i
              ></span>
              <!-- false -->
            </div>
            <router-link
              v-else
              :to="{
                name: detailsRouteName,
                params: { id: item.id },
              }"
              class="item-link"
            >
              {{ item[column.field] }}
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filteredItems: [...this.items],
      activeSearchColumnIndex: null,
      selectedItems: [],
    };
  },
  props: {
    visibleColumns: Array,
    items: Array,
    detailsRouteName: String,
  },
  computed: {
    areAllItemsSelected() {
      return (
        this.selectedItems.length === this.filteredItems.length &&
        this.filteredItems.length > 0
      );
    },
  },
  methods: {
    filterData() {
      const searchColumn = this.visibleColumns[this.activeSearchColumnIndex];
      const searchTerm = searchColumn.search.toLowerCase();

      this.filteredItems = this.items.filter((item) =>
        String(item[searchColumn.field]).toLowerCase().startsWith(searchTerm)
      );
    },
    toggleSort(column) {
      column.sortDirection = column.sortDirection === "asc" ? "desc" : "asc";
      this.sortData(column);
      this.filteredItems = [...this.filteredItems];
    },
    sortData(sortableColumn) {
      sortableColumn =
        sortableColumn || this.columns.find((column) => column.sortDirection);
      if (!sortableColumn) return;

      this.filteredItems.sort((a, b) => {
        const field = sortableColumn.field;
        const valA = a[field];
        const valB = b[field];

        if (!isNaN(valA) && !isNaN(valB)) {
          const sortResult =
            sortableColumn.sortDirection === "asc" ? valA - valB : valB - valA;
          return sortResult;
        }

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
      this.filteredItems = [...this.items];
    },
    activateSearch(index) {
      if (this.activeSearchColumnIndex === index) {
        this.deactivateSearch();
        return;
      }

      this.activeSearchColumnIndex = index;
      this.$nextTick(() => {
        setTimeout(() => {
          const refArray = this.$refs["searchInput-" + index];
          if (refArray && refArray[0]) {
            refArray[0].focus();
            document.addEventListener("click", this.handleDocumentClick);
          } else {
            console.warn("Reference to search input not found");
          }
        }, 550);
      });
    },
    deactivateSearch() {
      this.activeSearchColumnIndex = null;
      this.filteredItems = [...this.items];
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
      document.removeEventListener("click", this.handleDocumentClick);
    },
    clearSearchInput() {
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
    },
    handleDocumentClick(event) {
      const isOutsideInput =
        event.target !== this.$el.querySelector(".search") &&
        !event.target.closest(".search");
      const isOutsideTableBody =
        event.target !== this.$refs.tbodyElement &&
        !event.target.closest(".table-container tbody");

      if (isOutsideInput && isOutsideTableBody) {
        this.deactivateSearch();
      }
    },
    toggleSelectAll() {
      if (this.areAllItemsSelected) {
        this.selectedItems = [];
      } else {
        this.selectedItems = this.filteredItems.map((item) => item.id);
      }
    },
    toggleSelectItem(item) {
      const index = this.selectedItems.indexOf(item.id);
      if (index > -1) {
        // Item is already selected, so we remove it
        this.selectedItems.splice(index, 1);
      } else {
        // Item is not selected, so we add it
        this.selectedItems.push(item.id);
      }
    },
    isItemSelected(item) {
      return this.selectedItems.includes(item.id);
    },
  },
  watch: {
    items(newItems) {
      this.filteredItems = newItems;
    },
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

.custom-td,
.custom-th {
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
.custom-checkbox {
  width: 25px;
  cursor: pointer;
}
</style>
