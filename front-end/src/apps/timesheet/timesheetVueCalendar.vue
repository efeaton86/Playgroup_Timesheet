/* eslint-disable */
<template>
  <div class="row">
    <div class="col-8">
      <div class="calendar-month">
        <div class="calendar-month-header">
          <CalendarDateIndicator
            :selected-date="selectedDate"
            class="calendar-month-header-selected-month"
          />

          <CalendarDateSelector
            :current-date="today"
            :selected-date="selectedDate"
            @dateSelected="selectDate"
          />
        </div>

        <CalendarWeekdays />

        <ol class="days-grid">
          <CalendarMonthDayItem
            v-for="day in days"
            :key="day.date"
            :day="day"
            :is-today="day.date === today"
          />
        </ol>
      </div>
      </div>
    <div class="col-4">
      <timesheetUserEntryForm></timesheetUserEntryForm>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

import dayjs from "dayjs";
import weekday from "dayjs/plugin/weekday";
import weekOfYear from "dayjs/plugin/weekOfYear";
import CalendarMonthDayItem from "@/components/timesheet/CalendarMonthDayItem";
import CalendarDateIndicator from "@/components/timesheet/CalendarDateIndicator";
import CalendarDateSelector from "@/components/timesheet/CalendarDateSelector";
import CalendarWeekdays from "@/components/timesheet/CalendarWeekdays";
import timesheetUserEntryForm from "@/components/timesheet/timesheetUserEntryForm";

dayjs.extend(weekday);
dayjs.extend(weekOfYear);

