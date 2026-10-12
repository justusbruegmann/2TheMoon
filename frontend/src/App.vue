<script setup lang="ts">
import Header from "./components/Header.vue";
import {useRoute} from "vue-router";
import {computed} from "vue";
const route = useRoute();

const currentPath = computed(() => String(route.name).split(" ")[2]);
</script>

<template>
<Header :label="currentPath"/>

  <router-view/>
</template>
