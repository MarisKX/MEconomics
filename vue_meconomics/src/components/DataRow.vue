<template>
  <div class="container d-flex align-items-center">
    <div class="row w-100">
      <div class="col-12 col-xl-4">{{ formattedDate }}</div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    formattedDate() {
      const [day, month, year] = this.dateToday.split("-");
      let dateObj = new Date(year, month - 1, day);
      let options = { year: "numeric", month: "long", day: "2-digit" };
      return dateObj.toLocaleDateString("en-NL", options);
    },
    dateToday() {
      const dateToday = this.$store.state.dateToday;
      return dateToday;
    },
  },
};
</script>
