<template>
  <div id="wrap">
    <div id="header"><navigationBar v-bind:loading="refresh" v-on:listenChildMsg="recvmsg"></navigationBar></div>
    <div id="container">
      <div id="left_side"><leftBar :leftmsgs="endDeivces"></leftBar></div>
      <div id="content" v-if="hackReset"><mapDemo :allmsgs="allDatas"></mapDemo></div>
      <div id="right_side"><rightBar :rightmsgs="gateWays"></rightBar></div>
    </div>
    <!--<div id="footer"><footerBar></footerBar></div>-->
  </div>
</template>

<script>
  import navigationBar from './navigationBar'
  import leftBar from './leftBar'
  import mapDemo from './mapDemo'
  import rightBar from './rightBar'
  import footerBar from './footerBar'
  export default {
    name: 'home',
    components: {
      navigationBar,
      leftBar,
      mapDemo,
      rightBar,
      footerBar
    },
    data () {
      return {
        refresh: false,
        hackReset: false,
        endDeivces: [],
        gateWays: [],
        allDatas: []
      }
    },
    mounted () {
      this.getEd()
      this.getGw()
      this.getAllData()
      this.hackReset = false
      this.$nextTick(() => {
        this.hackReset = true
      })
    },
    methods: {
      recvmsg (data){
        this.refresh = data
        this.getEd()
        this.getGw()
        this.getAllData()
      },
      getEd () {
        this.$http.get(this.GLOBAL.baseUrl + 'api/locationMap/getEd')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.endDeivces = res
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
          .catch((response) => {
            this.$Message.error('获取终端节点数据失败：' + response)
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
      },
      getGw () {
        this.$http.get(this.GLOBAL.baseUrl + 'api/locationMap/getGw')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.gateWays = res
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
          .catch((response) => {
            this.$Message.error('获取网关数据失败：' + response)
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
      },
      getAllData () {
        this.$http.get(this.GLOBAL.baseUrl + 'api/locationMap/getAllData')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.allDatas = res
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
          .catch((response) => {
            this.$Message.error('获取网关和终端节点数据失败：' + response)
            if (this.refresh) {
              this.refresh = !this.refresh
            }
          })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #wrap{
    width: 100%;
    margin: 0 auto;
  }
  #header{
    margin-bottom: 10px;
    height: 50px;
  }
  #container{
    position: relative;
    height: 530px;
    border: 2px solid #5a5a5a;
  }
  #left_side{
    position: absolute;
    top: 0px;
    left: 0px;
    width: 200px;
    height: 100%;
  }
  #content{
    margin: 0px 200px 0px 200px;
    height: 100%;
    border-left: 2px solid #5a5a5a;
    border-right: 2px solid #5a5a5a;
  }
  #right_side{
    position: absolute;
    top: 0px;
    right: 0px;
    width: 200px;
    height: 100%;
  }
  #footer{
    margin-top: 9px;
    height: 58px;
  }
</style>
