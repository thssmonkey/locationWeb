<template>
  <div id="wrap">
    <div id="header">终端设备</div>
    <div id="container">
      <EasyScrollbar :barOption="barOpt">
        <div id="wrapper">
          <div v-for="(device, index) in leftmsgs" :key="index">
            <Button class="btn" type="dashed" ghost @click="checkDetails(index)">{{device.name}}</Button>
          </div>
        </div>
      </EasyScrollbar>
    </div>
    <div id="footer" v-if="click">
      <div id="title">具体数据</div>
      <div class="detail-style">ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp; {{device.eid}}</div>
      <div class="detail-style">NAME:&nbsp; {{device.name}}</div>
      <div class="detail-style">COOR:&nbsp; {{device.coordinate}}</div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "leftBar",
    props: ['leftmsgs'],
    data () {
      return {
        barOpt: {
          barColor: "#959595",    //滚动条颜色
          barWidth: 2,            //滚动条宽度
          railColor: "#eee",      //导轨颜色
          barMarginRight: 0,      //垂直滚动条距离整个容器右侧距离单位（px）
          barMaginBottom: 0,      //水平滚动条距离底部距离单位（px)
          barOpacityMin: 0.1,     //滚动条非激活状态下的透明度
          zIndex: "auto",         //滚动条z-Index
          autohidemode: true,     //自动隐藏模式
          horizrailenabled: true, //是否显示水平滚动条
        },
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
    padding: 4px;
    height: 40px;
    border-bottom: 2px solid #5a5a5a;
    /*background: #DCDCDC;*/
    text-align: center;
    font-size: 20px;
    font-family: "微软雅黑";
    color: rgb(255, 255, 255);
  }
  #container{
    position: relative;
    padding: 10px 0 10px 50px;
    height: 350px;
  }
  #footer{
    height: 135px;
    border-top: 2px solid #5a5a5a;
  }
  #title {
    padding: 6px;
    height: 40px;
    /*background: #DCDCDC;*/
    border-bottom: 2px solid #5a5a5a;
    text-align: center;
    font-size: 16px;
    font-family: "微软雅黑";
    color: rgb(255, 255, 255);
  }
  #wrapper {
    height: 330px;
  }
  .detail-style {
    margin: 5px 0 0 5px;
    font-family: 'Helvetica Neue';
    font-size: 10px;
    font-weight: bold;
  }
  .btn {
    margin-bottom: 3px;
    color: rgb(204, 204, 204);
  }
</style>
