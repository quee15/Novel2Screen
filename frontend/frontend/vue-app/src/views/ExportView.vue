<script setup>
import { buildYamlPreviewNotes } from "../utils/yamlPreview";

const notes = buildYamlPreviewNotes();
</script>

<template>
  <section class="view-grid">
    <article class="section-card">
      <p class="section-card-eyebrow">YAML Export</p>
      <h3>YAML剧本导出</h3>
      <p class="section-card-description">
        对应统一 Schema 的导出、校验和下载，后续接 FastAPI 导出接口。
      </p>

      <ul class="plain-list">
        <li v-for="note in notes" :key="note">{{ note }}</li>
      </ul>
    </article>
  </section>
</template>
