# Vue3 Frontend Structure

## 顶层目录

```text
public/              静态资源和本地 mock 文件
src/                 前端源码目录
docs/                产品、技术和结构文档
```

## src 目录

```text
src/app/             应用入口级配置
src/assets/          图片、图标、全局样式等资源
src/components/      跨页面通用组件
src/modules/         按业务能力拆分的功能模块
src/views/           Vue Router 页面视图
src/services/        接口请求、AI任务轮询、文件导出等服务
src/stores/          Pinia 状态
src/types/           全局 TypeScript 类型
src/utils/           工具函数
src/composables/     通用组合式函数
src/config/          环境配置、菜单配置、常量配置
src/mocks/           前端 mock 数据
src/tests/           测试相关文件
```

## app

```text
src/app/layouts/     工作台布局、登录布局、项目详情布局
src/app/router/      Vue Router 路由表和权限路由
src/app/plugins/     UI库、图表、编辑器等插件注册
src/app/providers/   Query、主题、权限、全局上下文 Provider
```

## components

```text
src/components/base/           通用按钮、空状态、加载态、确认弹窗等
src/components/upload/         小说上传、文件进度、上传状态
src/components/script-editor/  剧本编辑器、格式工具栏、版本对比
src/components/graph/          人物图谱、故事图谱、节点详情面板
src/components/timeline/       故事时间线、事件列表
src/components/quality/        评分卡片、问题列表、修改建议
src/components/export/         YAML预览、导出配置、Schema校验
```

## modules

```text
src/modules/auth/           登录、用户信息、权限
src/modules/projects/       项目列表、新建项目、项目状态
src/modules/novel-import/   小说上传、解析任务、章节拆分
src/modules/chapters/       章节列表、章节详情、解析结果
src/modules/script-editor/  剧本编辑、剧本格式切换、版本记录
src/modules/people-graph/   人物抽取、人物关系、图谱数据处理
src/modules/story-map/      事件、地点、时间线、故事知识图谱
src/modules/ai-review/      一致性审核、质量评分、修改建议
src/modules/shotlist/       分镜脚本、镜头表格、镜头建议
src/modules/yaml-export/    YAML生成、预览、下载、Schema校验
```

## views

```text
src/views/login/             登录页
src/views/projects/          项目列表和创建项目页
src/views/project-overview/  项目总览页
src/views/chapters/          章节解析页
src/views/editor/            剧本编辑页
src/views/people-graph/      人物关系图谱页
src/views/story-map/         故事知识图谱页
src/views/review/            AI审核页
src/views/shotlist/          分镜脚本页
src/views/export/            YAML导出页
```

## services

```text
src/services/api/       HTTP请求封装、接口模块
src/services/ai-tasks/  AI解析、审核、导出等长任务状态管理
```

## 第一阶段 MVP

建议第一阶段先实现：

1. 小说上传与解析
2. 章节拆分结果展示
3. 剧本编辑器
4. AI审核结果展示
5. YAML导出

人物关系图谱、故事知识图谱、分镜脚本可以放到第二阶段。
