import { createRouter, createWebHistory } from 'vue-router';
import LandingView from '../../views/landing/LandingView.vue';
import ProjectCreateView from '../../views/projects/ProjectCreateView.vue';
import NovelImportView from '../../views/novel-import/NovelImportView.vue';
import PeopleGraphView from '../../views/people-graph/PeopleGraphView.vue';
import StoryMapView from '../../views/story-map/StoryMapView.vue';
import ScriptReviewView from '../../views/review/ScriptReviewView.vue';
import ShotlistView from '../../views/shotlist/ShotlistView.vue';
import YamlExportView from '../../views/export/YamlExportView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: LandingView },
    { path: '/projects', name: 'projects', component: ProjectCreateView },
    { path: '/projects/create', redirect: '/projects' },
    { path: '/novel-import', name: 'novel-import', component: NovelImportView },
    { path: '/people-graph', name: 'people-graph', component: PeopleGraphView },
    { path: '/story-map', name: 'story-map', component: StoryMapView },
    { path: '/review', name: 'review', component: ScriptReviewView },
    { path: '/shotlist', name: 'shotlist', component: ShotlistView },
    { path: '/export', name: 'export', component: YamlExportView },
  ],
});

export default router;
