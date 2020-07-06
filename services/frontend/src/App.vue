<template>
  <div id="app">
    <div id="logo" class="box">
        <img src="@/assets/logo.svg" alt="">
        <div id="title">
            <h2>GeoDiff</h2>
            <span>Comparing surfaces over time</span>
        </div>
    </div>
    <OpenlayersMap></OpenlayersMap>
    <Menu class="box"></Menu>
    <Dates class="box"></Dates>
  </div>
</template>

<script>
import OpenlayersMap from './components/Map.vue';
import Menu from './components/Menu.vue';
import Dates from './components/Dates.vue';

export default {
  name: 'App',
  components: {
    OpenlayersMap,
    Menu,
    Dates
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0px;
}

body {
    font-family: 'Montserrat', sans-serif;
}

#logo img{
    width: 100%;
    padding: 2px;
}

#title{
    margin: 0% 0% 0% 1%;
    display: block;
    padding-right: 20px;
}

#title h2 {
    margin: 5% 0% 0% 2%;
    transition: margin 1s;
    font-size: 27px;
}

#title span {
  display: inline;
  font-weight: 100;
  white-space: nowrap;
  visibility: hidden;
  transition: visibility 0s;
}

#app {
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-columns: 5% 80% 15%;
    grid-template-rows: 10% 70% 20%;
    grid-template-areas: "logo  .  	."
                        ".     .   	menu"
                        "dates dates dates";
}

.box {
    border: 2px outset #afc7a9;
    margin: 7px;
    box-shadow: 2px 2px rgb(0, 0, 0, 20%);
    border-radius: 2% 2%;
    background-color: #d1dcda;
}

#logo:hover { 
    width: 300px;
    height: 55px;
}

#logo:hover > #title span {
    visibility: visible;
}

#logo:hover > #title h2 {
    margin: 0%;
}


#logo {
    grid-area: logo;
    border-radius: 58px 58px 58px 58px;
    -moz-border-radius: 58px 58px 58px 58px;
    -webkit-border-radius: 58px 58px 58px 58px;
    border: 2px outset #afc7a9;
    display: flex;
    height: 60px;
    background-color: #d1dcda;
    width: 200px;
    z-index: 10;
    transition: width 1s, height 1s;
}
</style>
