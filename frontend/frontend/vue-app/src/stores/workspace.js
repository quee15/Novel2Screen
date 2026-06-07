import { defineStore } from "pinia";

export const useWorkspaceStore = defineStore("workspace", {
  state: () => ({
    project: {
      id: "project_001",
      title: "旧城雨夜",
      description: "Vue3 工程骨架中的默认项目占位。"
    },
    capabilities: [
      "小说上传与解析",
      "人物关系图谱",
      "故事图谱",
      "多风格剧本改编",
      "AI剧本审校",
      "人机协同创作",
      "分镜脚本生成",
      "剧本质量评估",
      "YAML剧本导出"
    ],
    backendChain: [
      "Vue3",
      "FastAPI",
      "Novel Parser",
      "LLM Service",
      "Character Extractor",
      "Screenplay Generator",
      "Storyboard",
      "YAML Export"
    ]
  })
});
