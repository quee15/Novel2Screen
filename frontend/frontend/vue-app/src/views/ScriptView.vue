<template>
  <section class="view-grid">
    <article class="section-card">
      <p class="section-card-eyebrow">Screenplay Generator</p>
      <h3>多风格剧本改编</h3>
      <p class="section-card-description">
        对应 LLM Service 的剧本生成能力，后续可接 `POST /api/projects/{project_id}/scripts`。
      </p>

      <ul class="plain-list">
        <li>电影</li>
        <li>电视剧</li>
        <li>短剧</li>
        <li>动漫</li>
      </ul>
    </article>

    <article class="section-card">
      <p class="section-card-eyebrow">Human-in-the-loop</p>
      <h3>人机协同创作</h3>
      <p class="section-card-description">
        这里对应在线编辑场次、动作、对白和顺序调整，后续接场次编辑接口。
      </p>
    </article>
  </section>
</template>
