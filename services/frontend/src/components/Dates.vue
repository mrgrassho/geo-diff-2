<template>
    <div id="dates-bar">
        <div class="date" 
            v-for="date in dates"
            v-bind:key="date.date"
        >
            {{ date.date }}
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Dates",
    data: function () {
        return {
            dates: ''
        }
    },
    mounted() {
        axios
        .get(process.env.VUE_APP_BE_URL + "/dates", {
            headers: {
                'Authorization': process.env.VUE_APP_BE_API_TOKEN
            }
        })
        .then(response => { this.dates = response.data })
        .catch(e => { this.errors.push(e)})
    }
}
</script>

<style scoped>
#dates-bar {
    background-color: #d1dcda;
    display: flex;
}

.date {
    padding: 5px;
    border-radius: 4%;
    background-color: #8cc07f;
}
</style>