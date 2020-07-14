<template>
    <div id="menu-bar">
        <div class="filter" 
            v-for="filter in filters"
            v-bind:key="filter._id"
            :class="{ 'active': filter.name === filterSelected }"
            @click="changeFilter(filter.name)">
            {{ filter.longName }}
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
        }
    }
</script>

<style scoped>
#menu-bar {
    position: relative;
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

.filter:hover {
    background-color: #7de663;
}

.active {
    background-color: #517ddb;
}
</style>