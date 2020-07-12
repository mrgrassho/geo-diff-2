<template>
    <div id="dates-bar">
        <div id='date-selected'>
            {{ dateSelected }}
        </div>
        <div id="timeline">
            <div class="timeline-elem" 
                v-for="date in dates"
                v-bind:key="date.date"
                :class="{ 'active': date.date == dateSelected }"
                @click="changeDate(date.date)">
                {{ date.date }}
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
            ...mapActions(['getDates']) 
        },
        created() { 
            this.$store.dispatch('getDates');
        }
}
</script>

<style scoped>
#dates-bar {
    position: relative;
    grid-area: dates;
    background-color: #d1dcda;
    display: grid;
    grid-template-columns: 20% 80%;
    grid-template-areas: "date-selected timeline";
    margin-bottom: 3%;
    z-index: 10;
}

#date-selected {
    grid-area: date-selected;
    font-size: 3vw;
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
    padding: 5px;
    background-color: #8cc07f;
}

#timeline {
    grid-area: timeline;
    display: flex;
    overflow-x: scroll;
}

.timeline-elem {
    background-color: #8cc07f;
}

.timeline-elem:hover {
    background-color: #7de663;
}

.active {
    background-color: #517ddb;
}
</style>