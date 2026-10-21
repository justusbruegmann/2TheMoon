<script setup lang="ts">
import NotificationContainer from "./components/ui-components/NotificationContainer.vue";
import Header from "./components/Header.vue";
import {useRoute} from "vue-router";
import {computed} from "vue";
const route = useRoute();

const currentPath = computed(() => String(route.name).split(" ")[2]);

</script>

<template>
<Header :label="currentPath"/>

  <notification-container/>

  <router-view/>
</template>
