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
        margin-right: 1%;
        right: 0%;
        left: auto;
        background-color:var(--secondary-bg-color);
    }

    .ol-zoom.ol-unselectable.ol-control button{
        background-color: var(--select-color);
        opacity: 70%;
    }

    .ol-zoom.ol-unselectable.ol-control button:hover{
        opacity: 100%;
    }
</style>