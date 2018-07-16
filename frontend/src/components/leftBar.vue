<template>
  <div id="wrap">
    <div id="header">终端设备</div>
    <div id="container">
      <Scroll height="290">
        <div v-for="(device, index) in leftmsgs" :key="index">
          <Button class="btn" type="dashed" @click="checkDetails(index)">{{device.name}}</Button>
        </div>
      </Scroll>
    </div>
    <div id="footer">
      <div id="title">具体数据</div>
      <div class="detail-style" v-if="click">ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp; {{device.eid}}</div>
      <div class="detail-style" v-if="click">NAME:&nbsp; {{device.name}}</div>
      <div class="detail-style" v-if="click">COOR:&nbsp; {{device.coordinate}}</div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "leftBar",
    props: ['leftmsgs'],
    data () {
      return {
        device: '',
        click: false
      }
    },
    mounted () {
      this.getEd()
    },
    methods: {
      getEd () {
      },
      checkDetails (index) {
        this.device = this.leftmsgs[index]
        this.click = true
        this.$root.Bus.$emit('deviceEvent', this.device)
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
  }
  #container{
    position: relative;
    margin-left: 40px;
    height: 290px;
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
