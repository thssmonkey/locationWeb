import Vue from 'vue'
import Vuex from 'vuex'

// 告诉 vue “使用” vuex
Vue.use(Vuex)

// 创建一个对象来保存应用启动时的初始状态
// 需要维护的状态
const store = new Vuex.Store({
  state: {
    // 放置初始状态 app启动的时候的全局的初始值
    endDevices: '',
    gateWays: ''
  },
  mutations: {
    muEndDevices(state, msg) {
      state.endDevices = msg
    },
    muGateWays(state, msg) {
      state.gateWays = msg
    }
  },
  actions: {
    modifyEndDevices ({commit}) {
      commit('muEndDevices')
    },
    modifyGateWays ({commit}) {
      commit('muGateWays')
    }
  }
})
// 整合初始状态和变更函数，我们就得到了我们所需的 store
// 至此，这个 store 就可以连接到我们的应用中
export default store
