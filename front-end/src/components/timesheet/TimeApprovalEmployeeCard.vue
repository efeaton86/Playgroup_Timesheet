<template>
  //holds employee name card and carousel for selectable months
  <section>
    <div class="container">
        <div v-for="user in users" :key="user.id" class="row employee_card">

          <div class="col">
            <div class="card">
              <div class="card-header">{{timeApproved(user.id)}}</div>
              <div class="card-body">
                <h5 class="card-title">{{ fullName(user) }}</h5>
                <p class="card-text">Loop the user obj to add names in these boxes</p>
                <a href="#" class="btn btn-primary">Detail View</a>
              </div>
            </div>
          </div>

          <div class="col">
            <div v-for="card in cards" class="col">
              Slides go here
            </div>


          </div>

        </div>
    </div>

  </section>


</template>

<script>
export default {
  name: "TimeApprovalEmployeeCard",
  props: {
    users: {required: true},
    userTimeEntries: {required: true},
    cards: {required: false}
  },
  data: function() {
    return {

    }
  },
  methods: {
    fullName(userObject) {
      return userObject.first_name + ' ' + userObject.last_name
    },

    groupBy(object, key) {
      var groupedObject = {}
      for (let i = 0; i < this.userTimeEntries.length; i++) {
        var groupByKey = this.userTimeEntries[i][key]
        if (!groupedObject[groupByKey]) {
          groupedObject[groupByKey] = []
          groupedObject[groupByKey].push(this.userTimeEntries[i])
        } else {
          groupedObject[groupByKey].push(this.userTimeEntries[i])
        }
      }
      return groupedObject
    },

    timeApproved (userID) {
      let approvedFlag = 'Time Approved'
      var entriesByUser = this.groupBy(this.userTimeEntries, 'employee_id')
      try {
        if(entriesByUser[userID].some(element => element.entry_approved === false)) {
        approvedFlag = 'Time Not Approved'
        }
      } catch (e) {
        approvedFlag = 'No Entries'
      }
      return approvedFlag
    }
  },

  computed: {}

}
</script>

<style scoped>

</style>
