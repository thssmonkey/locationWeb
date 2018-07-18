<template>
  <div class="tags">
    <div class="title">我写的丑，看的人更丑</div>
  </div>
</template>

<script>
  export default {
    name: 'footerBar'
  }
</script>

<style scoped>
  .tags{
    width: 100%;
    height: 100%;
    text-align: center;
    /*background: #0c0914;*/
    word-wrap: break-word;
    padding: 0px;
    border: 0px solid transparent;
    display: block;
    opacity: 0.2;
    background-color: rgb(255, 255, 255);
    filter: alpha(opacity=30);
    -moz-opacity: 0.3;
    -khtml-opacity: 0.3;
    opacity: 0.1;
  }
  .title {
    padding: 16px;
    font-size: 16px;
    font-family: 微软雅黑;
    color: black;
  }
</style>
