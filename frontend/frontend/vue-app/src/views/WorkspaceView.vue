<script setup>
import { storeToRefs } from "pinia";

import SectionCard from "../components/SectionCard.vue";
import { useWorkspaceStore } from "../stores/workspace";

const workspaceStore = useWorkspaceStore();
const { project, capabilities, backendChain } = storeToRefs(workspaceStore);
</script>

<template>
  <section class="view-grid">
    <SectionCard
      eyebrow="Project Workspace"
      title="工程化前端起点"
      description="这里对应未来 Vue3 应用的总览页，用来展示项目、任务和核心能力覆盖。"
    >
      <div class="key-value-grid">
        <div>
          <span>project.id</span>
          <strong>{{ project.id }}</strong>
        </div>
        <div>
          <span>title</span>
          <strong>{{ project.title }}</strong>
        </div>
      </div>
    </SectionCard>

    <SectionCard
      eyebrow="Core Capabilities"
      title="根目录 README 对齐"
      description="后续正式开发时，所有视图都要继续围绕这 9 项核心能力展开。"
    >
      <ul class="plain-list">
        <li v-for="item in capabilities" :key="item">{{ item }}</li>
      </ul>
    </SectionCard>

    <SectionCard
      eyebrow="Architecture Chain"
      title="对接 FastAPI 的调用链"
      description="前端通过 API 调用 FastAPI，再分发到 Novel Parser、LLM Service、YAML Export 等模块。"
    >
      <div class="tag-list">
        <span v-for="item in backendChain" :key="item" class="tag">{{ item }}</span>
      </div>
    </SectionCard>
  </section>
</template>
