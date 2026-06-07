<template>
  <section class="view-grid">
    <article class="section-card">
      <p class="section-card-eyebrow">LLM Review</p>
      <h3>AI剧本审校</h3>
      <p class="section-card-description">
        对应角色一致性、时间线、场景完整性和对白分布检查。
      </p>
    </article>

    <article class="section-card">
      <p class="section-card-eyebrow">Quality Score</p>
      <h3>剧本质量评估</h3>
      <p class="section-card-description">
        对应总分与维度评分，后续接 `POST /api/scripts/{script_id}/quality`。
      </p>
    </article>
  </section>
</template>
