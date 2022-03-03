<template>

  <section id="time_entry_form">
<!--    <form id="timeEntryForm" action="" method="POST">-->
      <div class="container d-flex flex-column p-0">
        <div class="mb-2">
          <div v-if="getDateRangePickerStatus">
            <label for="startDate" class="d-flex justify-content-between form-label">
                Start Date:
                  <div
                    class="d-inline-block pb-2"
                    @click="activateDateRangePicker"
                  >
                    <span class="pe-2">Select Single Day</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-range" viewBox="0 0 16 16">
                      <path d="M9 7a1 1 0 0 1 1-1h5v2h-5a1 1 0 0 1-1-1zM1 9h4a1 1 0 0 1 0 2H1V9z"/>
                      <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                    </svg>
                  </div>
            </label>
            <input v-model="date" name="startDate" id="startDate" type="date" class="form-control mb-3" placeholder="Date" required>
            <span style="color: red">{{ formErrors.date }}</span>

            <label for="endDate" class="d-flex justify-content-between form-label">End Date:</label>
            <input v-model="endDate" name="endDate" id="endDate" type="date" class="form-control" placeholder="Date" required>
            <span style="color: red">{{ formErrors.endDate}}</span>
          </div>

          <div v-else>
                <label for="date" class="d-flex justify-content-between form-label">
                Date:
                  <div
                    class="d-inline-block pb-3"
                    @click="activateDateRangePicker"
                  >
                    <span class="pe-2">Select date range</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-range" viewBox="0 0 16 16">
                      <path d="M9 7a1 1 0 0 1 1-1h5v2h-5a1 1 0 0 1-1-1zM1 9h4a1 1 0 0 1 0 2H1V9z"/>
                      <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                    </svg>
                  </div>
                </label>
              <input v-model="date" name="date" id="date" type="date" class="form-control" placeholder="Date"  required>
              <span style="color: red">{{ formErrors.date }}</span>
          </div>

        </div>

        <div class="mb-3">
          <label for="hours" class="d-flex justify-content-start form-label">Hours:</label>
          <input v-model="hours" name="hours" id="hours" type="number" class="form-control" min="0">
          <span style="color: red">{{ formErrors.hours }}</span>
        </div>

        <div class="mb-3">
          <label for="minutes" class="d-flex justify-content-start form-label">Minutes:</label>
          <input v-model="minutes" name="minutes" id="minutes" type="number" class="form-control" min="0">
          <span style="color: red">{{ formErrors.minutes }}</span>
        </div>

        <div class="mb-3">
          <label for="comments" class="d-flex justify-content-start form-label">Comments:</label>
          <textarea v-model="comments" name="comments" id="comments" rows="1" class="form-control"></textarea>
          <span style="color: red">{{ formErrors.comments }}</span>
        </div>

        <div class="me-0">
          <label for="overtime" class="d-flex justify-content-start form-label">Pay Rate:</label>
          <select v-model="payRate" id="overtime" name="overtime" class="form-select" aria-label="Default select example" required>
            <option value="base">Base</option>
            <option value="overtime">Overtime</option>
          </select>
          <span style="color: red">{{ formErrors.payRate }}</span>
        </div>

      </div>
      <div class="d-grid gap-2">
        <button class="btn btn-info mt-3" @click="submitUserTimeEntryForm()">Submit</button>
      </div>

<!--    </form>-->
  </section>
</template>

<script>
import {mapGetters, mapState, mapActions} from "vuex";

import axios from "axios";
import Cookies from 'js-cookie'

const csrftoken = Cookies.get('csrftoken');



export default {
  name: "timesheetUserEntryForm",

  methods: {
    ...mapActions(['submitUserTimeEntryForm']),
    activateDateRangePicker() {
      console.log('activateDateRangePicker')
      this.$store.state.userTimeForm.dateRangePickerActive = !this.$store.state.userTimeForm.dateRangePickerActive

      // need to clear end date when changing back to single day entry
      this.$store.state.userTimeForm.endDate = null
    },
  },

  computed: {
    ...mapState(['userTimeForm', 'formErrors']),

    ...mapGetters(['getDateRangePickerStatus']),

    date: {
      get() {
        return this.$store.state.userTimeForm.date
      },
      set(value) {
        this.$store.commit('UPDATE_DATE', value)
      }
    },
    endDate: {
      get() {
        return this.$store.state.userTimeForm.endDate
      },
      set(value) {
        this.$store.commit('UPDATE_END_DATE', value)
      }
    },
    hours: {
      get() {
        return this.$store.state.userTimeForm.hours
      },
      set(value) {
        this.$store.commit('UPDATE_HOURS', value)
      }
    },
    minutes: {
      get() {
        return this.$store.state.userTimeForm.minutes
      },
      set(value) {
        this.$store.commit('UPDATE_MINUTES', value)
      }
    },
    comments: {
      get() {
        return this.$store.state.userTimeForm.comments
      },
      set(value) {
        this.$store.commit('UPDATE_COMMENTS', value)
      }
    },
    payRate: {
      get() {
        return this.$store.state.userTimeForm.payRate
      },
      set(value) {
        this.$store.commit('UPDATE_PAY_RATE', value)
      }
    },
  },
}
</script>

<style scoped>

</style>
