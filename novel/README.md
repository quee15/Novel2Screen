# AI Novel Script Workspace

这是一个面向“小说解析、AI剧本改编、剧本审核、分镜生成、YAML导出”的 Vue3 前端项目骨架。

当前阶段只搭建目录结构，不包含业务代码。

## 推荐技术栈

- Vue 3 + Vite + TypeScript
- Vue Router：页面路由
- Pinia：状态管理
- Vue Query / TanStack Query：接口请求和异步任务状态
- Element Plus 或 Arco Design Vue：后台工作台 UI
- AntV G6 / ECharts Graph / Vue Flow：人物关系图谱、故事图谱
- Monaco Editor / TipTap Vue：剧本编辑器
- ECharts：评分、统计和可视化
- yaml：YAML预览与导出

## 核心页面

- `/login`：登录
- `/projects`：项目列表
- `/projects/create`：上传小说并创建项目
- `/projects/:id`：项目总览
- `/projects/:id/chapters`：章节解析
- `/projects/:id/editor`：剧本编辑器
- `/projects/:id/people`：人物关系图谱
- `/projects/:id/storymap`：故事知识图谱
- `/projects/:id/review`：AI剧本审核
- `/projects/:id/shotlist`：分镜脚本
- `/projects/:id/export`：YAML导出

## 目录说明

详细目录规划见 `docs/VUE3_FRONTEND_STRUCTURE.md`。
