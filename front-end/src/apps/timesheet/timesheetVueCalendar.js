import { createApp } from 'vue'
import timesheetVueCalendar from './timesheetVueCalendar.vue'
import store from "@/store/store";



createApp(timesheetVueCalendar).use(store).mount('#app')


