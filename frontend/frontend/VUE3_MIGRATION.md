# Frontend Vue3 Migration

本文档用于说明 `frontend/` 目录如何从当前零依赖静态原型迁移到 `Vue3 + FastAPI` 正式架构。

## 当前状态

当前 `frontend/` 根目录下的文件：

- `index.html`
- `styles.css`
- `app.js`
- `data.js`
- `yaml.js`

它们构成一个可直接双击打开的静态原型，适合：

1. 演示产品流程
2. 校对页面结构
3. 提前确认前后端字段

## 新增的 Vue3 工程骨架

新增目录：

- `frontend/vue-app/`

对应后续要落地的正式架构：

- Vue3
- Vue Router
- Pinia
- Axios
- FastAPI API 对接

## 页面映射关系

当前原型页面与 Vue3 视图的映射如下：

| 原型能力 | Vue3 视图 |
| --- | --- |
| 项目工作台 | `src/views/WorkspaceView.vue` |
| 小说上传与解析 | `src/views/UploadParserView.vue` |
| 人物关系图谱 / 故事图谱 | `src/views/GraphView.vue` |
| 多风格剧本改编 / 人机协同创作 | `src/views/ScriptView.vue` |
| AI 剧本审校 / 剧本质量评估 | `src/views/ReviewView.vue` |
| 分镜脚本生成 | `src/views/StoryboardView.vue` |
| YAML 剧本导出 | `src/views/ExportView.vue` |

## 数据迁移关系

当前静态原型中的逻辑建议这样迁移：

| 当前文件 | 后续迁移方向 |
| --- | --- |
| `data.js` | `src/stores/` + `src/services/modules/` |
| `yaml.js` | `src/utils/yamlPreview.js` |
| `app.js` | `src/views/` + `src/components/` |
| `styles.css` | `src/styles/app.css` |

## 推荐协作方式

负责前端时，可以优先做：

1. 按 `vue-app/src/views/` 继续补页面
2. 按 `src/services/modules/` 和队友约定 FastAPI 接口
3. 把静态原型里的 mock 数据逐步替换成接口请求
4. 保留根目录静态原型用于演示，保留 `vue-app` 用于正式开发
