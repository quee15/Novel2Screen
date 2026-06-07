<script setup lang="ts">
import { computed, ref } from 'vue';
import {
  Bell,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  ClipboardCheck,
  Clapperboard,
  Clock,
  Eye,
  FileCode2,
  FileText,
  GitBranch,
  LayoutDashboard,
  Layers,
  ListChecks,
  Network,
  RotateCcw,
  ScanText,
  Search,
  Settings,
  SlidersHorizontal,
  Sparkles,
  UploadCloud,
} from 'lucide-vue-next';

const selectedFileName = ref('天幕回声_正文.docx');
const selectedMode = ref('智能识别');
const selectedLanguage = ref('简体中文');

const navItems = [
  { label: '项目工作台', icon: LayoutDashboard, active: false, path: '/projects' },
  { label: '小说导入', icon: UploadCloud, active: true, path: '/novel-import' },
  { label: '人物图谱', icon: Network, active: false, path: '/people-graph' },
  { label: '故事图谱', icon: GitBranch, active: false, path: '/story-map' },
  { label: '剧本校审', icon: ClipboardCheck, active: false, path: '/review' },
  { label: '分镜脚本', icon: Clapperboard, active: false, path: '/shotlist' },
  { label: 'YAML导出', icon: FileCode2, active: false, path: '/export' },
];

const importModes = ['智能识别', '按章节标题', '按空行段落', '手动标记'];

const fileQueue = [
  { name: '天幕回声_正文.docx', size: '4.8 MB', status: '已选择', progress: 100 },
  { name: '人物设定补充.txt', size: '420 KB', status: '可合并', progress: 64 },
  { name: '世界观资料.txt', size: '318 KB', status: '待确认', progress: 28 },
];

const parserCards = [
  { label: '章节标题', value: '126', sub: '识别到 8 种标题格式', tone: 'indigo' },
  { label: '正文段落', value: '8,642', sub: '已过滤重复空行', tone: 'green' },
  { label: '疑似对白', value: '2,318', sub: '可进入剧本对白候选', tone: 'amber' },
  { label: '异常片段', value: '14', sub: '需要人工复核', tone: 'rose' },
];

const chapterPreview = [
  { chapter: '第001章 雨夜来客', words: '3,842', confidence: '98%', warning: '正常' },
  { chapter: '第002章 铁轨尽头', words: '4,106', confidence: '96%', warning: '正常' },
  { chapter: '番外 旧城档案', words: '1,208', confidence: '78%', warning: '标题疑似番外' },
  { chapter: '第003章 不存在的钟声', words: '3,664', confidence: '94%', warning: '正常' },
];

const checks = [
  { label: '文件格式', desc: 'DOCX结构可读取，未发现损坏段落', state: '通过', icon: CheckCircle2 },
  { label: '章节连续性', desc: '发现 1 个番外章节，建议确认是否进入主线', state: '待确认', icon: CircleAlert },
  { label: '敏感空段', desc: '正文空段已自动归并，不影响拆章', state: '已处理', icon: ListChecks },
];

const nextTasks = [
  { title: '人物抽取', desc: '从章节正文中抽取角色、身份和首次出现位置' },
  { title: '事件归纳', desc: '整理关键事件、地点、时间点和因果关系' },
  { title: '剧本改编', desc: '按目标体裁生成可编辑剧本初稿' },
];

const uploadCopy = computed(() => selectedFileName.value || '拖拽 TXT / DOCX 文件到这里');

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    selectedFileName.value = file.name;
  }
}
</script>

