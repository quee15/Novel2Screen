# Novel2Screen Frontend

当前前端目录现在包含两套内容：一套是可直接运行的零依赖静态原型，另一套是面向 `Vue3 + FastAPI` 的正式工程骨架；两者都以根目录 `README.md` 中定义的核心功能为基准。

## 目录结构

| 文件 | 说明 |
| --- | --- |
| `index.html` | 页面骨架，挂载侧边栏、Hero 区和主内容区域 |
| `styles.css` | 整体视觉系统、响应式布局和各模块样式 |
| `data.js` | 演示数据、图谱/剧本/分镜/评分生成逻辑 |
| `yaml.js` | YAML 结构生成与 Schema 规则校验 |
| `app.js` | 页面渲染、状态管理、交互逻辑、文件上传与工作流联动 |
| `VUE3_MIGRATION.md` | 静态原型迁移到 Vue3 的映射说明 |
| `vue-app/` | 面向 `Vue3 + FastAPI` 的正式前端工程骨架 |

## 当前能力

1. 小说上传与解析：支持 TXT / DOCX 文件选择与拖拽，展示章节列表与解析状态。
2. 构建人物关系图谱：展示人物节点、关系边、角色详情和关系来源占位信息。
3. 生成故事图谱：展示故事事件、地点、时间线及其结构化映射。
4. 多风格剧本改编：支持电影、电视剧、短剧、动漫风格切换与剧本重生成。
5. AI 剧本审校：展示角色一致性、时间线、场景完整性与对白分布问题。
6. 人机协同创作：支持在线编辑场次、动作、对白，以及新增、删除、调整顺序。
7. 分镜脚本生成：根据当前剧本生成镜头设计、景别、运镜、光线和时长建议。
8. 剧本质量评估：输出总分与多维评分结果，并展示评分说明。
9. 导出 YAML 格式剧本：按 `schema_version: "1.0"` 生成预览，执行结构校验并下载导出文件。

## 与文档的对齐

1. `README.md`
   前端能力说明、页面功能分区和展示重点以根目录 9 项核心功能为唯一基准。
2. `docs/schema_design.md`
   YAML 预览和校验围绕 `project/source/characters/story_graph/script/storyboard/review/quality/export/extensions` 组织。
3. `docs/architecture.md`
   页面中的任务状态、服务命名和工作流顺序对齐了 Project / Parser / Extraction / Script / Review / Storyboard / Export 这些模块边界。

## 运行方式

1. 静态原型：直接在浏览器里打开 `frontend/index.html`
2. Vue3 工程：进入 `frontend/vue-app/` 后执行 `npm install`、`npm run dev`

## 后续建议

1. 接入真实后端时，优先把 `data.js` 中的模拟生成逻辑替换为 API 调用。
2. 如果后续正式按 `Vue3 + FastAPI` 开发，可直接在 `frontend/vue-app/` 基础上继续补视图、路由、状态和 API 模块。
