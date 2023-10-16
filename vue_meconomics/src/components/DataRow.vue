<template>
  <div class="container d-flex align-items-center">
    <div class="row w-100">{{ formattedDate }}</div>
  </div>
</template>

<script>
export default {
  computed: {
    formattedDate() {
      let dateObj = new Date(this.dateToday);
      let options = { year: "numeric", month: "short", day: "numeric" };
      return dateObj.toLocaleDateString("en-US", options);
    },
    dateToday() {
      const dateToday = this.$store.state.dateToday;
      return dateToday;
    },
  },
};
</script>
