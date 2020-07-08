<template>
    <div id="dates-bar">
        <div id='date-selected'>
            {{ selectedDate }}
        </div>
        <div id="timeline">
            <div class="timeline-elem" 
                v-for="date in dates"
                v-bind:key="date.date"
                :class="{ 'active': date.date === selectedDate }"
                @click="handleSelectDate(date)"
            >
                {{ date.date }}
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Dates",
    data: function () {
        return {
            selectedDate: null,
            dates: ''
        }
    },
    methods: {
        handleSelectDate(date){
            this.selectedDate = date.date;
            this.$emit('changeDate', this.selectedDate);
        }
    },
    created() {
        axios
        .get(process.env.VUE_APP_BE_URL + "/dates", {
            headers: {
                'Authorization': process.env.VUE_APP_BE_API_TOKEN
            }
        })
        .then(response => { this.dates = response.data; this.selectedDate = this.dates[0].date })
        .catch(e => { this.errors.push(e)})
    }
}
</script>

<style scoped>
#dates-bar {
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