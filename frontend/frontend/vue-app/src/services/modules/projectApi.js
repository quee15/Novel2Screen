import http from "../http";

export function fetchProjects() {
  return http.get("/projects");
}

export function fetchProjectDetail(projectId) {
  return http.get(`/projects/${projectId}`);
}

export function uploadSource(projectId, formData) {
  return http.post(`/projects/${projectId}/source`, formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
}

export function triggerExtraction(projectId) {
  return http.post(`/projects/${projectId}/extract`);
}

export function generateScript(projectId, payload) {
  return http.post(`/projects/${projectId}/scripts`, payload);
}

export function requestReview(scriptId) {
  return http.post(`/scripts/${scriptId}/review`);
}

export function requestQuality(scriptId) {
  return http.post(`/scripts/${scriptId}/quality`);
}

export function requestStoryboard(scriptId) {
  return http.post(`/scripts/${scriptId}/storyboard`);
}

export function exportYaml(projectId) {
  return http.post(`/projects/${projectId}/exports/yaml`);
}
