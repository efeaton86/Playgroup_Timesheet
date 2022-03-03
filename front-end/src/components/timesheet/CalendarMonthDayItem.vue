<template>
  <li
    class="calendar-day"
    :class="{
      'calendar-day--not-current': !day.isCurrentMonth,
      'calendar-day--today': isToday
    }"
    v-bind:id="label"

    @click="navigateToDayDetailView(day)"

  >
    <span>{{ label }}</span>
    <br>
    <div :class="timeEntryCurrentMonth(label, day)"></div>
  </li>
</template>

<script>
import dayjs from 'dayjs'

import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'CalendarMonthDayItem',

  props: {
    day: {
      type: Object,
      required: true
    },
    isCurrentMonth: {
      type: Boolean,
      default: false
    },
    isToday: {
      type: Boolean,
      default: false
    },
  },

  methods: {
    //@click="setDay(day.date)"
    ...mapActions(["setDay"]),

    timeEntryCurrentMonth(label, day) {
      var entry_set = this.$store.getters.daysWithTimeEntry
      if (entry_set.has(label) && day.isCurrentMonth) {
        return 'time_entry'
      } else {
        return ''
      }
    },

    // this should only fire if the user has an entry for that day
    // it is currently firing for all users and showing every
    // users entries on a single day
    navigateToDayDetailView (day) {
      //day is the day number integer
      const year = dayjs(day.date).format('YYYY')
      const month = dayjs(day.date).format('M')
      const dayOfMonth = dayjs(day.date).format('D')

      // console.log('inside navigate')
      // console.log(year, month, dayOfMonth)
      //link is 'user_entries/<int:pk>/'

      document.location = `user_entries/${year}/${month}/${dayOfMonth}/`
    }
  },

  computed: {
    ...mapGetters(['daysWithTimeEntry']),
    label() {
      return Number(dayjs(this.day.date).format("D"))
    },
  }
}

</script>

<style scoped>
/*body {*/
/*  font-family: sans-serif;*/
/*  font-weight: 100;*/
/*  --grey-100: #e4e9f0;*/
/*  --grey-200: #cfd7e3;*/
/*  --grey-300: #b5c0cd;*/
/*  --grey-800: #3e4e63;*/
/*  --grid-gap: 1px;*/
/*  --day-label-size: 20px;*/
/*}*/

.calendar-day {
  position: relative;
  min-height: 100px;
  font-size: 16px;
  background-color: #fff;
  color: #3e4e63;
  padding: 5px;
  border: 1px solid #cfd7e3;

}

.calendar-day > span {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  right: 2px;
  width: var(--day-label-size);
  height: var(--day-label-size);
}

.calendar-day--not-current {
  background-color: #e4e9f0;
  color: #b5c0cd;
}

.calendar-day--today {
  padding-top: 4px;
}

.calendar-day--today > span {
  color: #fff;
  border-radius: 9999px;
  background-color: green;
}

.time_entry {
  background-color: green;
  height: 3px;
  width: 100%;
}

</style>
