<script setup>
import { computed } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";

import { navigationItems } from "./config/navigation";

const route = useRoute();

const currentPage = computed(() => {
  return navigationItems.find((item) => item.name === route.name) ?? navigationItems[0];
});
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand-panel">
        <p class="brand-kicker">Vue3 Scaffold</p>
        <h1>Novel2Screen</h1>
        <p>面向 FastAPI、Novel Parser 与 LLM Service 的正式前端骨架。</p>
      </div>

      <nav class="nav-list" aria-label="Vue3 工作区导航">
        <RouterLink
          v-for="item in navigationItems"
          :key="item.name"
          :to="item.path"
          class="nav-item"
          active-class="active"
        >
          <span class="nav-index">{{ item.index }}</span>
          <span class="nav-copy">
            <strong>{{ item.label }}</strong>
            <small>{{ item.eyebrow }}</small>
          </span>
        </RouterLink>
      </nav>

      <section class="sidebar-note">
        <p class="sidebar-label">后端对接方向</p>
        <ul>
          <li>FastAPI 作为统一 API 层</li>
          <li>Novel Parser 负责原文解析</li>
          <li>LLM Service 负责改编、审校与分镜</li>
          <li>YAML Export 对齐 `schema_design.md`</li>
        </ul>
      </section>
    </aside>

    <main class="main-stage">
      <header class="hero">
        <div>
          <p class="hero-eyebrow">{{ currentPage.eyebrow }}</p>
          <h2>{{ currentPage.label }}</h2>
          <p>{{ currentPage.description }}</p>
        </div>
        <div class="hero-tags">
          <span class="hero-tag">Vue3</span>
          <span class="hero-tag">Pinia</span>
          <span class="hero-tag">Vue Router</span>
          <span class="hero-tag">Axios + FastAPI</span>
        </div>
      </header>

      <RouterView />
    </main>
  </div>
</template>
