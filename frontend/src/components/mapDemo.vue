<template>
  <div id="allmap" class=mapStyle></div>
</template>

<script>
  import BMap from 'BMap'
  export default {
    name: 'mapDemo',
    props: ['allmsgs'],
    data:function(){
      return{
        longitude: 116.404,
        latitude: 39.915
      }
    },
    components: {
      BMap
    },
    watch: {
      allmsgs(newVal, oldVal) {
        this.allmsgs = newVal
        this.ready()
      }
    },
    created(){
      this.$root.Bus.$on('deviceEvent', value => {
        this.longitude = value.coordinate.split(",")[0]
        this.latitude = value.coordinate.split(",")[1]
        this.ready()
      })
      this.$root.Bus.$on('gatewayEvent', value => {
        this.longitude = value.coordinate.split(",")[0]
        this.latitude = value.coordinate.split(",")[1]
        this.ready()
      })
    },
    mounted () {
      this.ready()
    },
    methods: {
      ready () {
        // 创建地图
        var map = new BMap.Map("allmap")
        // 设置地图中心点，北京市天安门
        var point = new BMap.Point(this.longitude, this.latitude)
        // 初始化地图,设置中心点坐标和地图级别
        map.centerAndZoom(point, 15)
        // 后端数据
        var markerArr = this.allmsgs
         // 绘制点
        var lngs = new Array()
        var lats = new Array()
        for (var i = 0; i < markerArr.length; i++) {
          var p0 = markerArr[i].coordinate.split(",")[0]
          var p1 = markerArr[i].coordinate.split(",")[1]
          var maker = addMarker(new window.BMap.Point(p0, p1), i)
          addInfoWindow(maker, markerArr[i])
          lngs[i] = p0
          lats[i] = p1
        }
        // 划线
        // 网关之间的连线
        for (var i = 0; markerArr && i < 4; i++) {
          var polyline = new BMap.Polyline([new BMap.Point(lngs[i], lats[i]), new BMap.Point(lngs[(i + 1) % 4], lats[(i + 1) % 4])], {strokeColor:"red", strokeWeight:2, strokeOpacity:0.5})
          map.addOverlay(polyline)
          addLineInfo(polyline, markerArr[i], markerArr[(i + 1) % 4])
        }
        // 节点与网关之间的连线
        for (var i = 4; i < markerArr.length; i++) {
          for (var j = 0; j < 4; j++) {
            var polyline = new BMap.Polyline([new BMap.Point(lngs[i], lats[i]), new BMap.Point(lngs[j], lats[j])], {strokeColor:"purple", strokeWeight:2, strokeOpacity:0.5})
            map.addOverlay(polyline)
            addLineInfo(polyline, markerArr[i], markerArr[j])
          }
        }
        // 添加功能和控件
        map.enableScrollWheelZoom(true)                                  // 启用滚轮放大缩小
        map.enableDoubleClickZoom(true)                                  // 启用双击放大
        map.enableKeyboard((true))                                       // 启用键盘操作。键盘的上、下、左、右键可连续移动地图。+、-键会使地图放大或缩小一级
        map.enableInertialDragging(true)                                 // 启用地图惯性拖拽
        map.enableContinuousZoom(true)                                   // 启用连续缩放效果
        map.addControl(new BMap.MapTypeControl())                        // 添加2D,3D卫星地图类型控件
        map.addControl(new BMap.OverviewMapControl())                    // 添加右下角缩略图（小地图）控件
        map.addControl(new BMap.NavigationControl())                     // 比例尺控件
        map.addControl(new BMap.ScaleControl())                          // 缩放控件
        map.addControl(new BMap.GeolocationControl())                    // 定位控件
        // 绘制标注的函数
        function addLineInfo(line, from, to){
          var linePoint = line.getPath()                                       //线的坐标串
          var myIcon = new BMap.Icon("http://api0.map.bdimg.com/images/stop_icon.png", new BMap.Size(11, 11))
          var middlePoint = new BMap.Point((linePoint[0].lng + linePoint[1].lng) / 2, (linePoint[0].lat + linePoint[1].lat) / 2)
          var marker = new BMap.Marker(middlePoint,{ icon: myIcon })             // 创建标注
          map.addOverlay(marker)                                               // 将标注添加到地图中
          //pop弹窗标题
          var title = '<div style="font-weight:bold;color:#CE5521;font-size:14px">' + "从" + from.name + "到" + to.name + '</div>'
          //pop弹窗信息
          var html = []
          html.push('<table cellspacing="0" style="table-layout:fixed;width:100%;font:12px arial,simsun,sans-serif"><tbody>')
          html.push('<tr>')
          html.push('<td style="vertical-align:top;line-height:16px;width:38px;white-space:nowrap;word-break:keep-all">距离:</td>')
          html.push('<td style="vertical-align:top;line-height:16px">' +  (map.getDistance(linePoint[0], linePoint[1])).toFixed(2) + '米' + ' </td>')
          html.push('</tr>')
          html.push('</tbody></table>')
          var infoWindow = new BMap.InfoWindow(html.join(""), { title: title, width: 200 })
          var openInfoWinFun = function () {
            marker.openInfoWindow(infoWindow)
          }
          marker.addEventListener("click", openInfoWinFun)
        }
        // 添加标注
        function addMarker(point, index) {
          if (index < 4) {
            var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png",
              new BMap.Size(23, 25), { offset: new BMap.Size(10, 25), imageOffset: new BMap.Size(0, 0 - 12 * 25) })
            var marker = new BMap.Marker(point, { icon: myIcon })
          }
          else {
            var marker = new BMap.Marker(point)
          }
          map.addOverlay(marker)
          var label = new window.BMap.Label(markerArr[index].name, { offset: new window.BMap.Size(20, -10) });
          label.setStyle({ width: "80px", color: '#fff', background: '#ff8355', border: '1px solid "#ff8355"',
            borderRadius: "5px", textAlign: "center", height: "26px", lineHeight: "26px" });
          marker.setLabel(label);
          return marker
        }
        // 添加信息窗口
        function addInfoWindow(marker, poi) {
          //pop弹窗标题
          var title = '<div style="font-weight:bold;color:#CE5521;font-size:14px">' + poi.name + '</div>'
          //pop弹窗信息
          var html = []
          html.push('<table cellspacing="0" style="table-layout:fixed;width:100%;font:12px arial,simsun,sans-serif"><tbody>')
          html.push('<tr>')
          html.push('<td style="vertical-align:top;line-height:16px;width:38px;white-space:nowrap;word-break:keep-all">坐标:</td>')
          html.push('<td style="vertical-align:top;line-height:16px">' + poi.coordinate + ' </td>')
          html.push('</tr>')
          html.push('</tbody></table>')
          var infoWindow = new BMap.InfoWindow(html.join(""), { title: title, width: 200 })
          var openInfoWinFun = function () {
            marker.openInfoWindow(infoWindow)
          }
          marker.addEventListener("click", openInfoWinFun)
          return openInfoWinFun;
        }
      }
    }
  }
</script>

<style scoped>
  .mapStyle {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    overflow:hidden;
  }
</style>
