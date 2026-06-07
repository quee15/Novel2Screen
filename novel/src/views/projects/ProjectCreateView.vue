<script setup lang="ts">
import { computed, ref } from 'vue';
import {
  Bell,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clapperboard,
  FileCode2,
  FolderOpen,
  GitBranch,
  LayoutDashboard,
  Network,
  Plus,
  Search,
  Settings,
  Sparkles,
  UploadCloud,
  WandSparkles,
} from 'lucide-vue-next';

const selectedFileName = ref('长夜余火.txt');
const selectedFormat = ref('短剧');

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: true, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const formats = ['电影', '电视剧', '短剧', '动漫'];

const pipeline = [
  { label: '文本解析', value: '已完成', done: true },
  { label: '章节拆分', value: '82%', done: false },
  { label: '人物抽取', value: '待开始', done: false },
  { label: '剧本改编', value: '待确认', done: false },
];

const featureCards = [
  { title: '小说解析', desc: 'TXT / DOCX章节识别与清洗', accent: 'indigo' },
  { title: '人物关系', desc: '自动抽取角色身份与关系', accent: 'green' },
  { title: '故事图谱', desc: '事件、地点、时间线结构化', accent: 'amber' },
  { title: 'AI校审', desc: '一致性、完整性与节奏评分', accent: 'rose' },
  { title: '分镜生成', desc: '镜头、景别、光线与时长建议', accent: 'cyan' },
  { title: 'YAML导出', desc: '按统一Schema导出结构化文件', accent: 'violet' },
];

const recentProjects = [
  { name: '长夜余火', status: '解析中', chapter: '第 18 章', score: 86 },
  { name: '雾都信使', status: '待校审', chapter: '第 42 章', score: 78 },
  { name: '星港旧梦', status: '可导出', chapter: '全书完成', score: 91 },
];

const uploadCopy = computed(() => (selectedFileName.value ? selectedFileName.value : '拖拽 TXT / DOCX 到这里'));

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    selectedFileName.value = file.name;
  }
}
</script>

<template>
  <div class="workspace-shell">
    <aside class="sidebar" aria-label="主导航">
      <RouterLink to="/" class="brand" aria-label="返回首页">
        <div class="brand-mark">
          <BookOpenText :size="24" />
        </div>
        <div>
          <strong>ScriptAI</strong>
          <span>小说剧本工作台</span>
        </div>
        <span class="home-link-label">返回首页</span>
      </RouterLink>

      <nav class="nav-list">
        <RouterLink v-for="item in navItems" :key="item.label" :to="item.path" class="nav-item" :class="{ active: item.active }">
          <component :is="item.icon" :size="18" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-status">
        <span>本月额度</span>
        <strong>18 / 30</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索项目、人物或章节" placeholder="搜索项目、人物或章节" />
        </div>
        <div class="topbar-actions">
          <button class="icon-button" aria-label="通知">
            <Bell :size="18" />
          </button>
          <button class="icon-button" aria-label="设置">
            <Settings :size="18" />
          </button>
          <button class="primary-button">
            <Plus :size="18" />
            新项目
          </button>
        </div>
      </header>

      <section class="page-heading">
        <div>
          <p class="eyebrow">第一步：导入小说</p>
          <h1>创建剧本项目</h1>
          <p>上传小说后，系统会自动拆分章节、抽取人物和事件，并生成可编辑的剧本工作流。</p>
        </div>
        <button class="ghost-button">
          <WandSparkles :size="18" />
          查看解析规则
        </button>
      </section>

      <section class="creation-grid" aria-label="项目创建区域">
        <div class="upload-panel">
          <div class="section-title">
            <div>
              <span>小说文件</span>
              <h2>上传并解析文本</h2>
            </div>
            <span class="status-pill">Mock预览</span>
          </div>

          <label class="upload-zone">
            <input type="file" accept=".txt,.doc,.docx" @change="onFileChange" />
            <UploadCloud :size="34" />
            <strong>{{ uploadCopy }}</strong>
            <span>支持 TXT、DOC、DOCX，建议单次不超过 5MB</span>
          </label>

          <div class="form-row">
            <label>
              项目名称
              <input value="长夜余火 - 短剧改编" aria-label="项目名称" />
            </label>
            <label>
              目标集数
              <input value="24" aria-label="目标集数" />
            </label>
          </div>

          <div class="format-control" aria-label="剧本风格">
            <button
              v-for="format in formats"
              :key="format"
              :class="{ selected: selectedFormat === format }"
              @click="selectedFormat = format"
            >
              {{ format }}
            </button>
          </div>

          <div class="pipeline-list">
            <div v-for="step in pipeline" :key="step.label" class="pipeline-item">
              <CheckCircle2 :size="18" :class="{ muted: !step.done }" />
              <span>{{ step.label }}</span>
              <strong>{{ step.value }}</strong>
            </div>
          </div>

          <button class="wide-button">
            <Sparkles :size="18" />
            开始AI解析
          </button>
        </div>

        <aside class="insight-panel">
          <div class="section-title">
            <div>
              <span>解析预览</span>
              <h2>当前任务概览</h2>
            </div>
          </div>

          <div class="metric-grid">
            <div>
              <span>预计字数</span>
              <strong>48.6万</strong>
            </div>
            <div>
              <span>章节</span>
              <strong>126</strong>
            </div>
            <div>
              <span>角色</span>
              <strong>37</strong>
            </div>
            <div>
              <span>场景</span>
              <strong>214</strong>
            </div>
          </div>

          <div class="quality-preview">
            <div class="score-ring">
              <strong>86</strong>
              <span>质量预估</span>
            </div>
            <div>
              <h3>适合短剧改编</h3>
              <p>冲突密度较高，人物关系清晰。建议优先校验时间线和关键场景连续性。</p>
            </div>
          </div>

          <div class="mini-map" aria-label="故事结构预览">
            <span class="node n1">人物</span>
            <span class="node n2">事件</span>
            <span class="node n3">地点</span>
            <span class="node n4">时间</span>
            <i class="line l1" />
            <i class="line l2" />
            <i class="line l3" />
          </div>
        </aside>
      </section>

      <section class="feature-section" aria-label="功能入口">
        <article v-for="card in featureCards" :key="card.title" class="feature-card" :class="card.accent">
          <div>
            <h3>{{ card.title }}</h3>
            <p>{{ card.desc }}</p>
          </div>
          <ChevronRight :size="18" />
        </article>
      </section>

      <section class="recent-section" aria-label="最近项目">
        <div class="section-title">
          <div>
            <span>最近项目</span>
            <h2>继续正在处理的剧本</h2>
          </div>
        </div>

        <div class="project-table">
          <div class="table-row table-head">
            <span>项目</span>
            <span>状态</span>
            <span>进度</span>
            <span>评分</span>
          </div>
          <div v-for="project in recentProjects" :key="project.name" class="table-row">
            <strong>{{ project.name }}</strong>
            <span>{{ project.status }}</span>
            <span>{{ project.chapter }}</span>
            <span>{{ project.score }}</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
