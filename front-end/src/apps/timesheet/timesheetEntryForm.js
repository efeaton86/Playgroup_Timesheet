import {createApp} from "vue";
import timesheetEntryForm from "@/apps/timesheet/timesheetEntryForm.vue";
import store from "@/store/store";


createApp(timesheetEntryForm).use(store).mount('#app-entryForm')
