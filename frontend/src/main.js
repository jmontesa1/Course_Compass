import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './main.css' //Global CSS for Font
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi' //Google Icons
import '@mdi/font/css/materialdesignicons.css' //Google Icons
import { VCalendar } from 'vuetify/labs/VCalendar' //Vuetify Components from vuetify labs
import { VSparkline } from 'vuetify/labs/VSparkline' //Vuetify Components from vuetify labs
import { VNumberInput } from 'vuetify/labs/VNumberInput' //Vuetify Components from vuetify labs
const vuetify = createVuetify({
    components:{
      VCalendar,
      VSparkline,
      VNumberInput,
      ...components,
    },
    
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
          mdi,
        },
    },
})
  
  createApp(App).use(router).use(vuetify).mount('#app') //Creates the app and establishes routing and vuetify library