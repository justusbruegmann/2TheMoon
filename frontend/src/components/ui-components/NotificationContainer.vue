<script setup lang="ts">
import {notifications} from "../../scripts/notify";
import type {Status} from "../../types/notifications.ts";



function getNotificationClasses(status: Status): string {
  const statusClasses: Record<Status, string> = {
    success: "border-gain bg-surface text-gain",
    error: "border-loss bg-surface text-loss",
    warning: "border-warning bg-surface text-warning",
    info: "border-primary bg-surface text-primary",
  };

  return `rounded-lg border border-l-4 p-4 shadow-md ${statusClasses[status]}`;
}

</script>

<template>
  <div class="fixed right-4 top-20 z-100 flex w-80 flex-col gap-3">
    <div v-for="notification in notifications" :key="notification.id" :class="getNotificationClasses(notification.status)">
      <h3 class="font-semibold">{{ notification.title }}</h3>
      <p class="mt-1 text-sm text-text-muted">{{ notification.message }}</p>
    </div>
  </div>
</template>

<style scoped>

</style>