<template>
    <div id="menu-bar">
        <div class="filters">
            <p class="section-tittle">IMAGE FILTER</p>
            <div class="filter" 
                v-for="filter in filters"
                v-bind:key="filter._id"
                :class="{ 'active': filter.name === filterSelected }"
                @click="changeFilter(filter.name)">
                {{ filter.name }}
            </div>
        </div>    
        <button class="btn minimize-menu left active">
            <b-icon icon="arrow-bar-left"></b-icon>
        </button>
        <button class="btn minimize-menu right disable">
            <b-icon icon="arrow-bar-right"></b-icon>
        </button>

        <div class="stats">
            <p class="section-tittle">STATISTICS</p>
            <div class="stat">
                Ey Max, insert stats here.
            </div> 
        </div>
    </div> 
</template>

<script>
    import {mapState,mapMutations,mapActions} from 'vuex';

    export default {
        name: "Menu",
        data: function () {
            return {
            }
        },
        computed: {
            ...mapState(['filters','filterSelected'])
        },
        methods: {
            ...mapMutations(['changeFilter']),
            ...mapActions(['getFilters']) 
        },
        created() { 
            this.$store.dispatch('getFilters');
        },
    };

    document.addEventListener("DOMContentLoaded", function(event) {
        console.log("[MENU] DOM fully loaded and parsed"); 
        var buttons_minimize = document.querySelectorAll(".btn.minimize-menu");
        var b_icon_left = document.querySelector(".btn.minimize-menu.left");
        var b_icon_right = document.querySelector(".btn.minimize-menu.right");
            
        buttons_minimize.forEach(element => {
            element.onclick = function () {            
                // Cambia el icono del boton
                if (b_icon_left.classList.contains("active")){
                    b_icon_left.classList.remove("active");
                    b_icon_left.classList.add("disable");
                    b_icon_right.classList.remove("disable");
                    b_icon_right.classList.add("active");
                }else{                
                    b_icon_right.classList.remove("active");
                    b_icon_right.classList.add("disable");
                    b_icon_left.classList.remove("disable");
                    b_icon_left.classList.add("active");
                }

                //Animacion: minimiza el menu
                var menu = document.getElementById("menu-bar");
                if (menu.style.width!="0%"){
                    menu.style.width="0%"
                }else{
                    menu.style.width="90%"
                }
            };
        });

    });

</script>

<style scoped>
#menu-bar {
    background-color: var(--secondary-bg-color);
    border-radius: 4px 0px 4px 4px;
    border-top: 0px;
    display: inline-block;
    grid-area: menu;
    overflow-x: hidden; 
    position: relative;
    transition: width 0.5s;
    width:90%;
    z-index: 10;
}

.btn.minimize-menu{
    background-color:var(--select-color);
    border-bottom: 2px;
    border-radius: 0px 24px 24px 0px;
    box-shadow: 2px 2px rgb(0, 0, 0, 20%);
    color: white;
    position: fixed;
}
.active{
    display: inline-block;
}
.disable{
    display: none;
}

.filters{
    width: 100%;
    display: inline-block;
}

.section-tittle{
    text-align: left;
    font-weight: bold;
    margin: 2px;
    border-bottom: 2px solid black;
    border-top: 2px solid black;
}

.filter {
    background-color:var(--primary-bg-color);
    padding: 2px;
    position: relative;
    text-align: left;
    width: 100%;
}

.filter:hover {
    background-color:var(--hover-color);
    cursor: pointer;
}

.filter.active {
    background-color:var(--select-color);
    color: white;
}

.stat{
    background-color: var(--primary-bg-color);
    /*BORRAR LAS PROPIEDADES SIGUIENTES CUANDO SE TERMINE LA SECCION DE ESTADISTICAS*/ 
    height: 200px;
}

</style>