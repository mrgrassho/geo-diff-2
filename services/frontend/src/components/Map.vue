<template>
    <div id="map" class="map"></div>
</template>

<script>
import Zoom from 'ol/control/Zoom';
export default {
        
    name: "OpenlayersMap",
    data () {
        return {
            mapX: {
                type: Object,
                default: {}
            }
        }
    },        
    computed: {
    },
    methods : {
    },
    mounted() {
        this.$store.dispatch('getMap');
        this.mapX = this.$store.state.map
    }
}
</script>

<style>
    .map {
        width: 100%;
        height: 100%;
        left: 0px;
        top: 0px;
        position: absolute;
    }

    .ol-zoom.ol-unselectable.ol-control{
        top: 5em;
        left: 1em;
        background-color: white;
        opacity: 80%;
    }
</style>