<template>
    <div id="menu-bar">
        <div class="filter" 
            v-for="filter in filters"
            v-bind:key="filter._id"
        >
            {{ filter.longName }}
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Menu",
    data: function () {
        return {
            filters: ''
        }
    },
    created() {
        axios
        .get(process.env.VUE_APP_BE_URL + "/filters", {
            headers: {
                'Authorization': process.env.VUE_APP_BE_API_TOKEN
            }
        })
        .then(response => { console.log(response); this.filters = response.data })
        .catch(e => { this.errors.push(e)})
    }
}
</script>

<style scoped>
#menu-bar {
    grid-area: menu;
    background-color: #d1dcda;
    display: block;
    z-index: 10;
}

.filter {
    padding: 2px;
    border-radius: 4%;
    background-color: #8cc07f;
}
</style>