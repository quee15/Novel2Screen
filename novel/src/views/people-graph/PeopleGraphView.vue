<script setup lang="ts">
import {
  Bell,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clapperboard,
  Download,
  FileCode2,
  Filter,
  GitBranch,
  LayoutDashboard,
  Maximize2,
  Network,
  PanelRightOpen,
  RefreshCw,
  Search,
  Settings,
  SlidersHorizontal,
  Sparkles,
  UploadCloud,
  UserRoundCheck,
  UserRoundSearch,
  UsersRound,
  ZoomIn,
  ZoomOut,
} from 'lucide-vue-next';

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: true, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const filters = ['全部人物', '主线人物', '高频互动', '关系冲突'];

const graphNodes = [
  { name: '沈澜', role: '主角', type: 'protagonist', x: 47, y: 47 },
  { name: '顾闻舟', role: '同盟 / 导师', type: 'ally', x: 29, y: 28 },
  { name: '林照夜', role: '对手', type: 'rival', x: 69, y: 28 },
  { name: '乔以宁', role: '搭档', type: 'ally', x: 25, y: 68 },
  { name: '秦砚', role: '隐藏反派', type: 'risk', x: 70, y: 68 },
  { name: '许安白', role: '关键证人', type: 'neutral', x: 50, y: 79 },
  { name: '陆衡', role: '旧友', type: 'neutral', x: 14, y: 47 },
  { name: '闻青', role: '亲属', type: 'family', x: 84, y: 47 },
];

const graphEdges = [
  { className: 'edge-main e1', label: '信任' },
  { className: 'edge-main e2', label: '冲突' },
  { className: 'edge-main e3', label: '搭档' },
  { className: 'edge-main e4', label: '背叛' },
  { className: 'edge-soft e5', label: '旧识' },
  { className: 'edge-soft e6', label: '证词' },
  { className: 'edge-soft e7', label: '亲属' },
];

const metrics = [
  { label: '人物总数', value: '37', desc: '主线 12 人' },
  { label: '关系边', value: '86', desc: '强关系 24 条' },
  { label: '冲突关系', value: '9', desc: '需优先校审' },
  { label: '抽取置信度', value: '92%', desc: '基于 126 章' },
];

const relations = [
  { target: '顾闻舟', type: '信任上升', evidence: '第 12 章、第 24 章多次共同推进调查' },
  { target: '林照夜', type: '敌对冲突', evidence: '第 31 章出现直接目标冲突' },
  { target: '秦砚', type: '隐藏背叛', evidence: '第 58 章行为与前文动机不一致' },
];

const appearances = [
  { chapter: '第 001 章', scene: '雨夜车站', effect: '首次登场' },
  { chapter: '第 018 章', scene: '地下档案室', effect: '关系反转' },
  { chapter: '第 064 章', scene: '旧城天台', effect: '主线抉择' },
];

const reviewItems = [
  { title: '身份称谓不一致', level: '中', desc: '沈澜在前 20 章被称为调查员，后文出现记者称谓。' },
  { title: '关系转折缺少铺垫', level: '高', desc: '秦砚从同盟转为背叛的证据集中在后半段。' },
  { title: '关键人物出场间隔过长', level: '低', desc: '许安白在第 21 章后间隔 18 章再次出现。' },
];
</script>

