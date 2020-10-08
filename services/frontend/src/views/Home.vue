<template>
  <div class="home">
        <div id="logo" class="box">
            <img src="@/assets/logo.svg" alt="">
            <div id="title">
                <h2>GeoDiff</h2>
                <span>Comparing surfaces over time</span>
            </div>
        </div>
        <OpenLayersMap></OpenLayersMap>
        <Menu class="box"></Menu>
        <Dates class="box"></Dates>
  </div>
</template>

<script>
import Menu from '@/components/Menu.vue'
import Dates from '@/components/Dates.vue'
import OpenLayersMap from '@/components/Map.vue'

export default {
  name: 'Home',
    data () {
    return {
    }
  },
  components: {
    OpenLayersMap,
    Menu,
    Dates
  }
}
</script>


<style>
/*VARIABLES GENERALES*/


html, body {
  height: 100%;
  margin: 0px;
  --primary-bg-color: #8cc07f;
  --secondary-bg-color: #d1dcda;
  --select-color: #097e68;
  --hover-color:#7de663;
}

body {
    font-family: 'Montserrat', sans-serif;
}

#app{
  width: 100%;
  height: 100%;
}

.box {
    border: 2px outset #afc7a9;
    margin: 7px;
    box-shadow: 2px 2px rgb(0, 0, 0, 20%);
    border-radius: 2% 2% 2% 2%;
    background-color: var(--secondary-bg-color);
}

.home {
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-columns: 20% 80%;
    grid-template-rows: 12% 70% 18%;
    grid-template-areas:
        "logo . "
        "menu . "
        "dates dates";                 
}

#logo {
    grid-area: logo;
    border-radius: 58px 58px 58px 58px;
    -moz-border-radius: 58px 58px 58px 58px;
    -webkit-border-radius: 58px 58px 58px 58px;
    border: 2px outset #afc7a9;
    display: flex;
    height: 60px;
    background-color: var(--secondary-bg-color);
    width: 200px;
    z-index: 10;
    transition: width 400ms, height 300ms;
}

#logo img{
    height: 90%;
    padding: 5px 2px 0px 5px;
    transition: 0.4s;
}

#title{
    margin: 0% 0% 0% 1%;
    display: block;
    padding-right: 20px;
}

#title h2 {
    margin: 5% 40% 0% 0%;
    transition: margin 500ms;
    font-size: 27px;
}

#title span {
  display: inline;
  font-weight: 100;
  white-space: nowrap;
  visibility: hidden;
  transition: visibility 0s;
}


#logo:hover { 
    width: 300px;
}
#logo:hover > img{
  height: 80%;
}

#logo:hover > #title span {
    visibility: visible;
}

#logo:hover > #title h2 {
    margin: 0%;
}

</style>
