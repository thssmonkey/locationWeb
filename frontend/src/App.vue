<template>
  <div id="app"> <!--class="container"-->
    <!--<img src="./assets/logo.png">
    <router-view/>-->
    <transition name="fade">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </transition>
  </div>
  <!--

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.container{
  padding-top: 40px;
  width:1170px;
  margin: 0 auto;
  padding-bottom: 20px;
  overflow: hidden;
}
  -->
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
</style>
