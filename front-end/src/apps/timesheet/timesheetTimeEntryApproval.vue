<template>
  <div class="container-fluid">
    <section id="header">
      <div class="container d-flex flex-column justify-content-between">
            <span id="settings_selector" class="py-3">Select Pay Period:
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-week" viewBox="0 0 16 16">
                <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-5 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
              </svg>
            </span>
            <div class="row mt-5 mb-4 d-flex justify-content-start">
              <div class="col-md-6">
                  <label class="me-3" for="start">Pay Period:</label>
                  <input v-model="payPeriod" type="month" id="start" name="start" min="2019-01">
              </div>
            </div>


            <div id="employee_card_container" class="container d-flex flex-column p-1">
              <TimeApprovalEmployeeCard
                :users="users"
                :userTimeEntries="userTimeEntries"
                :cards="cards"
              ></TimeApprovalEmployeeCard>

              <!--<p class="card-text">Selecting detail view removes the bar chart</p>-->
              <!--<p class="card-text">And displays a tabular view of the users time that should be approved</p>-->
            </div>

      </div>
    </section>
    <section id="body">
      <div class="row mt-5 d-flex justify-content-center">
        <div class="col-md-10">
          <h1>Bar Chart</h1>
<!--          <barChart-->
<!--            :chartData="chartDataBar"-->
<!--            :chartOptions="chartOptionsBar"-->
<!--            :chartType="chartTypeBar"-->
<!--          ></barChart>-->
        </div>

      </div>
    </section>
    <section id="footer">
      <div class="container d-flex justify-content-end me-0 pt-5 pb-2">
        <button class="btn btn-primary">Pay Cycle Report Generator</button>
      </div>
    </section>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
const csrftoken = Cookies.get('csrftoken');

import barChart from "@/components/timesheet/barChart";
import TimeApprovalEmployeeCard from "@/components/timesheet/TimeApprovalEmployeeCard";
import axios from "axios";



export default {
  name: 'timesheetTimeEntryApproval',
  components: { barChart, TimeApprovalEmployeeCard },
  data: function () {
    return {
      // User Data
      users: [],
      selectedUser: null,
      userTimeEntries: [],

      // Mock Data for carousel -> pass to the TimeApprovalEmployeeCard
      cards: [1,2,3,4,5],

      // Chart Data
      chartDataBar: {
        labels:
          ['Employee 1', 'Employee 2', 'Employee 3', 'Employee 4'],
        datasets: [
          {
            label: "Recorded Time for Current Month",
            data: [10,20,30,40],
            backgroundColor: [
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1,
          },
        ],
      },
      chartTypeBar: 'bar',
      chartOptionsBar: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },

      // make this default to current month
      //payPeriod: '2021-11',
      payPeriod: null,
    }
  },
  watch: {
    payPeriod() {
      this.getUserTimeEntryData()
    }
  },
  computed: {},

  methods: {
    getTodaysDate: function() {
      var date = new Date()
      var month = date.getMonth()
      var year = date.getFullYear()
      this.payPeriod = `${year}-${month + 1}`
    },

    getUserTimeEntryData: function () {
      console.log(this.payPeriod)
      axios({
        method: 'PUT',
        url: '/timesheet/api/get_user_time_entry_data/',
        data: {
          payPeriod: this.payPeriod,
        },
        headers: {
          "X-CSRFToken": csrftoken,
          'Content-Type': 'application/json'
        }
      }).then(
        (response) => {
          var users = JSON.parse(response.data.payload.users)
          var timeEntries = response.data.payload.pay_period_entries
          for (let i = 0; i < timeEntries.length; i++) {
            this.userTimeEntries.push(timeEntries[i])
          }
          this.users = users
        }
      )
    },
  },

  mounted() {
    this.getTodaysDate()
  },
}


</script>

<style scoped>

#settings_selector {
  justify-content: end;
}

</style>

