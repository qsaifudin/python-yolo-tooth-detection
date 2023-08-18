<template>
  <v-app>
    <v-main class="bg">
      <Home />
    </v-main>
  </v-app>
</template>

<script setup>
import Home from "@/components/Home.vue";
</script>
<style>
.bg {
  background: url("img/bg1.jpg") center center / cover no-repeat;
  background-size: auto, auto;
}
</style>
