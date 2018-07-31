<template>
  <div class="tags">
    <div class="title">Location</div>
    <div class="btn">
      <Button type="dashed" shape="circle" @click="refresh">
        <Icon type="md-refresh" size=20 v-if="loading==false" />
        <Icon type="ios-loading" size=20 class="spin-icon-load" v-if="loading==true"></Icon>
     </Button>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'navigationBar',
    props: ['loading'],
    data () {
      return {
      }
    },
    methods: {
      refresh () {
        this.$root.Bus.$emit('refreshEvent', '116.404,39.915')
        this.$emit('listenChildMsg', !this.loading)
      }
    }
  }
</script>

<style scoped>
  .tags{
    width: 100%;
    height: 100%;
    position: relative;
    /*background: black;
    background-color: rgb(237, 249, 250); <Icon type="ios-refresh" />*/
    word-wrap: break-word;
    padding: 0px;
    border: 0px solid transparent;
    display: block;
    opacity: 0.3;
    background-color: rgb(255, 255, 255);
    filter: alpha(opacity=30);
    -moz-opacity: 0.3;
    -khtml-opacity: 0.3;
    opacity: 0.6;
  }
  .title {
    position: absolute;
    width: 96%;
    padding: 10px;
    font-size: 20px;
    text-align: center;
    font-family: "微软雅黑";
    color: black;
  }
  .btn {
    position: absolute;
    top: 8px;
    margin-left: 96%;
  }
  .spin-icon-load{
    animation: ani-demo-spin 1s linear infinite;
  }
</style>
