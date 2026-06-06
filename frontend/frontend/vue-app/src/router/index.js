import { createRouter, createWebHistory } from "vue-router";

import WorkspaceView from "../views/WorkspaceView.vue";
import UploadParserView from "../views/UploadParserView.vue";
import GraphView from "../views/GraphView.vue";
import ScriptView from "../views/ScriptView.vue";
import ReviewView from "../views/ReviewView.vue";
import StoryboardView from "../views/StoryboardView.vue";
import ExportView from "../views/ExportView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "workspace", component: WorkspaceView },
    { path: "/upload", name: "upload", component: UploadParserView },
    { path: "/graph", name: "graph", component: GraphView },
    { path: "/script", name: "script", component: ScriptView },
    { path: "/review", name: "review", component: ReviewView },
    { path: "/storyboard", name: "storyboard", component: StoryboardView },
    { path: "/export", name: "export", component: ExportView }
  ]
});

export default router;
