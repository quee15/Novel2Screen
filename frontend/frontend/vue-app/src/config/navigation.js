export const navigationItems = [
  {
    index: "01",
    name: "workspace",
    path: "/",
    label: "项目工作台",
    eyebrow: "Operating Deck",
    description: "对齐根目录 README 的 9 项核心能力，汇总任务状态、能力覆盖和开发方向。"
  },
  {
    index: "02",
    name: "upload",
    path: "/upload",
    label: "小说上传与解析",
    eyebrow: "Source Intake",
    description: "对应 FastAPI -> Novel Parser 的入口页面，负责文件上传、章节预览和解析状态。"
  },
  {
    index: "03",
    name: "graph",
    path: "/graph",
    label: "人物与故事图谱",
    eyebrow: "Knowledge Graph",
    description: "承接 Character Extractor 结果，展示人物关系图谱与故事图谱。"
  },
  {
    index: "04",
    name: "script",
    path: "/script",
    label: "剧本改编与协同创作",
    eyebrow: "Screenplay",
    description: "承接 LLM Service -> Screenplay Generator 的结果，并提供在线编辑入口。"
  },
  {
    index: "05",
    name: "review",
    path: "/review",
    label: "AI审校与质量评估",
    eyebrow: "Review & Score",
    description: "展示 AI 审校结果、质量维度评分和可解释的扣分依据。"
  },
  {
    index: "06",
    name: "storyboard",
    path: "/storyboard",
    label: "分镜脚本生成",
    eyebrow: "Storyboard",
    description: "承接 Storyboard 结果，展示镜头设计、景别、运镜和时长。"
  },
  {
    index: "07",
    name: "export",
    path: "/export",
    label: "YAML剧本导出",
    eyebrow: "Schema Export",
    description: "承接 YAML Export 能力，预览结构、执行校验并发起下载。"
  }
];
