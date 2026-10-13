<script setup lang="ts">

import Card from "../components/ui-components/Card.vue"
import Button from "../components/ui-components/Button.vue"
import {useRouter} from "vue-router";
import { ref} from 'vue'
import {supabase} from "../lib/supabaseClient.ts";

const email = ref<string>('')
const password = ref<string>('')
const username = ref<string>('')
const router = useRouter();

async function signUpNewUser() {
   await supabase.auth.signUp({
    email: email.value,
    password: password.value,
     options: {
       data: { display_name: username.value },
     }
  }).then((data) => {
     console.log(data)
     if (data?.error?.code== "weak_password"){
       errorRef.value = true
       return;
     }
     errorRef.value = false
    router.push('/portfolio')
   }).catch(e => {
     console.log(e)
   })
}

const errorRef = ref<boolean>(false);

</script>

<template>
  <div class="flex h-screen items-center justify-center -mt-32 w-auto">
    <Card title="Sign up" width="20rem">
      <div class="py-2">
        <p>Email</p>
        <input v-model="email" type="text" class="w-full bg-border border border-text-muted rounded text-text pl-1" placeholder="Email" />
      </div>
      <div class="py-2">
        <p>Username</p>
        <input v-model="username" type="text" class="w-full bg-border border border-text-muted rounded text-text pl-1" placeholder="Username" />
      </div>

      <div class="py-2">
        <p>Password</p>
        <input v-model="password" type="password" class="w-full bg-border border border-text-muted rounded text-text pl-1" placeholder="Password" />
      </div>
      <div class="py-2">
        <p v-if="errorRef" class="text-loss pb-2">Password needs 8 characters. capital, lowercase, numbers and a special symbol </p>
        <Button label="Sign up" variant="primary" class="h-8 w-full" @click="signUpNewUser()"/>
      </div>
      <hr/>
      <div class="py-2">
        <p>You have an Account?</p>
        <Button label="Login" variant="primary" class="h-8 w-full" @click="router.push('/login')"/>
      </div>

    </Card>
  </div>
</template>

<style scoped>

</style>