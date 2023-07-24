<template>
  <div>
    The information below is rendered from JSON data from <a href="http://127.0.0.1:5000/providers_data">localhost:5000/providers_data</a>
    <hr>
    <div v-for="provider in msg" :key="provider.id" class="tile">
        Provider ID:{{provider.id}} | Provider Name: {{ provider.name }}
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
    name: 'thread',
    data() {
        return {
            msg: [],
        }
    },
    methods: {
        getResponse() {
            const path = 'http://localhost:5000/providers_data';
            axios.get(path)
            .then ((res) => {
                console.log(res.data)
                this.msg = res.data.json_list;
            })
            .catch ((err) => {
                console.log(err)
            })
        },
    },
    created(){
        this.getResponse();
    }
}
</script>

<style>
.tile {
    border: 2px solid grey;
    width: 50%;
    text-align: left;
    display: inline-block;
    margin: 2px;
    padding: 5px;
    border-radius: 5px;
    background: rgba(111, 142, 125, 0.7);
}

</style>