<template>
  <div class="workspace-shell people-page">
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
        <span>图谱抽取</span>
        <strong>92% 置信度</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索人物、关系或章节证据" placeholder="搜索人物、关系或章节证据" />
        </div>
        <div class="topbar-actions">
          <button class="icon-button" aria-label="通知">
            <Bell :size="18" />
          </button>
          <button class="icon-button" aria-label="设置">
            <Settings :size="18" />
          </button>
          <button class="primary-button">
            <Sparkles :size="18" />
            重新抽取
          </button>
        </div>
      </header>

      <section class="page-heading people-heading">
        <div>
          <p class="eyebrow">人物图谱</p>
          <h1>把角色、身份和关系变化变成可检查网络</h1>
          <p>从小说正文中抽取人物节点、关系边和章节证据，帮助剧本改编时检查角色一致性与冲突强度。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <Filter :size="18" />
            筛选规则
          </button>
          <button class="ghost-button">
            <Download :size="18" />
            导出图谱
          </button>
        </div>
      </section>

      <section class="people-metrics" aria-label="人物图谱统计">
        <article v-for="metric in metrics" :key="metric.label" class="people-metric-card">
          <span>{{ metric.label }}</span>
          <strong>{{ metric.value }}</strong>
          <p>{{ metric.desc }}</p>
        </article>
      </section>

      <section class="people-workbench">
        <div class="graph-panel">
          <div class="graph-toolbar">
            <div class="segmented-control" aria-label="图谱筛选">
              <button v-for="filter in filters" :key="filter" :class="{ selected: filter === '主线人物' }">
                {{ filter }}
              </button>
            </div>
            <div class="graph-actions">
              <button class="icon-button" aria-label="缩小">
                <ZoomOut :size="17" />
              </button>
              <button class="icon-button" aria-label="放大">
                <ZoomIn :size="17" />
              </button>
              <button class="icon-button" aria-label="适配画布">
                <Maximize2 :size="17" />
              </button>
              <button class="icon-button" aria-label="刷新布局">
                <RefreshCw :size="17" />
              </button>
            </div>
          </div>

          <div class="graph-canvas" aria-label="人物关系图谱画布">
            <i v-for="edge in graphEdges" :key="edge.className" class="graph-edge" :class="edge.className">
              <span>{{ edge.label }}</span>
            </i>

            <button
              v-for="node in graphNodes"
              :key="node.name"
              class="person-node"
              :class="node.type"
              :style="{ left: `${node.x}%`, top: `${node.y}%` }"
            >
              <strong>{{ node.name }}</strong>
              <span>{{ node.role }}</span>
            </button>

            <div class="graph-legend">
              <span><i class="legend-dot protagonist" />主角</span>
              <span><i class="legend-dot ally" />同盟</span>
              <span><i class="legend-dot rival" />对手</span>
              <span><i class="legend-dot risk" />风险</span>
            </div>
          </div>
        </div>

        <aside class="character-panel">
          <div class="section-title">
            <div>
              <span>当前人物</span>
              <h2>沈澜</h2>
            </div>
            <PanelRightOpen :size="20" />
          </div>

          <div class="character-card">
            <div class="avatar-tile">
              <UsersRound :size="30" />
            </div>
            <div>
              <strong>主角 · 调查员</strong>
              <p>贯穿全书 96 个章节，推动 14 个关键事件，是剧本改编的一号视角人物。</p>
            </div>
          </div>

          <div class="relation-list">
            <div class="panel-subtitle">
              <UserRoundSearch :size="17" />
              <strong>强关系证据</strong>
            </div>
            <article v-for="relation in relations" :key="relation.target" class="relation-item">
              <div>
                <strong>{{ relation.target }}</strong>
                <span>{{ relation.type }}</span>
              </div>
              <p>{{ relation.evidence }}</p>
            </article>
          </div>

          <div class="appearance-list">
            <div class="panel-subtitle">
              <UserRoundCheck :size="17" />
              <strong>关键出场</strong>
            </div>
            <article v-for="item in appearances" :key="item.chapter" class="appearance-item">
              <span>{{ item.chapter }}</span>
              <strong>{{ item.scene }}</strong>
              <p>{{ item.effect }}</p>
            </article>
          </div>
        </aside>
      </section>

      <section class="graph-review-section">
        <div class="section-title">
          <div>
            <span>一致性检查</span>
            <h2>关系图谱发现的问题</h2>
          </div>
          <button class="ghost-button compact-button">
            <SlidersHorizontal :size="16" />
            校审维度
          </button>
        </div>

        <div class="review-grid">
          <article v-for="item in reviewItems" :key="item.title" class="review-card">
            <div>
              <strong>{{ item.title }}</strong>
              <span>{{ item.level }}风险</span>
            </div>
            <p>{{ item.desc }}</p>
            <button>
              查看证据
              <ChevronRight :size="16" />
            </button>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>