export default {
  name: "timesheetVueCalendar",

  created(selectedDate) {
    // calculate today's date -api call to get this months data back
    var date_obj = {
      month: dayjs().month(),
      year: dayjs().year()
    }
    this.$store.dispatch('getUserTimeEntries', date_obj)
    // this.$store.dispatch('apiTest', date_obj)
  },

  mounted() {

  },

  components: {
    CalendarMonthDayItem,
    CalendarDateIndicator,
    CalendarDateSelector,
    CalendarWeekdays,
    timesheetUserEntryForm
  },

  data() {
    return {
      selectedDate: dayjs()
    };
  },

  computed: {
    days() {
      return [
        ...this.previousMonthDays,
        ...this.currentMonthDays,
        ...this.nextMonthDays
      ];

    },

    today() {
      return dayjs().format("YYYY-MM-DD");
    },

    month() {
      return Number(this.selectedDate.format("M"));
    },

    year() {
      return Number(this.selectedDate.format("YYYY"));
    },

    numberOfDaysInMonth() {
      return dayjs(this.selectedDate).daysInMonth();
    },

    currentMonthDays() {

      // console.log('currentMonthDays',[...Array(this.numberOfDaysInMonth)].map((day, index) => {
      //   return {
      //     date: dayjs(`${this.year}-${this.month}-${index + 1}`).format(
      //       "YYYY-MM-DD"),
      //     isCurrentMonth: true
      //   };
      // }))
      return [...Array(this.numberOfDaysInMonth)].map((day, index) => {
        return {
          date: dayjs(`${this.year}-${this.month}-${index + 1}`).format(
            "YYYY-MM-DD"),
          isCurrentMonth: true
        };
      });
    },

    previousMonthDays() {
      const firstDayOfTheMonthWeekday = this.getWeekday(
        //this const returns the positional index of the first day of the month
        // ie Sunday == 0, Monday ==1, indicating how many days from prior month need to be displayed
        this.currentMonthDays[0].date
      );
      // console.log('firstDayOfTheMonthWeekday', firstDayOfTheMonthWeekday)

      const previousMonth = dayjs(`${this.year}-${this.month}-01`).subtract(
        1,
        "month"
      );

      // Cover first day of the month being sunday (firstDayOfTheMonthWeekday === 0)
      const visibleNumberOfDaysFromPreviousMonth = firstDayOfTheMonthWeekday
        // ? firstDayOfTheMonthWeekday - 1
        // : 6;
      // console.log('visibleNumberOfDaysFromPreviousMonth', visibleNumberOfDaysFromPreviousMonth)


      const previousMonthLastMondayDayOfMonth = dayjs(
        // this const captures the day number of the last sunday of the prior month
        this.currentMonthDays[0].date
      )
        .subtract(visibleNumberOfDaysFromPreviousMonth, "day")
        .date();

      //previousMonthDays fn returns an array who's len is equal to the number of days
      // that must be shown from prior month.
      // constructs array in format of {date: "YYYY-MM-DD", isCurrentMonth: false}
      return [...Array(visibleNumberOfDaysFromPreviousMonth)].map(
        (day, index) => {
          return {
            date: dayjs(
              `${previousMonth.year()}-${previousMonth.month() + 1}-${previousMonthLastMondayDayOfMonth + index}`
            ).format("YYYY-MM-DD"),
            isCurrentMonth: false
          };
        }
      );
    },

    nextMonthDays() {
      const lastDayOfTheMonthWeekday = this.getWeekday(
        `${this.year}-${this.month}-${this.currentMonthDays.length}`
      );

      // while dayjs is zero index with months, need to add 2 so that
      //date selector will work in html
      const nextMonth = dayjs(`${this.year}-${this.month}-01`).add(2, "month");
      const visibleNumberOfDaysFromNextMonth = 6 - lastDayOfTheMonthWeekday
        // ? 6 - lastDayOfTheMonthWeekday
        // : lastDayOfTheMonthWeekday;
      ;

      // console.log([...Array(visibleNumberOfDaysFromNextMonth)].map((day, index) => {
      //   return {
      //     date: dayjs(
      //       `${nextMonth.year()}-${nextMonth.month()}-${index + 1}`
      //     ).format("YYYY-MM-DD"),
      //     isCurrentMonth: false
      //   }
      // }))

      return [...Array(visibleNumberOfDaysFromNextMonth)].map((day, index) => {
        return {
          date: dayjs(
            `${nextMonth.year()}-${nextMonth.month()}-${index + 1}`
          ).format("YYYY-MM-DD"),
          isCurrentMonth: false
        };
      });
    }
  },

  methods: {
    getWeekday(date) {
      // return weekday of a given date
      return dayjs(date).weekday();
    },

    selectDate(newSelectedDate) {
      this.selectedDate = newSelectedDate;
    }
  }
};

</script>

<style scoped>


body {
  font-family: sans-serif;
  font-weight: 100;
  --grey-100: #e4e9f0;
  --grey-200: #cfd7e3;
  --grey-300: #b5c0cd;
  --grey-800: #3e4e63;
  --grid-gap: 1px;
  --day-label-size: 20px;
}

ol,
li {
  padding: 0;
  margin: 0;
  list-style: none;
}

.calendar-month-header {
  display: flex;
  justify-content: space-between;
  background-color: #fff;
  padding: 10px;
  border-top: 1px solid #cfd7e3;
  border-left: 1px solid #cfd7e3;
  border-right: 1px solid #cfd7e3;
}

/*.calendar-month {*/
/*  position: relative;*/
/*  background-color: var(--grey-200);*/
/*  border: solid 1px var(--grey-300);*/
/*}*/

/*not needed here*/
/*.day-of-week {*/
/*  color: var(--grey-800);*/
/*  font-size: 18px;*/
/*  background-color: #fff;*/
/*  padding-bottom: 5px;*/
/*  padding-top: 10px;*/
/*}*/

.day-of-week,
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  /*border: 1px solid gray;*/

}

.day-of-week > * {
  text-align: right;
  padding-right: 5px;
}

.days-grid {
  height: 100%;
  position: relative;
  grid-column-gap: var(--grid-gap);
  grid-row-gap: var(--grid-gap);
  border-top: solid 1px #cfd7e3;
}

</style>
