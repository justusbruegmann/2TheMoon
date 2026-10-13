<script setup lang="ts">

import Card from "../components/ui-components/Card.vue"
import Button from "../components/ui-components/Button.vue"
import {useRouter} from "vue-router";
import { ref} from 'vue'
import {supabase} from "../lib/supabaseClient.ts";

const email = ref<string>('')
const password = ref<string>('')
const router = useRouter();


//TODO: Header inplementation
//TODO: error when unsuccesfull With Team fly in or inside card
async function signInWithEmail() {
  await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  }).then((data: any) => {
    console.log(data)
    if (data?.error?.code == "invalid_credentials"){
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
 <Card title="Login" width="20rem">
   <div class="py-4">
     <p>Email</p>
     <input v-model="email" type="text" class="w-full bg-border border border-text-muted rounded text-text pl-1" placeholder="Email" />
   </div>

   <div class="py-4">
     <p>Password</p>
     <input v-model="password" type="password" class="w-full bg-border border border-text-muted rounded text-text pl-1" placeholder="Password" />
   </div>
   <div class="py-2">
     <p v-if="errorRef" class="text-loss pb-2">Invalid Credentials</p>
     <Button label="Login" variant="primary" class="h-8 w-full" @click="signInWithEmail()"/>
   </div>
   <p class="text-text-muted" >Forgot Password?</p>
   <hr/>
  <div class="py-2">
    <p>Do not have an Account?</p>
    <Button label="Sign up" variant="primary" class="h-8 w-full" @click="router.push('/register')"/>
  </div>

 </Card>
</div>
</template>

<style scoped>

</style>