<template>
  <div class="tags">
    <div class="title">你丑你先看</div>
  </div>
</template>

<script>
  export default {
    name: 'navigationBar'
  }
</script>

<style scoped>
  .tags{
    width: 100%;
    height: 100%;
    text-align: center;
    /*background: black;
    background-color: rgb(237, 249, 250);*/
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
    padding: 10px;
    font-size: 20px;
    font-family: "微软雅黑";
    color: black;
  }
</style>
