<script setup lang="ts">
import * as userManagement from "../scripts/userManagement.ts";

import Button from "./ui-components/Button.vue";
import {computed, onMounted, ref} from "vue";
import {supabase} from "../lib/supabaseClient.ts";
import {useRouter} from "vue-router";

const router = useRouter();

defineProps<{
  label: string;
}>()

const isLoggedIn = ref<boolean>();

onMounted(async () => {
  isLoggedIn.value = await userManagement.isLoggedIn();
})

computed(() => {
 userManagement.isLoggedIn().then(e => isLoggedIn.value = e);
})


async function signOut() {
  await supabase.auth.signOut()
  isLoggedIn.value = false

}

//TODO: Change it to real Login
async function handleClick() {
  if (isLoggedIn.value) {
    await signOut();
  } else {
    router.push("/login");
  }
}

function handleRegister() {
  router.push("/register");
}

</script>

<template>
  <div class="bg-surface w-screen h-16 ">
    <div class="flex flex-row  w-full">
      <div class="flex items-center">
        <img src="../assets/logo.png" alt="2TheMoon Logo" class="w-12 m-2" @click="router.push('/')"/>
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