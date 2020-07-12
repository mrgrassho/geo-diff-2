<template>
    <div id="map" class="map"></div>
</template>

<script>
        
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

<style scoped>
    .map {
        width: 100%;
        height: 100%;
        left: 0px;
        top: 0px;
        position: absolute;
    }
</style>