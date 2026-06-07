<script setup lang="ts">
import {
  Bell,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  Clipboard,
  ClipboardCheck,
  Clapperboard,
  Code2,
  Copy,
  Download,
  FileArchive,
  FileCheck2,
  FileCode2,
  GitBranch,
  LayoutDashboard,
  ListChecks,
  Network,
  PanelRightOpen,
  PlayCircle,
  Search,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  UploadCloud,
} from 'lucide-vue-next';

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: true, path: '/export' },
];

const exportStats = [
  { label: '导出场次', value: '58', desc: '包含 186 个镜头' },
  { label: 'Schema版本', value: 'v1.4', desc: '剧本标准结构' },
  { label: '校验通过', value: '97%', desc: '2 项建议修复' },
  { label: '预计大小', value: '842KB', desc: 'YAML + 元数据' },
];

const exportRanges = ['全剧本', '当前章节', '选中场次', '仅分镜'];
const modules = [
  { label: '剧本文本', checked: true },
  { label: '人物关系', checked: true },
  { label: '故事图谱', checked: true },
  { label: '分镜脚本', checked: true },
  { label: '校审结果', checked: false },
];

const yamlPreview = `project:
  id: scriptai-2026-042
  title: 天幕回声
  schema: scriptai.yaml.v1.4
  target_format: short_drama

scenes:
  - id: S42
    title: 档案室失火
    location: 旧城地下档案室
    time: 夜
    characters:
      - 沈澜
      - 顾闻舟
      - 秦砚
    summary: >
      主角发现关键档案被提前转移，
      火势迫使众人离开档案室。
    shots:
      - id: S42-01
        size: 远景
        movement: 缓慢推进
        duration: 6
      - id: S42-03
        size: 特写
        movement: 静止转轻推
        duration: 5

validation:
  score: 97
  warnings:
    - path: scenes[42].timeline
      message: 三日后时间跳转建议补充过渡`;

const validations = [
  { title: '字段完整性', state: '通过', desc: '项目、场次、镜头和人物字段均符合 Schema。' },
  { title: '引用一致性', state: '通过', desc: '人物、地点、章节引用均可追溯到图谱数据。' },
  { title: '时间线提示', state: '建议', desc: 'S42 的三日后时间跳转建议加入 transition 字段。' },
];

const packageItems = [
  { title: 'script.yaml', desc: '结构化剧本主体' },
  { title: 'characters.yaml', desc: '人物和关系索引' },
  { title: 'shotlist.yaml', desc: '分镜镜头表' },
  { title: 'review_report.yaml', desc: 'AI校审结果' },
];
</script>

<template>
  <div class="workspace-shell yaml-page">
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
        <span>导出状态</span>
        <strong>Schema v1.4</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索导出字段、场次或 Schema" placeholder="搜索导出字段、场次或 Schema" />
        </div>
        <div class="topbar-actions">
          <button class="icon-button" aria-label="通知">
            <Bell :size="18" />
          </button>
          <button class="icon-button" aria-label="设置">
            <Settings :size="18" />
          </button>
          <button class="primary-button">
            <Download :size="18" />
            下载YAML
          </button>
        </div>
      </header>

      <section class="page-heading yaml-heading">
        <div>
          <p class="eyebrow">YAML导出</p>
          <h1>按统一 Schema 交付结构化剧本文件</h1>
          <p>选择导出范围和模块，预览 YAML 结构，完成 Schema 校验后下载给后端、制片系统或自动化工作流使用。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <Copy :size="18" />
            复制预览
          </button>
          <button class="ghost-button">
            <PlayCircle :size="18" />
            运行校验
          </button>
        </div>
      </section>

      <section class="yaml-stats" aria-label="YAML导出统计">
        <article v-for="stat in exportStats" :key="stat.label" class="yaml-stat-card">
          <span>{{ stat.label }}</span>
          <strong>{{ stat.value }}</strong>
          <p>{{ stat.desc }}</p>
        </article>
      </section>

      <section class="yaml-workbench">
        <aside class="export-config-panel">
          <div class="section-title">
            <div>
              <span>导出配置</span>
              <h2>选择范围和模块</h2>
            </div>
            <SlidersHorizontal :size="20" />
          </div>

          <div class="range-control" aria-label="导出范围">
            <button v-for="range in exportRanges" :key="range" :class="{ selected: range === '全剧本' }">
              {{ range }}
            </button>
          </div>

          <div class="module-list">
            <label v-for="module in modules" :key="module.label">
              <input type="checkbox" :checked="module.checked" />
              <span>{{ module.label }}</span>
            </label>
          </div>

          <div class="schema-card">
            <Code2 :size="20" />
            <div>
              <strong>scriptai.yaml.v1.4</strong>
              <p>包含 project、characters、scenes、shots、validation 五个一级结构。</p>
            </div>
          </div>
        </aside>

        <div class="yaml-preview-panel">
          <div class="code-toolbar">
            <div>
              <span>YAML Preview</span>
              <strong>script.yaml</strong>
            </div>
            <div class="script-tools">
              <button class="ghost-button compact-button">
                <Clipboard :size="16" />
                复制
              </button>
              <button class="ghost-button compact-button">
                <FileCheck2 :size="16" />
                格式化
              </button>
            </div>
          </div>

          <pre class="yaml-code"><code>{{ yamlPreview }}</code></pre>
        </div>

        <aside class="yaml-check-panel">
          <div class="section-title">
            <div>
              <span>Schema校验</span>
              <h2>导出前检查</h2>
            </div>
            <PanelRightOpen :size="20" />
          </div>

          <div class="validation-summary">
            <ShieldCheck :size="28" />
            <div>
              <strong>可导出</strong>
              <p>当前文件通过主要校验，仍有 1 条建议可优化。</p>
            </div>
          </div>

          <div class="validation-list">
            <article v-for="item in validations" :key="item.title">
              <CheckCircle2 :size="18" />
              <div>
                <strong>{{ item.title }}</strong>
                <p>{{ item.desc }}</p>
              </div>
              <span>{{ item.state }}</span>
            </article>
          </div>
        </aside>
      </section>

      <section class="package-section">
        <div class="section-title">
          <div>
            <span>导出包内容</span>
            <h2>将生成的文件</h2>
          </div>
          <FileArchive :size="20" />
        </div>

        <div class="package-grid">
          <article v-for="item in packageItems" :key="item.title">
            <FileCode2 :size="20" />
            <div>
              <strong>{{ item.title }}</strong>
              <p>{{ item.desc }}</p>
            </div>
            <ChevronRight :size="16" />
          </article>
        </div>

        <button class="wide-button yaml-download-button">
          <Sparkles :size="18" />
          生成并下载导出包
        </button>
      </section>
    </main>
  </div>
</template>
