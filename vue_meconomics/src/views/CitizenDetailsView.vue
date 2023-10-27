<template>
  <div class="home">
    <TopNav />
    <hr class="top-data-seperator" />
    <DataRow />
    <hr class="top-data-seperator" />
  </div>
</template>

<script>
import TopNav from "../components/TopNav.vue";
import DataRow from "../components/DataRow.vue";
export default {
  name: "CitizenDetailsView",
  components: {
    TopNav,
    DataRow,
  },
};
</script>
