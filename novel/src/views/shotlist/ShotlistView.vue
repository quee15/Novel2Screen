<script setup lang="ts">
import {
  Aperture,
  Bell,
  BookOpenText,
  Camera,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clapperboard,
  Clock3,
  Download,
  FileCode2,
  Film,
  GitBranch,
  LayoutDashboard,
  Lightbulb,
  Maximize2,
  Move,
  Network,
  PanelRightOpen,
  Play,
  Rows3,
  Search,
  Settings,
  SlidersHorizontal,
  Sparkles,
  Sun,
  UploadCloud,
  Video,
  WandSparkles,
} from 'lucide-vue-next';

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: true, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const shotStats = [
  { label: '镜头总数', value: '186', desc: '当前场 12 个镜头', tone: 'pink' },
  { label: '预计时长', value: '18:42', desc: '较目标超出 01:20', tone: 'gold' },
  { label: '对白镜头', value: '64', desc: '占比 34%' },
  { label: '动作镜头', value: '38', desc: '需要调度设计' },
];

const shotRows = [
  { no: 'S42-01', scene: '档案室入口', shot: '远景', move: '缓慢推进', light: '冷色顶光', duration: '06s', state: '已生成' },
  { no: 'S42-02', scene: '文件柜前', shot: '中景', move: '手持跟拍', light: '手电侧光', duration: '09s', state: '待确认' },
  { no: 'S42-03', scene: '沈澜特写', shot: '特写', move: '静止', light: '低照度面光', duration: '05s', state: '推荐' },
  { no: 'S42-04', scene: '走廊火光', shot: '大全景', move: '快速横移', light: '火光反打', duration: '07s', state: '风险' },
  { no: 'S42-05', scene: '秦砚转身', shot: '近景', move: '轻微推近', light: '背光剪影', duration: '08s', state: '已生成' },
];

const shotCards = [
  { no: '01', title: '建立空间', desc: '远景交代档案室深度和出口方向' },
  { no: '02', title: '线索发现', desc: '跟拍文件柜，突出档案被转移' },
  { no: '03', title: '主角判断', desc: '特写沈澜，承接角色动机' },
  { no: '04', title: '危险进入', desc: '火光横移，制造节奏突变' },
  { no: '05', title: '反转伏笔', desc: '秦砚背光，暗示立场不稳' },
];

const cameraSettings = [
  { icon: Camera, label: '景别', value: '特写' },
  { icon: Move, label: '运镜', value: '静止转轻推' },
  { icon: Sun, label: '光线', value: '低照度面光' },
  { icon: Clock3, label: '时长', value: '05 秒' },
];

const suggestions = [
  { title: '加强出口方向', desc: '在 S42-01 增加左侧出口标识，避免后续逃跑方向突兀。' },
  { title: '保留反转信息', desc: 'S42-05 的背光剪影可以作为秦砚背叛的视觉伏笔。' },
  { title: '压缩动作镜头', desc: 'S42-04 可从 7 秒压到 5 秒，让火势突入更干脆。' },
];
</script>

<template>
  <div class="workspace-shell shotlist-page">
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
        <span>镜头生成</span>
        <strong>42 / 58 场</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索镜头、场景或对白" placeholder="搜索镜头、场景或对白" />
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
            生成分镜
          </button>
        </div>
      </header>

      <section class="page-heading shot-heading">
        <div>
          <p class="eyebrow">分镜脚本</p>
          <h1>把剧本场次转成可拍摄的镜头计划</h1>
          <p>根据剧本文本自动生成镜头编号、景别、运镜、光线、时长和画面描述，供导演和制片继续调整。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <SlidersHorizontal :size="18" />
            镜头规则
          </button>
          <button class="ghost-button">
            <Download :size="18" />
            导出表格
          </button>
        </div>
      </section>

      <section class="shot-stats" aria-label="分镜统计">
        <article v-for="stat in shotStats" :key="stat.label" class="shot-stat-card" :class="stat.tone">
          <span>{{ stat.label }}</span>
          <strong>{{ stat.value }}</strong>
          <p>{{ stat.desc }}</p>
        </article>
      </section>

      <section class="shot-workbench">
        <div class="shot-table-panel">
          <div class="section-title">
            <div>
              <span>镜头表</span>
              <h2>第 42 场 · 档案室失火</h2>
            </div>
            <button class="ghost-button compact-button">
              <Rows3 :size="16" />
              表格视图
            </button>
          </div>

          <div class="shot-table">
            <div class="shot-row shot-head">
              <span>编号</span>
              <span>场景</span>
              <span>景别</span>
              <span>运镜</span>
              <span>光线</span>
              <span>时长</span>
              <span>状态</span>
            </div>
            <button v-for="shot in shotRows" :key="shot.no" class="shot-row" :class="{ selected: shot.no === 'S42-03' }">
              <strong>{{ shot.no }}</strong>
              <span>{{ shot.scene }}</span>
              <span>{{ shot.shot }}</span>
              <span>{{ shot.move }}</span>
              <span>{{ shot.light }}</span>
              <span>{{ shot.duration }}</span>
              <em>{{ shot.state }}</em>
            </button>
          </div>
        </div>

        <aside class="shot-detail-panel">
          <div class="section-title">
            <div>
              <span>当前镜头</span>
              <h2>S42-03 沈澜特写</h2>
            </div>
            <PanelRightOpen :size="20" />
          </div>

          <div class="shot-preview">
            <div class="preview-frame">
              <Film :size="30" />
              <span>16:9</span>
            </div>
            <div>
              <strong>画面描述</strong>
              <p>沈澜抬眼看向被翻空的档案柜，火光尚未出现，画面保持安静压迫感。</p>
            </div>
          </div>

          <div class="camera-grid">
            <article v-for="setting in cameraSettings" :key="setting.label">
              <component :is="setting.icon" :size="18" />
              <span>{{ setting.label }}</span>
              <strong>{{ setting.value }}</strong>
            </article>
          </div>

          <button class="wide-button">
            <WandSparkles :size="18" />
            重新生成当前镜头
          </button>
        </aside>
      </section>

      <section class="shot-journey">
        <div class="section-title">
          <div>
            <span>镜头旅程</span>
            <h2>从建立空间到反转伏笔</h2>
          </div>
          <button class="ghost-button compact-button">
            <Play :size="16" />
            播放预览
          </button>
        </div>

        <div class="shot-card-track">
          <article v-for="card in shotCards" :key="card.no" class="shot-card">
            <span>{{ card.no }}</span>
            <div class="shot-card-frame">
              <Aperture :size="24" />
            </div>
            <strong>{{ card.title }}</strong>
            <p>{{ card.desc }}</p>
          </article>
        </div>
      </section>

      <section class="shot-suggestion-section">
        <div class="section-title">
          <div>
            <span>AI镜头建议</span>
            <h2>提升可拍摄性和视觉连续性</h2>
          </div>
          <Lightbulb :size="20" />
        </div>

        <div class="shot-suggestion-grid">
          <article v-for="suggestion in suggestions" :key="suggestion.title">
            <CheckCircle2 :size="18" />
            <div>
              <strong>{{ suggestion.title }}</strong>
              <p>{{ suggestion.desc }}</p>
            </div>
            <ChevronRight :size="16" />
          </article>
        </div>
      </section>
    </main>
  </div>
</template>
