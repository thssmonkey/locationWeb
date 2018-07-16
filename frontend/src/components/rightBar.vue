<template>
  <div id="wrap">
    <div id="header">网关</div>
    <div id="container">
      <div v-for="(gateway, index) in rightmsgs" :key="index">
        <Button class="btn" type="dashed" @click="checkDetails(index)">{{gateway.name}}</Button>
      </div>
    </div>
    <div id="footer">
      <div id="title">具体数据</div>
      <div class="detail-style" v-if="click">ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp; {{gateway.gid}}</div>
      <div class="detail-style" v-if="click">NAME:&nbsp; {{gateway.name}}</div>
      <div class="detail-style" v-if="click">COOR:&nbsp; {{gateway.coordinate}}</div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "rightBar",
    props: ['rightmsgs'],
    data () {
      return {
        gateway: '',
        click: false
      }
    },
    mounted () {
      this.getGw()
    },
    methods: {
      getGw () {
      },
      checkDetails (index) {
        this.gateway = this.rightmsgs[index]
        this.click = true
        this.$root.Bus.$emit('gatewayEvent', this.gateway)
      }
    }
  }
</script>

<style scoped>
  #wrap{
    width: 100%;
    height: 100%;
  }
  #header{
    padding: 10px;
    height: 40px;
    background: #DCDCDC;
    text-align: center;
    margin-bottom: 10px;
  }
  #container{
    position: relative;
    margin-left: 60px;
    height: 280px;
  }
  #footer{
    height: 135px;
    border-top: 2px solid #dddee1;
  }
  #title {
    padding: 10px;
    height: 40px;
    background: #DCDCDC;
    text-align: center;
  }
  .detail-style {
    margin: 9px 0 0 20px;
    font-family: 'Helvetica Neue';
    font-size: 12px;
    font-weight: bold;
  }
  .btn {
    margin-bottom: 3px;
  }
</style>
