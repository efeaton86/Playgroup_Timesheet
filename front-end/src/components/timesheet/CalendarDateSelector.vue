/* eslint-disable */
<template>
  <div class="calendar-date-selector">
    <span @click="selectPrevious">&lt</span>
    <span @click="selectCurrent">Today</span>
    <span @click="selectNext">&gt</span>
  </div>
</template>

<script>
import dayjs from "dayjs"

export default {
  name: "CalendarDateSelector",

  props: {
    currentDate: {
      type: String,
      required: true
    },
    selectedDate: {
      type: Object,
      required: true
    }
  },

  methods: {
    selectPrevious() {
      let newSelectedDate = dayjs(this.selectedDate).subtract(1, 'month')
      var date_obj = {
        'month': newSelectedDate.month(),
        'year': newSelectedDate.year()
      }
      // console.log('selectPrevious',date_obj)
      this.$emit('dateSelected', newSelectedDate)
      this.$store.dispatch('getUserTimeEntries', date_obj)
    },

    selectCurrent() {
      let newSelectedDate = dayjs(this.currentDate)
      var date_obj = {
        'month': newSelectedDate.month(),
        'year': newSelectedDate.year()
      }
      this.$emit('dateSelected', newSelectedDate)
      this.$store.dispatch('getUserTimeEntries', date_obj)
    },

    selectNext() {
      let newSelectedDate = dayjs(this.selectedDate).add(1, 'month')
      var date_obj = {
        'month': newSelectedDate.month(),
        'year': newSelectedDate.year()
      }
      this.$emit('dateSelected', newSelectedDate)
      this.$store.dispatch('getUserTimeEntries', date_obj)

    }
  }
}
</script>

<style scoped>
.calendar-date-selector {
  display: flex;
  justify-content: space-between;
  width: 80px;
  color: dimgrey;
}

.calendar-date-selector > * {
  cursor: pointer;
  user-select: none;
}
</style>
