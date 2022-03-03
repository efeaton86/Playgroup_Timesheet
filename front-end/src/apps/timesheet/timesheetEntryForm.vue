<template>
  <section v-if="getUserActiveDay">
    test
  </section>




</template>

<script>
import { mapGetters, mapState } from 'vuex'


export default {
  name: "timesheetEntryForm",

  computed: {
    ...mapState(['userActiveDay']),
    ...mapGetters(["getUserActiveDay", "getUserActiveDayStatus"]),
  },

  methods: {
  }
}

</script>

<style scoped>

</style>
