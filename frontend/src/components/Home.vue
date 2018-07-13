<template>
  <div>
    <p>GateWay: {{gateway}}</p>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      gateway: ''
    }
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/locationMap/home')
         .then((response) => {
           var res = JSON.parse(response.bodyText)
           console.log(res)
           this.gateway = res.name
        })
        .catch((response) => {
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
