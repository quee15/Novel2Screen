# Novel2Screen Vue3 App

这是面向 `Vue3 + FastAPI` 正式架构的前端工程骨架，和 `frontend/` 根目录下的静态原型并存。

## 目的

1. 保留原型页面用于快速演示
2. 提前建立 Vue3 工程化目录
3. 让后续对接 FastAPI 时可以直接落到真实代码结构

## 目录说明

| 路径 | 说明 |
| --- | --- |
| `src/views/` | 对应各业务页面 |
| `src/components/` | 可复用布局和信息卡片 |
| `src/router/` | 页面路由 |
| `src/stores/` | Pinia 状态管理 |
| `src/services/` | Axios 和后端 API 模块 |
| `src/utils/` | YAML 预览和前端工具函数 |
| `src/config/` | 导航、功能清单等静态配置 |

## 计划对接的后端架构

- Vue3
- FastAPI
- Novel Parser
- LLM Service
- Character Extractor
- Screenplay Generator
- YAML Export
- Storyboard

## 本地启动

安装依赖后运行：

```bash
npm install
npm run dev
```

如果本机还没安装 Node.js，可以先继续使用 `frontend/index.html` 的静态原型进行演示。
