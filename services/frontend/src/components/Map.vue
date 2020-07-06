<template>
    <div id="map" class="map"></div>
</template>

<script>
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ';

export default {
    name: "OpenlayersMap",
    mounted() {
        this.$nextTick(function () {
            new Map({
                target: 'map',
                layers: [
                    new TileLayer({
                        source: new OSM(),
                        opacity: 0.7
                    }),
                    new TileLayer({
                        source: new XYZ({
                            url: process.env.VUE_APP_BE_URL + '/RAW/2016-01-09/{z}/{y}/{x}?key=' + process.env.VUE_APP_BE_API_TOKEN,
                            maxZoom: 9
                            //url: 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Aqua_CorrectedReflectance_TrueColor/default/2014-04-09/250m/{z}/{y}/{x}.jpeg'
                            //url: 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/2016-04-09/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpeg',
                            
                        })
                    }),
                    new TileLayer({
                        source: new XYZ({
                            url: process.env.VUE_APP_MAPTILER_URL  + '?key=' + process.env.VUE_APP_MAPTILER_API_TOKEN
                        }),
                        opacity: 0.7
                    }),
                ],
                view: new View({
                    //projection: 'EPSG:4326',
                    center: [0,0],
                    zoom: 1
                })
            });
        })
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