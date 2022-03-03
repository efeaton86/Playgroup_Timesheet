<template>
  <ol class="day-of-week">
    <li
      v-for="weekday in weekdays"
      :key="weekday"
    >
      {{ weekday }}
    </li>
  </ol>
</template>

<script>
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export default {
  name: 'CalendarWeekdays',

  computed: {
    weekdays() {
      return WEEKDAYS
    }
  }
}
</script>

<style scoped>

.day-of-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  border-left: 1px solid #cfd7e3;
  border-right: 1px solid #cfd7e3;
}

/*.day-of-week > * {*/
/*  text-align: right;*/
/*  padding-right: 5px;*/
/*}*/

.day-of-week {
  color: var(--grey-800);
  font-size: 18px;
  background-color: #fff;
  padding-bottom: 5px;
  padding-top: 10px;
}

.day-of-week,
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}
</style>
