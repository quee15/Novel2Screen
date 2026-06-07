<script setup lang="ts">
import {
  Bell,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clapperboard,
  Clock3,
  FileCode2,
  FileWarning,
  GitBranch,
  Highlighter,
  LayoutDashboard,
  ListFilter,
  MessageSquareText,
  Network,
  PanelRightOpen,
  RefreshCw,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  UploadCloud,
  WandSparkles,
} from 'lucide-vue-next';

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: false, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: true, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const scoreCards = [
  { label: '综合评分', value: '82', desc: '可进入人工精修', tone: 'indigo' },
  { label: '角色一致性', value: '76', desc: '发现 5 处称谓/动机问题', tone: 'amber' },
  { label: '时间线合理性', value: '88', desc: '1 处跳转需补充', tone: 'green' },
  { label: '场景完整性', value: '71', desc: '3 个场景缺少动作信息', tone: 'rose' },
];

const issueFilters = ['全部', '高风险', '角色', '时间线', '场景', '对白'];

const issues = [
  { title: '秦砚动机转折缺少铺垫', type: '角色一致性', level: '高', chapter: '第 42 场', active: true },
  { title: '三日后时间跳转没有镜头交代', type: '时间线', level: '中', chapter: '第 37 场', active: false },
  { title: '档案室失火场景缺少出口方向', type: '场景完整性', level: '中', chapter: '第 43 场', active: false },
  { title: '沈澜对白语气与前文不一致', type: '对白', level: '低', chapter: '第 51 场', active: false },
];

const scriptLines = [
  { role: '场景 42', text: '内景，旧城地下档案室，夜。雨声从通风井里灌进来，文件柜被翻得七零八落。', mark: 'scene' },
  { role: '沈澜', text: '这些档案不是被烧掉的，是有人提前拿走了。', mark: '' },
  { role: '顾闻舟', text: '你怀疑秦砚？他一直在帮我们。', mark: '' },
  { role: '沈澜', text: '正因为他太及时了。每一次线索断掉，他都刚好在场。', mark: 'character' },
  { role: '动作', text: '远处传来玻璃碎裂声，火光从走廊尽头猛地扑上来。', mark: 'scene' },
  { role: '秦砚', text: '别往回走。出口在左边。', mark: 'risk' },
];

const suggestions = [
  { title: '补充前置证据', desc: '在第 28 场加入秦砚短暂离席或隐藏通信的动作，降低背叛突兀感。' },
  { title: '增强镜头交代', desc: '在失火前增加走廊方向、出口位置和烟雾蔓延路径。' },
  { title: '统一称谓', desc: '将“记者”称谓统一改为“调查员”，除非剧情需要身份误导。' },
];

const dimensions = [
  { label: '人物动机', value: 76 },
  { label: '对白自然度', value: 84 },
  { label: '节奏密度', value: 79 },
  { label: '可拍摄性', value: 73 },
];
</script>

<template>
  <div class="workspace-shell script-review-page">
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
        <span>校审进度</span>
        <strong>18 / 24 场</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索问题、场次或对白" placeholder="搜索问题、场次或对白" />
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
            重新校审
          </button>
        </div>
      </header>

      <section class="page-heading review-heading">
        <div>
          <p class="eyebrow">AI剧本校审</p>
          <h1>定位剧本中的一致性、时间线和场景问题</h1>
          <p>系统会根据人物图谱和故事图谱，对剧本初稿进行评分、标注问题，并给出可直接应用的修改建议。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <ListFilter :size="18" />
            校审维度
          </button>
          <button class="ghost-button">
            <RefreshCw :size="18" />
            同步图谱
          </button>
        </div>
      </section>

      <section class="review-score-grid" aria-label="剧本校审评分">
        <article v-for="card in scoreCards" :key="card.label" class="review-score-card" :class="card.tone">
          <span>{{ card.label }}</span>
          <strong>{{ card.value }}</strong>
          <p>{{ card.desc }}</p>
        </article>
      </section>

      <section class="review-workbench">
        <aside class="issue-panel">
          <div class="section-title">
            <div>
              <span>问题队列</span>
              <h2>待处理问题 14 条</h2>
            </div>
            <FileWarning :size="20" />
          </div>

          <div class="issue-filter" aria-label="问题筛选">
            <button v-for="filter in issueFilters" :key="filter" :class="{ selected: filter === '全部' }">
              {{ filter }}
            </button>
          </div>

          <div class="issue-list">
            <article v-for="issue in issues" :key="issue.title" class="issue-item" :class="{ active: issue.active }">
              <div>
                <strong>{{ issue.title }}</strong>
                <span>{{ issue.chapter }}</span>
              </div>
              <p>{{ issue.type }}</p>
              <em :class="{ high: issue.level === '高' }">{{ issue.level }}风险</em>
            </article>
          </div>
        </aside>

        <div class="script-panel">
          <div class="script-toolbar">
            <div>
              <span>剧本文本</span>
              <strong>第 42 场 · 档案室失火</strong>
            </div>
            <div class="script-tools">
              <button class="ghost-button compact-button">
                <Highlighter :size="16" />
                显示标注
              </button>
              <button class="ghost-button compact-button">
                <MessageSquareText :size="16" />
                评论
              </button>
            </div>
          </div>

          <div class="script-paper">
            <article v-for="line in scriptLines" :key="`${line.role}-${line.text}`" class="script-line" :class="line.mark">
              <span>{{ line.role }}</span>
              <p>{{ line.text }}</p>
            </article>
          </div>
        </div>

        <aside class="suggestion-panel">
          <div class="section-title">
            <div>
              <span>AI建议</span>
              <h2>当前问题修订方案</h2>
            </div>
            <PanelRightOpen :size="20" />
          </div>

          <div class="selected-issue-card">
            <div>
              <ShieldCheck :size="22" />
              <strong>秦砚动机转折缺少铺垫</strong>
            </div>
            <p>该问题影响角色一致性。建议在前文增加细节证据，让观众能回看时理解反转逻辑。</p>
          </div>

          <div class="suggestion-list">
            <article v-for="suggestion in suggestions" :key="suggestion.title">
              <CheckCircle2 :size="18" />
              <div>
                <strong>{{ suggestion.title }}</strong>
                <p>{{ suggestion.desc }}</p>
              </div>
            </article>
          </div>

          <button class="wide-button">
            <WandSparkles :size="18" />
            应用建议到草稿
          </button>
        </aside>
      </section>

      <section class="dimension-section">
        <div class="section-title">
          <div>
            <span>质量维度</span>
            <h2>剧本质量雷达</h2>
          </div>
          <Clock3 :size="20" />
        </div>

        <div class="dimension-grid">
          <article v-for="dimension in dimensions" :key="dimension.label">
            <div>
              <strong>{{ dimension.label }}</strong>
              <span>{{ dimension.value }}</span>
            </div>
            <div class="dimension-bar" aria-hidden="true">
              <i :style="{ width: `${dimension.value}%` }" />
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>
