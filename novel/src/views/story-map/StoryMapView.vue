<script setup lang="ts">
import {
  Bell,
  BookOpenText,
  CalendarClock,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clapperboard,
  Download,
  FileCode2,
  Filter,
  GitBranch,
  Hourglass,
  Layers3,
  LayoutDashboard,
  MapPin,
  Maximize2,
  Network,
  Route,
  ScanLine,
  Search,
  Settings,
  Sparkles,
  Split,
  UploadCloud,
  Waypoints,
  ZoomIn,
  ZoomOut,
} from 'lucide-vue-next';

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: true, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const mapLayers = ['事件', '地点', '时间', '章节'];

const storyStats = [
  { label: '关键事件', value: '58', desc: '主线事件 21 个' },
  { label: '地点节点', value: '34', desc: '高频场景 9 个' },
  { label: '时间锚点', value: '76', desc: '待确认 6 个' },
  { label: '因果链路', value: '112', desc: '强因果 38 条' },
];

const storyNodes = [
  { title: '雨夜车站', meta: '地点', type: 'place', x: 16, y: 50 },
  { title: '收到密信', meta: '事件', type: 'event', x: 32, y: 28 },
  { title: '旧城调查', meta: '事件', type: 'event', x: 48, y: 48 },
  { title: '档案室失火', meta: '事件', type: 'risk', x: 66, y: 28 },
  { title: '天台对峙', meta: '高潮', type: 'climax', x: 82, y: 50 },
  { title: '第18章', meta: '章节', type: 'chapter', x: 38, y: 72 },
  { title: '三日后', meta: '时间', type: 'time', x: 62, y: 72 },
];

const storyEdges = [
  { className: 'story-edge se1', label: '触发' },
  { className: 'story-edge se2', label: '追查' },
  { className: 'story-edge se3', label: '导致' },
  { className: 'story-edge se4', label: '升级' },
  { className: 'story-edge story-edge-soft se5', label: '发生于' },
  { className: 'story-edge story-edge-soft se6', label: '时间跳转' },
  { className: 'story-edge story-edge-soft se7', label: '归属章节' },
];

const timeline = [
  { chapter: '001-008', title: '引子与人物入局', state: '完成', desc: '沈澜收到密信，进入旧城调查线。' },
  { chapter: '009-026', title: '调查扩散', state: '完成', desc: '地点从车站扩展到档案室、地下市场。' },
  { chapter: '027-050', title: '冲突升级', state: '待确认', desc: '秦砚动机出现反转，需要补充因果证据。' },
  { chapter: '051-078', title: '真相暴露', state: '完成', desc: '档案室失火连接到天台对峙。' },
];

const selectedEvent = {
  title: '档案室失火',
  type: '关键转折事件',
  chapter: '第 42 章',
  place: '旧城地下档案室',
  time: '三日后夜间',
  summary: '主角一行发现关键档案被提前转移，随后档案室被人为纵火，故事从调查线转入追逃线。',
};

const evidence = [
  { label: '前置事件', value: '收到密信、旧城调查' },
  { label: '后续影响', value: '秦砚身份暴露、天台对峙' },
  { label: '涉及人物', value: '沈澜、顾闻舟、秦砚' },
];

const checks = [
  { title: '时间跳跃缺少说明', level: '中', desc: '第 41 章到第 42 章存在三日跳跃，正文缺少明显过渡。' },
  { title: '地点连续性良好', level: '低', desc: '车站、档案室、天台之间的移动路径清晰。' },
  { title: '因果链路强', level: '低', desc: '档案室失火直接推动后续追逃和身份反转。' },
];
</script>

