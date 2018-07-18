<template>
  <div id="wrap">
    <div id="header">网关</div>
    <div id="container">
      <EasyScrollbar :barOption="barOpt">
        <div id="wrapper">
          <div v-for="(gateway, index) in rightmsgs" :key="index">
            <Button class="btn" type="dashed" @click="checkDetails(index)">{{gateway.name}}</Button>
          </div>
        </div>
      </EasyScrollbar>
    </div>
    <div id="footer" v-if="click">
      <div id="title">具体数据</div>
      <div class="detail-style">ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp; {{gateway.gid}}</div>
      <div class="detail-style">NAME:&nbsp; {{gateway.name}}</div>
      <div class="detail-style">COOR:&nbsp; {{gateway.coordinate}}</div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "rightBar",
    props: ['rightmsgs'],
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
    padding: 4px;
    height: 40px;
    text-align: center;
    margin-bottom: 10px;
    /*background: #DCDCDC;*/
    border-bottom: 2px solid #5a5a5a;
    font-size: 20px;
    font-family: "微软雅黑";
    color: rgb(255, 255, 255);
  }
  #container{
    position: relative;
    padding-left: 70px;
    height: 280px;
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
    height: 270px;
  }
  .detail-style {
    margin: 9px 0 0 20px;
    font-family: 'Helvetica Neue';
    font-size: 12px;
    font-weight: bold;
  }
  .btn {
    margin-bottom: 3px;
    color: rgb(204, 204, 204);
  }
</style>
