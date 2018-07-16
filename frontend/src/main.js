// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import iView from 'iview'
import router from './router'
import store from './../store/index'
import VueResource from 'vue-resource'
import globalValue from './components/globalValue'

Vue.prototype.GLOBAL = globalValue
Vue.config.productionTip = false

Vue.use(VueResource)
Vue.use(iView)
// 设置 POST 请求时 的 data 格式
// Vue.http.options.emulateJSON = true

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  data: {
    // 空的实例放到根组件下，所有的子组件都能调用
    Bus: new Vue()
  }
})