<template>
  <div class="workspace-shell story-page">
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
        <span>故事结构</span>
        <strong>112 条链路</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索事件、地点、章节或时间" placeholder="搜索事件、地点、章节或时间" />
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
            生成故事图谱
          </button>
        </div>
      </header>

      <section class="page-heading story-heading">
        <div>
          <p class="eyebrow">故事图谱</p>
          <h1>把事件、地点与时间线连成故事知识网络</h1>
          <p>从章节中抽取关键事件、发生地点、时间锚点和因果关系，帮助剧本改编时检查剧情连续性。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <Filter :size="18" />
            关系筛选
          </button>
          <button class="ghost-button">
            <Download :size="18" />
            导出JSON
          </button>
        </div>
      </section>

      <section class="story-stats" aria-label="故事图谱统计">
        <article v-for="stat in storyStats" :key="stat.label" class="story-stat-card">
          <span>{{ stat.label }}</span>
          <strong>{{ stat.value }}</strong>
          <p>{{ stat.desc }}</p>
        </article>
      </section>

      <section class="story-workbench">
        <div class="story-map-panel">
          <div class="graph-toolbar">
            <div class="segmented-control" aria-label="图谱层级">
              <button v-for="layer in mapLayers" :key="layer" :class="{ selected: layer === '事件' }">
                {{ layer }}
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
              <button class="icon-button" aria-label="切换路径">
                <Route :size="17" />
              </button>
            </div>
          </div>

          <div class="story-canvas" aria-label="故事知识图谱画布">
            <i v-for="edge in storyEdges" :key="edge.className" :class="edge.className">
              <span>{{ edge.label }}</span>
            </i>

            <button
              v-for="node in storyNodes"
              :key="node.title"
              class="story-node"
              :class="node.type"
              :style="{ left: `${node.x}%`, top: `${node.y}%` }"
            >
              <strong>{{ node.title }}</strong>
              <span>{{ node.meta }}</span>
            </button>

            <div class="story-legend">
              <span><i class="legend-dot event" />事件</span>
              <span><i class="legend-dot place" />地点</span>
              <span><i class="legend-dot time" />时间</span>
              <span><i class="legend-dot risk" />冲突转折</span>
            </div>
          </div>
        </div>

        <aside class="story-detail-panel">
          <div class="section-title">
            <div>
              <span>当前事件</span>
              <h2>{{ selectedEvent.title }}</h2>
            </div>
            <Waypoints :size="20" />
          </div>

          <div class="event-summary-card">
            <div class="event-icon">
              <Split :size="28" />
            </div>
            <div>
              <strong>{{ selectedEvent.type }}</strong>
              <p>{{ selectedEvent.summary }}</p>
            </div>
          </div>

          <div class="event-meta-grid">
            <div>
              <CalendarClock :size="17" />
              <span>{{ selectedEvent.chapter }}</span>
            </div>
            <div>
              <MapPin :size="17" />
              <span>{{ selectedEvent.place }}</span>
            </div>
            <div>
              <Hourglass :size="17" />
              <span>{{ selectedEvent.time }}</span>
            </div>
          </div>

          <div class="evidence-list">
            <div class="panel-subtitle">
              <ScanLine :size="17" />
              <strong>事件证据</strong>
            </div>
            <article v-for="item in evidence" :key="item.label">
              <span>{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
            </article>
          </div>
        </aside>
      </section>

      <section class="timeline-workbench">
        <div class="story-timeline-panel">
          <div class="section-title">
            <div>
              <span>章节时间线</span>
              <h2>按故事阶段检查节奏</h2>
            </div>
            <button class="ghost-button compact-button">
              <Layers3 :size="16" />
              阶段视图
            </button>
          </div>

          <div class="story-timeline">
            <article v-for="item in timeline" :key="item.chapter" class="timeline-step">
              <span>{{ item.chapter }}</span>
              <div>
                <strong>{{ item.title }}</strong>
                <p>{{ item.desc }}</p>
              </div>
              <em :class="{ pending: item.state !== '完成' }">{{ item.state }}</em>
            </article>
          </div>
        </div>

        <aside class="continuity-panel">
          <div class="section-title">
            <div>
              <span>连续性校验</span>
              <h2>剧情结构风险</h2>
            </div>
          </div>

          <div class="continuity-list">
            <article v-for="check in checks" :key="check.title">
              <CheckCircle2 :size="18" />
              <div>
                <strong>{{ check.title }}</strong>
                <p>{{ check.desc }}</p>
              </div>
              <span>{{ check.level }}</span>
            </article>
          </div>
        </aside>
      </section>
    </main>
  </div>
</template>