<template>
  <div class="workspace-shell import-page">
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
        <span>导入额度</span>
        <strong>12.4M / 30M</strong>
        <div class="quota-bar" aria-hidden="true">
          <i />
        </div>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div class="search-box">
          <Search :size="18" />
          <input aria-label="搜索文件、章节或导入任务" placeholder="搜索文件、章节或导入任务" />
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
            开始解析
          </button>
        </div>
      </header>

      <section class="page-heading import-heading">
        <div>
          <p class="eyebrow">小说导入</p>
          <h1>把原始小说整理成可改编素材</h1>
          <p>先完成文件上传、章节识别、文本清洗和质量检查，再进入人物图谱、故事图谱与剧本改编流程。</p>
        </div>
        <div class="heading-actions">
          <button class="ghost-button">
            <RotateCcw :size="18" />
            重置配置
          </button>
          <button class="ghost-button">
            <Eye :size="18" />
            预览原文
          </button>
        </div>
      </section>

      <section class="import-hero">
        <div class="import-upload-card">
          <div class="section-title">
            <div>
              <span>文件上传</span>
              <h2>选择小说正文与补充资料</h2>
            </div>
            <span class="status-pill">无后端Mock</span>
          </div>

          <label class="import-dropzone">
            <input type="file" accept=".txt,.doc,.docx" @change="onFileChange" />
            <span class="dropzone-icon"><UploadCloud :size="34" /></span>
            <strong>{{ uploadCopy }}</strong>
            <span>支持 TXT、DOC、DOCX，可追加人物设定、世界观资料作为辅助文本</span>
          </label>

          <div class="file-queue">
            <article v-for="file in fileQueue" :key="file.name" class="file-row">
              <div class="file-icon">
                <FileText :size="20" />
              </div>
              <div>
                <strong>{{ file.name }}</strong>
                <span>{{ file.size }} · {{ file.status }}</span>
              </div>
              <div class="file-progress" aria-hidden="true">
                <i :style="{ width: `${file.progress}%` }" />
              </div>
            </article>
          </div>
        </div>

        <aside class="import-config-card">
          <div class="section-title">
            <div>
              <span>解析配置</span>
              <h2>控制拆章和清洗方式</h2>
            </div>
            <SlidersHorizontal :size="20" />
          </div>

          <div class="config-stack">
            <label>
              章节识别模式
              <select v-model="selectedMode" aria-label="章节识别模式">
                <option v-for="mode in importModes" :key="mode">{{ mode }}</option>
              </select>
            </label>
            <label>
              文本语言
              <select v-model="selectedLanguage" aria-label="文本语言">
                <option>简体中文</option>
                <option>繁体中文</option>
                <option>英文</option>
              </select>
            </label>
            <label>
              目标体裁
              <select aria-label="目标体裁">
                <option>短剧</option>
                <option>电影</option>
                <option>电视剧</option>
                <option>动漫</option>
              </select>
            </label>
          </div>

          <div class="switch-list">
            <label><input type="checkbox" checked /> 自动合并过短章节</label>
            <label><input type="checkbox" checked /> 保留原文段落索引</label>
            <label><input type="checkbox" /> 跳过番外章节</label>
          </div>
        </aside>
      </section>

      <section class="parser-summary" aria-label="解析统计">
        <article v-for="card in parserCards" :key="card.label" class="parser-card" :class="card.tone">
          <span>{{ card.label }}</span>
          <strong>{{ card.value }}</strong>
          <p>{{ card.sub }}</p>
        </article>
      </section>

      <section class="import-workbench">
        <div class="chapter-panel">
          <div class="section-title">
            <div>
              <span>章节识别预览</span>
              <h2>导入前确认拆章结果</h2>
            </div>
            <button class="ghost-button compact-button">
              <ScanText :size="16" />
              重新扫描
            </button>
          </div>

          <div class="chapter-table">
            <div class="chapter-row chapter-head">
              <span>章节</span>
              <span>字数</span>
              <span>置信度</span>
              <span>状态</span>
            </div>
            <div v-for="chapter in chapterPreview" :key="chapter.chapter" class="chapter-row">
              <strong>{{ chapter.chapter }}</strong>
              <span>{{ chapter.words }}</span>
              <span>{{ chapter.confidence }}</span>
              <span :class="{ warning: chapter.warning !== '正常' }">{{ chapter.warning }}</span>
            </div>
          </div>
        </div>

        <aside class="review-panel">
          <div class="section-title">
            <div>
              <span>导入质检</span>
              <h2>进入AI解析前的检查</h2>
            </div>
          </div>

          <div class="check-list">
            <article v-for="check in checks" :key="check.label" class="check-item">
              <component :is="check.icon" :size="18" />
              <div>
                <strong>{{ check.label }}</strong>
                <p>{{ check.desc }}</p>
              </div>
              <span>{{ check.state }}</span>
            </article>
          </div>

          <div class="next-flow">
            <div class="flow-title">
              <Clock :size="18" />
              <strong>后续生成任务</strong>
            </div>
            <article v-for="task in nextTasks" :key="task.title">
              <Layers :size="16" />
              <div>
                <strong>{{ task.title }}</strong>
                <p>{{ task.desc }}</p>
              </div>
              <ChevronRight :size="16" />
            </article>
          </div>
        </aside>
      </section>
    </main>
  </div>
</template>
