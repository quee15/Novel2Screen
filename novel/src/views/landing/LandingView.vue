<script setup lang="ts">
import {
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  Clapperboard,
  ClipboardCheck,
  FileCode2,
  GitBranch,
  Network,
  Play,
  Sparkles,
  UploadCloud,
  WandSparkles,
} from 'lucide-vue-next';

const workflow = [
  { title: '导入小说', desc: '上传 TXT / DOCX，自动拆章、清洗文本并保留原文索引。', icon: UploadCloud },
  { title: '构建图谱', desc: '抽取人物、事件、地点和时间线，形成可追溯的故事结构。', icon: GitBranch },
  { title: '生成剧本', desc: '面向电影、电视剧、短剧、动漫生成可编辑剧本初稿。', icon: Clapperboard },
  { title: '校审导出', desc: '检查一致性和可拍摄性，并导出标准 YAML 文件。', icon: FileCode2 },
];

const capabilities = [
  { title: '人物关系图谱', desc: '识别角色身份、关系强度、冲突变化和章节证据。', icon: Network },
  { title: '故事知识图谱', desc: '串联事件、地点、时间和因果链路，辅助改编结构判断。', icon: GitBranch },
  { title: 'AI剧本校审', desc: '定位角色一致性、时间线、场景完整性和对白问题。', icon: ClipboardCheck },
  { title: '分镜脚本生成', desc: '生成镜头编号、景别、运镜、光线和镜头时长建议。', icon: Clapperboard },
];

const metrics = [
  { value: '9', label: '核心工作流' },
  { value: '4', label: '剧本体裁' },
  { value: 'YAML', label: '结构化交付' },
];
</script>

<template>
  <div class="landing-page">
    <header class="landing-nav">
      <RouterLink to="/" class="landing-brand">
        <span><BookOpenText :size="22" /></span>
        <strong>ScriptAI</strong>
      </RouterLink>

      <nav aria-label="首页导航">
        <a href="#workflow">工作流</a>
        <a href="#capabilities">核心能力</a>
        <a href="#export">交付格式</a>
      </nav>

      <RouterLink to="/projects" class="landing-nav-cta">
        进入工作台
        <ArrowRight :size="17" />
      </RouterLink>
    </header>

    <main>
      <section class="landing-hero">
        <div class="hero-scene" aria-hidden="true">
          <div class="scene-board board-left">
            <span>Novel.txt</span>
            <i />
            <i />
            <i />
          </div>
          <div class="scene-board board-center">
            <span>Script Scene 42</span>
            <strong>档案室失火</strong>
            <i />
            <i />
            <i />
          </div>
          <div class="scene-board board-right">
            <span>YAML</span>
            <i />
            <i />
            <i />
          </div>
          <div class="scene-node node-a">人物</div>
          <div class="scene-node node-b">事件</div>
          <div class="scene-node node-c">分镜</div>
          <div class="scene-line line-a" />
          <div class="scene-line line-b" />
          <div class="scene-line line-c" />
          <div class="film-strip">
            <span />
            <span />
            <span />
            <span />
          </div>
        </div>

        <div class="hero-content">
          <p class="landing-eyebrow">AI Novel to Script Workspace</p>
          <h1>ScriptAI</h1>
          <p class="hero-lead">把长篇小说解析成可编辑剧本、人物图谱、故事图谱、分镜脚本和标准 YAML 交付文件。</p>
          <div class="hero-actions">
            <RouterLink to="/projects" class="hero-primary">
              开始创建项目
              <Sparkles :size="18" />
            </RouterLink>
            <RouterLink to="/novel-import" class="hero-secondary">
              查看导入流程
              <Play :size="18" />
            </RouterLink>
          </div>
        </div>

        <div class="hero-metrics">
          <article v-for="metric in metrics" :key="metric.label">
            <strong>{{ metric.value }}</strong>
            <span>{{ metric.label }}</span>
          </article>
        </div>
      </section>

      <section id="workflow" class="landing-section workflow-section">
        <div class="landing-section-heading">
          <span>Workflow</span>
          <h2>从小说原文到可交付剧本，一条线完成</h2>
        </div>
        <div class="workflow-grid">
          <article v-for="(item, index) in workflow" :key="item.title">
            <span class="step-index">0{{ index + 1 }}</span>
            <component :is="item.icon" :size="24" />
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </article>
        </div>
      </section>

      <section id="capabilities" class="landing-section capability-section">
        <div class="landing-section-heading">
          <span>Capabilities</span>
          <h2>围绕剧本生产的关键 AI 能力</h2>
        </div>
        <div class="capability-grid">
          <article v-for="item in capabilities" :key="item.title">
            <component :is="item.icon" :size="24" />
            <div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </div>
            <CheckCircle2 :size="18" />
          </article>
        </div>
      </section>

      <section id="export" class="landing-section export-story-section">
        <div>
          <span>Delivery</span>
          <h2>让创作结果可以被系统继续使用</h2>
          <p>ScriptAI 不只生成文本，还会把剧本、人物、故事结构、分镜和校审结果整理成统一 Schema，方便进入拍摄、制片或后续自动化流程。</p>
          <RouterLink to="/export" class="landing-inline-cta">
            查看 YAML 导出
            <FileCode2 :size="18" />
          </RouterLink>
        </div>
        <pre><code>project:
  title: 天幕回声
  target_format: short_drama
scenes:
  - id: S42
    location: 旧城地下档案室
    shots:
      - size: 特写
        movement: 静止转轻推</code></pre>
      </section>

      <section class="landing-final-cta">
        <WandSparkles :size="28" />
        <h2>开始搭建你的 AI 剧本生产线</h2>
        <p>先从上传一部小说开始，逐步生成剧本、图谱、校审结果和分镜脚本。</p>
        <RouterLink to="/projects">
          进入工作台
          <ArrowRight :size="18" />
        </RouterLink>
      </section>
    </main>
  </div>
</template>
