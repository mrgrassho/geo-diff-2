<template>
    <div id="dates-bar">
        <div id='date-selected'>
            {{ dateSelected }}
        </div>
        <div id="timeline-years">
            <button class="left scroll no-visible"> < </button>
            <button class="right scroll">></button>

            <div v-for= "year_x in Object.keys(inOrder()).sort()" 
                 v-bind:key= "year_x.id" 
                 class="timeline-year">
                    <div class="timeline-months">
                            <div v-for= "month_x in Object.keys(inOrder()[year_x]).sort()" 
                            v-bind:key= "month_x.id"
                            class="timeline-month">
                                    <div class="timeline-days">
                                            <div v-for= "day_x in inOrder()[year_x][month_x].sort()" 
                                                v-bind:key= "day_x.id"
                                                class="day value"
                                                @click="changeDate(
                                                [year_x,month_x,day_x].join('-'))"
                                                >
                                                {{day_x}}
                                            </div>
                                    </div>
                                    <div class="month value">{{monthToName(month_x)}}</div>
                            </div>
                    </div>
                    <div class="year value">{{year_x}}</div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState,mapMutations,mapActions} from 'vuex';

    export default {
        name: "Dates",
        data: function () {
            return {
            }
        },
        computed: {
            ...mapState(['dates','dateSelected'])
        },
        methods: {
            ...mapMutations(['changeDate']),
            ...mapActions(['getDates']),
            monthToName(month){
                var month_name = ""
                if (month=="01") {month_name = "JAN"};
                if (month=="02") {month_name = "FEB"}
                if (month=="03") {month_name = "MAR"}
                if (month=="04") {month_name = "APR"}
                if (month=="05") {month_name = "MAY"}
                if (month=="06") {month_name = "JUNE"}
                if (month=="07") {month_name = "JULY"}
                if (month=="08") {month_name = "AUG"}
                if (month=="09") {month_name = "SEPT"}
                if (month=="10") {month_name = "OCT"}
                if (month=="11") {month_name = "NOV"}
                if (month=="12") {month_name = "DEC"}
                return month_name
            },

            inOrder(){     
                const datesX = this.$store.state.dates;
                const years = new Object;

                datesX.forEach(element => {
                    var d = element.date;
                    var year = d.substring(0,4);
                    var month = d.substring(5,7);
                    var day = d.substring(8,10);   
                    if (!years.hasOwnProperty(year)){
                       years[year] = new Object; 
                    }
                    if (!years[year].hasOwnProperty(month)){
                       years[year][month] = []; 
                    }
                    if (!years[year][month].includes(day)){
                       years[year][month].push(day); 
                    }
                });
                //console.log(Object.keys(years[2018]).sort());
                return years                            
            }  
        },
        created() { 
            this.$store.dispatch('getDates');
        }
    }

    const scroll_element = function(direction,element){
        var properties = element.getBoundingClientRect();
        var scrollAmount = 0;
        var slideTimer = setInterval(function(){
            if (direction=="left"){ element.scrollLeft -= 20;
            }else{ element.scrollLeft += 20;}
            
            scrollAmount += 20;
            if(scrollAmount >= properties.width/2){ window.clearInterval(slideTimer);}
        }, 20); //cada cuantos milisegundos avanza
    };

    const check_scroll_button = function(scroll_element,btnLeft,btnRight){
        var maxScrollLeft = scroll_element.scrollWidth - scroll_element.clientWidth;
        
        if (scroll_element.scrollLeft==0){btnLeft.classList.add("no-visible")
        }else{ btnLeft.classList.remove("no-visible")}
        
        if (scroll_element.scrollLeft==maxScrollLeft){ btnRight.classList.add("no-visible")
        }else{ btnRight.classList.remove("no-visible")}
    }

    document.addEventListener("DOMContentLoaded", function(event) {
        console.log("DOM fully loaded and parsed");
        var timeline  = document.getElementById("timeline-years");    
        var btnRight = document.querySelector(".right.scroll"); 
        var btnLeft = document.querySelector(".left.scroll"); 
        //Cuando hacen click en los scroll buttons
        btnRight.onclick = function(){ scroll_element("rigth",timeline)}
        btnLeft.onclick = function(){ scroll_element("left",timeline)}
        //Cuando usan los scroll buttons
        timeline.addEventListener('scroll', function (event) {
            check_scroll_button(timeline,btnLeft,btnRight)
        });
        //cuando cambia tamaño de TIMELINE
        window.addEventListener('resize', function(event){
            check_scroll_button(timeline,btnLeft,btnRight)
        });
    });
</script>

<style scoped>
.no-visible{
    display: none;
}

#dates-bar {
    background-color: var(--primary-bg-color);
    display: grid;
    grid-area: dates;
    grid-template-areas: "date-selected timeline-years";
    grid-template-columns: 18% 82%;
    height: 94px;
    position: relative;
/*    margin-bottom: 20px;*/
    z-index: 10;
}

#date-selected {
    align-content: center;
    background-color: var(--secondary-bg-color);
    display: flex;
    flex-direction: column;
    font-size: 3vw;
    grid-area: date-selected;
    justify-content: center;
    padding: 5px;
}

#timeline-years {
    display: flex;
    overflow-x: hidden;
}

.timeline-year {
    border-left: 6px solid black;
    display: block;
}
.year.value{
    padding-left: 2%;
    text-align: left;
}

.timeline-months{
    display: flex;
}
.timeline-month{
    border-left: 4px solid brown;   
}
.month.value{
    padding-left: 10%;
}

.timeline-days{
    display: flex;
}
.day.value{
    border-left: 2px solid grey;
    padding-left: 2%;
    width: 50px;
}

.value{ 
    height: 30px;
    text-align: left;
}

.year.value:hover {
    background-color: #3BB359;
}
.month.value:hover {
    background-color: #38C986;
}
.day.value:hover{
    background-color: var(--hover-color);
    cursor: pointer;
}

.day.value.active {
    background-color: #517ddb;
}

.scroll{
    align-self: center;
    border-radius: 12px;
    border: 0px;
    height: 50%;
    position: absolute;
    opacity: 30%; 
    width: 30px;
    outline: none;
}

.scroll:hover{
    cursor: pointer;
    opacity: 100%;
}

.right.scroll{
    right: 0%;
}


</style>