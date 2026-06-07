<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  eyebrow: {
    type: String,
    default: ""
  },
  description: {
    type: String,
    default: ""
  }
});
</script>

<template>
  <article class="section-card">
    <p v-if="eyebrow" class="section-card-eyebrow">{{ eyebrow }}</p>
    <h3>{{ title }}</h3>
    <p v-if="description" class="section-card-description">{{ description }}</p>
    <slot />
  </article>
</template>
