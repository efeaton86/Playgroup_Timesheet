import Vuex from 'vuex';

// 3rd party packages
import axios from 'axios';
import dayjs from "dayjs";
import Cookies from "js-cookie";

const csrftoken = Cookies.get('csrftoken')

const getDefaultUserTimeFormState = () =>  {
  return {
    userTimeForm: {
      dateRangePickerActive: false,
      date: null,
      endDate: null,
      hours: null,
      minutes: null,
      comments: null,
      payRate: null
    }
  }
}

const getDefaultFormErrorState = () =>  {
  return {
    formErrors: {
      date: undefined,
      endDate: undefined,
      hours: undefined,
      minutes: undefined,
      comments: undefined,
      payRate: undefined
    }
  }
}

let store = new Vuex.Store({
  state: {
    userTimeEntries: [],
    userTimeForm: {
      dateRangePickerActive: false,
      date: null,
      endDate: null,
      hours: null,
      minutes: null,
      comments: null,
      payRate: null
    },
    formErrors: {
      date: undefined,
      endDate: undefined,
      hours: undefined,
      minutes: undefined,
      comments: undefined,
      payRate: undefined
    }
  },

  mutations: {
    //commit payload to userTimeEntries object
    UPDATE_TIME_ENTRIES (state, payload) {
      state.userTimeEntries = payload
    },
    //timesheetUserEntryForm mutations
    UPDATE_DATE (state, date) {
      state.userTimeForm.date = date
    },
    UPDATE_END_DATE (state, date) {
      state.userTimeForm.endDate = date
    },
    UPDATE_HOURS (state, hours) {
      state.userTimeForm.hours = hours
    },
    UPDATE_MINUTES (state, minutes) {
      state.userTimeForm.minutes = minutes
    },
    UPDATE_COMMENTS (state, comments) {
      state.userTimeForm.comments = comments
    },
    UPDATE_PAY_RATE (state, rate) {
      state.userTimeForm.payRate = rate
    },
    UPDATE_FORM_ERRORS (state, errors) {
      for (const key in errors) {
        const value = errors[key]
        state.formErrors[key] = value
      }
    },
    RESET_STATE (state) {
      Object.assign(state, getDefaultUserTimeFormState())
    },
    RESET_ERRORS (state) {
      Object.assign(state, getDefaultFormErrorState())
    }
  },

  actions: {
    // get user entries from the server
    //
    getUserTimeEntries ({ commit }, date_obj) {
      var month = date_obj.month
      var year = date_obj.year
      axios({
        method: 'GET',
        url: 'api/form_entries/',
        params: {
          month: month,
          year: year
        }
      })
        .then((response) => {
          commit(
            'UPDATE_TIME_ENTRIES',
            JSON.parse(response.data.time_entries_json)
          )
        })
    },

    setDay ({ commit }, user_date) {
      commit('UPDATE_DATE', user_date)
    },

    async submitUserTimeEntryForm({commit, dispatch}, state) {
      //validate form
      let errors = await dispatch('validateForm')

      //if errors, load errors to Vuex state
      if (Object.keys(errors).length) {
        commit('UPDATE_FORM_ERRORS', errors)
        return
      }

      // clear Vuex error state if there are no errors from front end validation
      commit('RESET_ERRORS')

      // submit form
      const userForm = JSON.stringify(store.state.userTimeForm)
      console.log(userForm)
      console.log('hello')
      axios({
        method: 'POST',
        url: '/timesheet/',
        data: userForm,
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'},
      })
      .then((response) => {
        var data = response.data

        // check if any errors found on backend validation
        if (data['is_valid_form'] == false) {
          const error_obj = data['error_dict']
          commit('UPDATE_FORM_ERRORS', error_obj)

        } else {
          console.log('reset state')
          commit('RESET_STATE')
          //redirect
        }
      })
    },

    validateForm({ commit }, context) {
      //validate that date is not empty
      const errors = {}
      if (store.state.userTimeForm.dateRangePickerActive) {
        if (
          (store.state.userTimeForm.date > store.state.userTimeForm.endDate) ||
          (!store.state.userTimeForm.date || !store.state.userTimeForm.endDate)
        ) {
          errors.endDate = "End date must come after start date."
        }
      }
      if (
        !Number.isInteger(Number(store.state.userTimeForm.hours)) ||
        Number(store.state.userTimeForm.hours) < 0
      ) {errors.hours = 'Must be a positive integer.'}
      if (
        !Number.isInteger(Number(store.state.userTimeForm.minutes)) ||
        Number(store.state.userTimeForm.minutes) < 0
      ) {errors.minutes = 'Must be a positive integer.'}
      if (!store.state.userTimeForm.hours && !store.state.userTimeForm.minutes) {
        errors.hours = 'Both hours and minutes may not be empty.'
        errors.minutes = 'Both hours and minutes may not be empty.'
      }
      if (!store.state.userTimeForm.date) {
        errors.date = 'A date must be provided.'
      }
      return errors
    },
  },

  getters: {
    userTimeEntries: state => state.userTimeEntries,

    getDateRangePickerStatus: function (state) {
      return state.userTimeForm.dateRangePickerActive
    },

    daysWithTimeEntry: function (state) {
      const unique = new Set()
      for (let i = 0; i < Object.keys(state.userTimeEntries).length; i++) {
        var obj = state.userTimeEntries[i]
        unique.add(dayjs(obj['record_date']).date())
      }
      return unique
    }
  },
  modules: {
  }
})


export default store
