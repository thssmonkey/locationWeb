// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import globalValue from './components/globalValue'

Vue.prototype.GLOBAL = globalValue
Vue.config.productionTip = false

Vue.use(VueResource)

// 设置 POST 请求时 的 data 格式
// Vue.http.options.emulateJSON = true

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
