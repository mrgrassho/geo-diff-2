import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ';
import TileLayer from 'ol/layer/Tile';

Vue.use(Vuex)

export default new Vuex.Store({
  state: { //Atributos generales que manejarn los componentes
    dates : [],
    filters : [],
    filterSelected : '2016-01-09',
    dateSelected : 'RAW',
    map : {}
  },
  mutations: { // Procesos que cambian los valroes de esos atributos generales
    changeFilter(state,filter){
      state.filterSelected = filter;
      this.commit('updateMap',state);
    },
    changeDate(state,date){
      state.dateSelected = date;
      this.commit('updateMap',state);
    },
    setFilters(state, filters){
      state.filters = filters;
    },
    setDates(state, dates){
      state.dates = dates;
    },
    setMap(state,map){
      state.map = map;
    },
    updateMap(state) {
      console.log('Actualizando filtro/fecha en el mapa');
      let s = new XYZ({
          url: `${process.env.VUE_APP_BE_URL}/${state.filterSelected}/${state.dateSelected}/{z}/{y}/{x}?key=${process.env.VUE_APP_BE_API_TOKEN}`,
          maxZoom: 9
      });
      let l = state.map.getLayers().getArray()[1];
      l.setSource(s);
    }  
  },

  actions: { //Eventos o acciones que llaman a los procesos anteriores.
    getFilters({commit}){
      console.log("Obteniendo filtros de la API...");
      axios //Libreria para consumir de una API.
      .get(process.env.VUE_APP_BE_URL + "/filters", {
          headers: {
              'Authorization': process.env.VUE_APP_BE_API_TOKEN
          }
      })
      .then(response => {  //llamo a las mutations
            commit('setFilters',response.data)
            commit('changeFilter',response.data[0].name)
      })
      //.catch(e => { this.errors.push(e)})
    },

    getDates({commit}){
      console.log("Obteniendo fechas de la API...");
      axios //Libreria para consumir de una API.
      .get(process.env.VUE_APP_BE_URL + "/dates", {
          headers: {
              'Authorization': process.env.VUE_APP_BE_API_TOKEN
          }
      })
      .then(response => { //llamo a las mutations
            commit('setDates',response.data)
            commit('changeDate',response.data[0].date)
            //console.log(response.data);  
      })
      //.catch(e => { this.errors.push(e)})
    },

    getMap({commit}){
        const mapX = new Map({
          target: 'map',
          layers: [
              new TileLayer({
                  source: new OSM(),
                  opacity: 0.7
              }),
              new TileLayer({
                  source: new XYZ({
                      url: `${process.env.VUE_APP_BE_URL}/${this.state.filterSelected}/${this.state.dateSelected}/{z}/{y}/{x}?key=${process.env.VUE_APP_BE_API_TOKEN}`,
                      maxZoom: 9
                  })
              }),
              new TileLayer({
                  source: new XYZ({
                      url: `${process.env.VUE_APP_MAPTILER_URL}?key=${process.env.VUE_APP_MAPTILER_API_TOKEN}`
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
        commit('setMap',mapX);
    }
  },

})
