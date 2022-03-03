import { createApp } from 'vue'
import timesheetTimeEntryApproval from './timesheetTimeEntryApproval.vue'
import store from "@/store/store";

createApp(timesheetTimeEntryApproval).use(store).mount('#app')
