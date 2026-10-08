<script setup lang="ts">
import {isUserLoggedIn} from "../scripts/userManagement.ts";

import Button from "./ui-components/Button.vue";
import {ref} from "vue";

defineProps<{
  label: string;
}>()

const isLoggedIn = ref<boolean>(isUserLoggedIn());

//TODO: Change it to real Login
function handleClick() {
  if (isLoggedIn.value) {
    localStorage.setItem("user", "false");
    isLoggedIn.value = false;
  } else {
    localStorage.setItem("user", "true");
    isLoggedIn.value = true;
  }
}

function handleRegister() {
  localStorage.setItem("user", "true");
  isLoggedIn.value = true;
}

</script>

<template>
  <div class="bg-surface w-screen h-16 ">
    <div class="flex flex-row  w-full">
      <div class="flex items-center">
        <img src="../assets/logo.png" alt="2TheMoon Logo" class="w-12 m-2"/>
        <div class="text-text">{{ label }}</div>
      </div>
      <div class="ml-auto flex flex-row">
        <nav class="flex flex-row w-full mt-4.5 mr-4 gap-2">
          <router-link class="text-text-muted" to="/portfolio">Portfolio</router-link>
          <router-link class="text-text-muted" to="/stocks">Stocks</router-link>
          <router-link class="text-text-muted" to="/leaderboard">Leaderboard</router-link>
        </nav>
        <Button variant="ghost" class="mt-1.5 mr-4 w-20" :label='isLoggedIn ?"Logout" : "Login"' @click="handleClick"/>
        <Button v-if="!isLoggedIn" class="mt-1.5 mr-4 w-20" label="Register" @click="handleRegister"/>
      </div>
    </div>

  </div>
</template>

<style scoped>

</style>