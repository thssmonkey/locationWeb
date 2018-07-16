import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import mapDemo from '@/components/mapDemo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/mapdemo',
      name: 'mapDemo',
      component: mapDemo
    }
  ]
})
