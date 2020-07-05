<template>
  <div id="app">
    <div  class="logo-container rounded">
        <img src="@/assets/logo.svg" alt="">
        <div class="title-container">
            <h2>GeoDiff</h2>
            <span>Comparing surfaces over time</span>
        </div>
    </div>
    <OpenlayersMap></OpenlayersMap>
    <Menu></Menu>
    <Dates></Dates>
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
body {
    font-family: 'Montserrat', sans-serif;
}

.rounded {
    border-radius: 5px;
}

.logo-container {
    display: flex;
    height: max-content;
    background-color: #d1dcda;
    width: max-content;
    padding: 1%;
}

.logo-container img{
    width: 60px;
    margin: 1%;
}

.title-container{
    margin: 0% 0% 0% 3%;
    display: block;
}


.title-container h2, p{
    margin: 0%;
    width: 200px;
}

.title-container span {
  display: inline;
  font-weight: 100;
}
</style>
