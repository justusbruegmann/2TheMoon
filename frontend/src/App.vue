<script setup lang="ts">

</script>

<template>
<nav class="p-4 gap-4">
  <router-link to="/portfolio">Portfolio</router-link>
  <router-link to="/stocks/TSLA">TSLA</router-link>
  <router-link to="/stocks">Stocks</router-link>
  <router-link to="/login">Login</router-link>
  <router-link to="/register">Register</router-link>
</nav>

  <router-view/>
</template>
