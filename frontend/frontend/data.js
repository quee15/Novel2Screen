(function () {
  const locationSeeds = [
    { id: "loc_001", name: "旧城旅馆", description: "靠近码头的老式旅馆，灯光常年发黄。" },
    { id: "loc_002", name: "旧城码头档案室", description: "堆满航运账本与旧箱子的狭窄仓室。" },
    { id: "loc_003", name: "暗房", description: "报社地下暗房，墙上挂着未显影的照片。" },
    { id: "loc_004", name: "排水隧道", description: "潮湿阴冷的地下通道，回声很重。" },
  ];

  const timeSeeds = ["雨夜", "深夜", "凌晨前", "拂晓"];

  const styleLibrary = {
    film: {
      label: "电影",
      description: "压缩事件数量，强化氛围和镜头感。",
      actionTone: "镜头缓慢推进，环境先于人物进入叙事。",
      dialogueTone: "对白克制，强调潜台词。",
      emotion: "低声",
      pacing: "集中",
      shotSizes: ["wide", "medium", "close_up"],
      cameraMoves: ["slow_push_in", "tracking", "static"],
      lighting: "冷色雨夜光与局部暖光形成对照。",
      audio: "雨声、脚步声、低频环境音",
    },
    tv_series: {
      label: "电视剧",
      description: "保留更多铺垫与人物互动，适合分集推进。",
      actionTone: "镜头服务对白与角色关系，保留更多交互信息。",
      dialogueTone: "对白更完整，交代动机与关系。",
      emotion: "沉稳",
      pacing: "层层递进",
      shotSizes: ["medium", "close_up", "wide"],
      cameraMoves: ["pan", "static", "dolly"],
      lighting: "自然光与实景光源并重。",
      audio: "对白主导，环境音作为铺底",
    },
    short_drama: {
      label: "短剧",
      description: "强调冲突和反转，单场信息密度更高。",
      actionTone: "切入更直接，场次落点更明确。",
      dialogueTone: "对白短促有钩子，适合推进冲突。",
      emotion: "急促",
      pacing: "高压推进",
      shotSizes: ["close_up", "medium", "wide"],
      cameraMoves: ["handheld", "slow_push_in", "pan"],
      lighting: "对比更强，重点压住人物表情。",
      audio: "节奏性音乐与近距离收音",
    },
    animation: {
      label: "动漫",
      description: "强化视觉奇观和动作节奏，允许更夸张的表演。",
      actionTone: "动作描述更视觉化，强调构图和节奏。",
      dialogueTone: "对白更具角色感，可容纳夸张反应。",
      emotion: "锐利",
      pacing: "张弛分明",
      shotSizes: ["extreme_wide", "medium", "close_up"],
      cameraMoves: ["tracking", "tilt", "slow_push_in"],
      lighting: "允许更风格化的色彩分区和轮廓光。",
      audio: "环境音、拟音和节奏点配合动作",
    },
  };

  function deepClone(value) {
    // 优化：处理特殊情况和循环引用
    if (value === null || value === undefined) {
      return value;
    }

    if (typeof value !== 'object') {
      return value;
    }

    // 处理 Date 对象
    if (value instanceof Date) {
      return new Date(value.getTime());
    }

    // 处理数组
    if (Array.isArray(value)) {
      return value.map(item => deepClone(item));
    }

    // 处理普通对象
    const cloned = {};
    for (const key in value) {
      if (value.hasOwnProperty(key)) {
        cloned[key] = deepClone(value[key]);
      }
    }
    return cloned;
  }

  function nowIso() {
    return new Date().toISOString();
  }

  // 数据验证辅助函数
  function validateProjectStructure(project) {
    const errors = [];

    if (!project || typeof project !== 'object') {
      errors.push('项目数据结构无效');
      return errors;
    }

    if (!project.schema_version) {
      errors.push('缺少 schema_version');
    }

    if (!project.project || !project.project.id) {
      errors.push('缺少项目 ID');
    }

    if (!project.source || !Array.isArray(project.source.chapters)) {
      errors.push('缺少章节数据');
    }

    if (!project.characters || !Array.isArray(project.characters)) {
      errors.push('缺少人物数据');
    }

    return errors;
  }

  function createDemoProject() {
    const project = {
      schema_version: "1.0",
      project: {
        id: "project_001",
        title: "旧城雨夜",
        description: "一部围绕失踪案展开的旧城悬疑改编项目。",
        creator: "frontend_demo",
        created_at: "2026-06-05T13:00:00+08:00",
        updated_at: "2026-06-05T15:00:00+08:00",
        status: "reviewing",
      },
      source: {
        document: {
          id: "doc_001",
          filename: "old_city.docx",
          file_type: "docx",
          language: "zh-CN",
          checksum: "sha256:old-city-demo",
        },
        parse_result: {
          chapter_count: 4,
          total_characters: 28642,
          parser_version: "parser-1.0",
        },
        chapters: [
          {
            id: "chapter_001",
            index: 1,
            title: "第一章 雨夜抵达",
            summary: "青年侦探林澈抵达旧城旅馆，接到一份有关失踪案的旧档案。",
            word_count: 7820,
          },
          {
            id: "chapter_002",
            index: 2,
            title: "第二章 码头旧账",
            summary: "林澈与档案员沈砚在码头档案室核对航运记录，发现账本被人提前翻动。",
            word_count: 7160,
          },
          {
            id: "chapter_003",
            index: 3,
            title: "第三章 暗房里的照片",
            summary: "摄影记者许燃在暗房翻出一组旧照片，照片里出现了失踪者与旅馆老板。",
            word_count: 6840,
          },
          {
            id: "chapter_004",
            index: 4,
            title: "第四章 隧道追逐",
            summary: "众人沿着排水隧道追逐幕后联系人，真相开始浮出水面。",
            word_count: 6822,
          },
        ],
      },
      characters: [
        {
          id: "char_001",
          name: "林澈",
          aliases: ["阿澈"],
          identity: "青年侦探",
          description: "冷静、敏锐，擅长从碎片线索里还原事件结构。",
          first_appearance: {
            chapter_id: "chapter_001",
            excerpt: "林澈推开旅馆的木门，雨水顺着伞骨滴到石阶上。",
          },
        },
        {
          id: "char_002",
          name: "沈砚",
          aliases: [],
          identity: "码头档案员",
          description: "熟悉旧城航运记录，对失踪案涉及的时间线格外敏感。",
          first_appearance: {
            chapter_id: "chapter_002",
            excerpt: "沈砚把一摞旧账簿推到林澈面前，手指停在缺页的位置。",
          },
        },
        {
          id: "char_003",
          name: "许燃",
          aliases: ["阿燃"],
          identity: "摄影记者",
          description: "擅长从图像中发现细节，性格直接，行动力强。",
          first_appearance: {
            chapter_id: "chapter_003",
            excerpt: "许燃关掉红灯，把刚显影的照片夹到晾线上。",
          },
        },
        {
          id: "char_004",
          name: "贺叔",
          aliases: ["贺老板"],
          identity: "旧旅馆老板",
          description: "掌握旧城多年前的隐秘往事，说话总留三分余地。",
          first_appearance: {
            chapter_id: "chapter_001",
            excerpt: "柜台后的老人抬起头，像早已知道林澈会出现。",
          },
        },
      ],
      relationships: [
        {
          id: "rel_001",
          from_character_id: "char_001",
          to_character_id: "char_002",
          type: "ally",
          label: "合作",
          description: "两人围绕失踪案共享档案与推理线索。",
          evidence: {
            chapter_id: "chapter_002",
            excerpt: "如果你愿意继续查，我可以把封存账本打开给你看。",
          },
          confidence: 0.91,
        },
        {
          id: "rel_002",
          from_character_id: "char_001",
          to_character_id: "char_003",
          type: "colleague",
          label: "互补搭档",
          description: "林澈负责推理，许燃负责寻找可视证据。",
          evidence: {
            chapter_id: "chapter_003",
            excerpt: "你看照片，我看背面的日期，我们一人一半。",
          },
          confidence: 0.88,
        },
        {
          id: "rel_003",
          from_character_id: "char_001",
          to_character_id: "char_004",
          type: "unknown",
          label: "隐瞒",
          description: "贺叔与案件相关，但始终没有说出完整真相。",
          evidence: {
            chapter_id: "chapter_001",
            excerpt: "这地方记不得的人多，可记住的人更危险。",
          },
          confidence: 0.72,
        },
      ],
      story_graph: {
        events: [
          {
            id: "event_001",
            title: "抵达旧城",
            summary: "林澈在暴雨夜抵达旧城旅馆，收到一份匿名寄来的旧档案。",
            chapter_id: "chapter_001",
            participants: ["char_001", "char_004"],
            location_id: "loc_001",
            time_label: "雨夜",
            timeline_order: 1,
            evidence: {
              excerpt: "风把招牌吹得直晃，柜台上的档案袋却干得像刚放下。",
            },
          },
          {
            id: "event_002",
            title: "码头旧账缺页",
            summary: "沈砚带林澈进入档案室，发现关键航运账本被人抽走了一页。",
            chapter_id: "chapter_002",
            participants: ["char_001", "char_002"],
            location_id: "loc_002",
            time_label: "深夜",
            timeline_order: 2,
            evidence: {
              excerpt: "缺页留下的撕痕很新，像刚被人匆匆拆走。",
            },
          },
          {
            id: "event_003",
            title: "暗房旧照曝光",
            summary: "许燃显影出一组旧照片，画面中出现失踪者和贺叔。",
            chapter_id: "chapter_003",
            participants: ["char_001", "char_003", "char_004"],
            location_id: "loc_003",
            time_label: "凌晨前",
            timeline_order: 3,
            evidence: {
              excerpt: "照片里旅馆的钟停在两点十七分，和失踪案时间完全对上。",
            },
          },
          {
            id: "event_004",
            title: "隧道追逐",
            summary: "众人沿着排水隧道追逐幕后联系人，更多旧城秘密被迫暴露。",
            chapter_id: "chapter_004",
            participants: ["char_001", "char_002", "char_003"],
            location_id: "loc_004",
            time_label: "拂晓",
            timeline_order: 4,
            evidence: {
              excerpt: "水声掩住了脚步，却盖不住金属门被撞开的回响。",
            },
          },
        ],
        locations: deepClone(locationSeeds),
        timeline: [
          { order: 1, event_id: "event_001" },
          { order: 2, event_id: "event_002" },
          { order: 3, event_id: "event_003" },
          { order: 4, event_id: "event_004" },
        ],
      },
      script: {
        id: "script_001",
        title: "旧城雨夜",
        style: "film",
        version: "v2",
        logline: "青年侦探在暴雨中的旧城追查失踪案，一层层逼近被隐藏多年的真相。",
        source_event_ids: ["event_001", "event_002", "event_003", "event_004"],
        scenes: [],
      },
      storyboard: { shots: [] },
      review: {
        reviewed_at: "2026-06-05T15:12:00+08:00",
        model: "n2s-reviewer-demo",
        issues: [],
      },
      quality: {
        total_score: 0,
        dimensions: [],
      },
      export: {
        exported_at: "2026-06-05T15:20:00+08:00",
        exporter_version: "frontend-prototype-1.0",
        validated: true,
        validation_errors: [],
      },
      extensions: {},
      meta: {
        graph_stale: false,
        review_stale: false,
        quality_stale: false,
        storyboard_stale: false,
        export_stale: false,
        graph_mode: "demo",
        layout: {
          char_001: { x: 52, y: 28 },
          char_002: { x: 22, y: 54 },
          char_003: { x: 74, y: 52 },
          char_004: { x: 49, y: 78 },
        },
      },
      tasks: [
        {
          id: "task_001",
          type: "source_parse",
          status: "succeeded",
          progress: 100,
          message: "小说解析完成，已拆分 4 章。",
          updated_at: "2026-06-05T13:40:00+08:00",
        },
        {
          id: "task_002",
          type: "graph_extract",
          status: "succeeded",
          progress: 100,
          message: "人物、关系与故事事件抽取完成。",
          updated_at: "2026-06-05T14:05:00+08:00",
        },
        {
          id: "task_003",
          type: "script_generation",
          status: "succeeded",
          progress: 100,
          message: "电影风格剧本已生成。",
          updated_at: "2026-06-05T14:22:00+08:00",
        },
        {
          id: "task_004",
          type: "script_review",
          status: "succeeded",
          progress: 100,
          message: "AI 审校完成，发现 3 个问题。",
          updated_at: "2026-06-05T15:12:00+08:00",
        },
        {
          id: "task_005",
          type: "quality_scoring",
          status: "succeeded",
          progress: 100,
          message: "质量评估已生成。",
          updated_at: "2026-06-05T15:15:00+08:00",
        },
        {
          id: "task_006",
          type: "storyboard_generation",
          status: "succeeded",
          progress: 100,
          message: "分镜脚本已完成。",
          updated_at: "2026-06-05T15:18:00+08:00",
        },
        {
          id: "task_007",
          type: "yaml_export",
          status: "succeeded",
          progress: 100,
          message: "YAML 通过 Schema 校验并已导出。",
          updated_at: "2026-06-05T15:20:00+08:00",
        },
      ],
      activity_log: [
        {
          id: "log_001",
          time: "2026-06-05T15:20:00+08:00",
          title: "导出 YAML",
          detail: "结构已按 schema_version 1.0 通过校验。",
        },
        {
          id: "log_002",
          time: "2026-06-05T15:18:00+08:00",
          title: "生成分镜",
          detail: "为 4 个场次生成了 8 个镜头。",
        },
        {
          id: "log_003",
          time: "2026-06-05T15:15:00+08:00",
          title: "刷新质量评分",
          detail: "总分 87，完整性与改编忠实度表现较好。",
        },
      ],
    };

    project.script = buildScriptFromStoryGraph(project, "film", "v2");
    project.storyboard = buildStoryboardFromScript(project);
    project.review = buildReviewFromScript(project);
    project.quality = buildQualityFromReview(project);
    project.export.validation_errors = [];
    return project;
  }

  function nextVersion(previousVersion) {
    const match = String(previousVersion || "v0").match(/(\d+)/);
    const nextNumber = match ? Number(match[1]) + 1 : 1;
    return "v" + nextNumber;
  }

  function getCharacterName(project, characterId) {
    const found = project.characters.find((character) => character.id === characterId);
    return found ? found.name : "未命名角色";
  }

  function getLocationName(project, locationId) {
    const found = project.story_graph.locations.find((location) => location.id === locationId);
    return found ? found.name : "未标注地点";
  }

  function buildScriptFromStoryGraph(project, styleKey, nextScriptVersion) {
    const style = styleLibrary[styleKey] || styleLibrary.film;
    const scenes = project.story_graph.events
      .slice()
      .sort((a, b) => a.timeline_order - b.timeline_order)
      .map((event, index) => {
        const leadCharacterId = event.participants[0];
        const leadName = getCharacterName(project, leadCharacterId);
        const supportName = getCharacterName(project, event.participants[1] || leadCharacterId);
        const locationName = getLocationName(project, event.location_id);

        return {
          id: "scene_" + String(index + 1).padStart(3, "0"),
          index: index + 1,
          title: event.title,
          location: locationName,
          time: event.time_label || "未标注时间",
          characters: event.participants.slice(),
          source_event_ids: [event.id],
          synopsis: event.summary + " " + style.description,
          beats: [
            {
              type: "action",
              content:
                style.actionTone +
                " " +
                leadName +
                "在" +
                locationName +
                "接住这段情节的重心，" +
                event.summary,
            },
            {
              type: "action",
              content:
                "场面节奏采用" +
                style.pacing +
                "推进，环境中的声响与空间阻力不断压迫人物判断。",
            },
            {
              type: "dialogue",
              character_id: leadCharacterId,
              character_name: leadName,
              emotion: style.emotion,
              content:
                "先别急着下结论，" +
                supportName +
                "留下的这道缝隙，正是我们进入真相的入口。",
            },
          ],
        };
      });

    return {
      id: project.script.id || "script_001",
      title: project.project.title,
      style: styleKey,
      version: nextScriptVersion || nextVersion(project.script.version),
      logline:
        project.project.title +
        "以" +
        style.label +
        "风格重构，聚焦人物关系、案件推进与旧城氛围。",
      source_event_ids: project.story_graph.events.map((event) => event.id),
      scenes: scenes,
    };
  }

  function buildStoryboardFromScript(project) {
    const style = styleLibrary[project.script.style] || styleLibrary.film;
    const shots = [];

    project.script.scenes.forEach((scene, sceneIndex) => {
      const actionBeats = scene.beats.filter((beat) => beat.type === "action");
      const leadCharacter = getCharacterName(project, scene.characters[0]);

      actionBeats.forEach((beat, beatIndex) => {
        shots.push({
          id: "shot_" + String(shots.length + 1).padStart(3, "0"),
          scene_id: scene.id,
          index: beatIndex + 1,
          image_description:
            scene.title +
            " / " +
            beat.content.slice(0, 52) +
            (beat.content.length > 52 ? "..." : ""),
          shot_size: style.shotSizes[(sceneIndex + beatIndex) % style.shotSizes.length],
          camera_movement:
            style.cameraMoves[(sceneIndex + beatIndex) % style.cameraMoves.length],
          lighting: style.lighting,
          duration_seconds: 4 + ((sceneIndex + beatIndex) % 3),
          audio:
            style.audio +
            "，重点跟随" +
            leadCharacter +
            "的动作与视线变化。",
        });
      });
    });

    return { shots: shots };
  }

  function buildReviewFromScript(project) {
    const issues = [];

    project.script.scenes.forEach((scene, index) => {
      if (!scene.location || !scene.time) {
        issues.push({
          id: "issue_" + String(issues.length + 1).padStart(3, "0"),
          type: "scene_integrity",
          severity: "high",
          scene_id: scene.id,
          beat_index: 1,
          message: "场次缺少明确地点或时间信息，难以进入分镜阶段。",
          suggestion: "补充场景时间与空间锚点，再进行分镜生成。",
        });
      }

      const dialogueCount = scene.beats.filter((beat) => beat.type === "dialogue").length;
      const ratio = scene.beats.length === 0 ? 0 : dialogueCount / scene.beats.length;

      if (ratio > 0.55) {
        issues.push({
          id: "issue_" + String(issues.length + 1).padStart(3, "0"),
          type: "dialogue_distribution",
          severity: "medium",
          scene_id: scene.id,
          beat_index: scene.beats.findIndex((beat) => beat.type === "dialogue") + 1,
          message: "对白占比偏高，动作信息可能不足以支撑镜头变化。",
          suggestion: "补一段行动或环境反应，降低对白对节奏的挤占。",
        });
      }

      if (index > 0 && !scene.beats.some((beat) => beat.type === "transition")) {
        issues.push({
          id: "issue_" + String(issues.length + 1).padStart(3, "0"),
          type: "continuity",
          severity: index === 1 ? "medium" : "low",
          scene_id: scene.id,
          beat_index: 1,
          message: "场次切换缺少明确转场提示，连续观看时可能略显跳跃。",
          suggestion: "在场次开头增加环境变化或角色动作承接。",
        });
      }
    });

    return {
      reviewed_at: nowIso(),
      model: "n2s-reviewer-demo",
      issues: issues.slice(0, 4),
    };
  }

  function buildQualityFromReview(project) {
    const issues = project.review.issues || [];
    const sceneCount = project.script.scenes.length || 1;
    const hasStoryMapping = project.script.scenes.every(
      (scene) => Array.isArray(scene.source_event_ids) && scene.source_event_ids.length > 0,
    );

    const completeness = Math.max(
      58,
      92 -
        project.script.scenes.filter(
          (scene) => !scene.location || !scene.time || !scene.synopsis || scene.beats.length === 0,
        ).length *
          10,
    );
    const consistency = Math.max(
      55,
      90 -
        issues.filter((issue) => issue.type === "character_consistency" || issue.type === "timeline")
          .length *
          8,
    );
    const sceneContinuity = Math.max(
      52,
      88 - issues.filter((issue) => issue.type === "continuity").length * 6,
    );
    const dialogueDistribution = Math.max(
      60,
      90 - issues.filter((issue) => issue.type === "dialogue_distribution").length * 10,
    );
    const adaptationFidelity = hasStoryMapping
      ? Math.min(95, 74 + Math.round((sceneCount / Math.max(project.story_graph.events.length, 1)) * 18))
      : 66;

    const dimensions = [
      {
        name: "完整性",
        key: "completeness",
        score: completeness,
        comment: "场次字段与片段结构基本完整，适合进入下一阶段加工。",
      },
      {
        name: "一致性",
        key: "consistency",
        score: consistency,
        comment: "角色称谓与事件顺序大体稳定，仍需人工复核关键信息。",
      },
      {
        name: "场景连续性",
        key: "scene_continuity",
        score: sceneContinuity,
        comment: "转场与空间承接有一定基础，但仍能继续压缩跳跃感。",
      },
      {
        name: "对白分布",
        key: "dialogue_distribution",
        score: dialogueDistribution,
        comment: "对白和动作的占比接近可拍摄脚本需求，仍可继续微调。",
      },
      {
        name: "改编忠实度",
        key: "adaptation_fidelity",
        score: adaptationFidelity,
        comment: "场次与事件保留了映射关系，便于追溯原文来源。",
      },
    ];

    const totalScore = Math.round(
      dimensions.reduce((sum, item) => sum + item.score, 0) / dimensions.length,
    );

    return {
      total_score: totalScore,
      dimensions: dimensions,
    };
  }

  function buildExtractionFromSource(project) {
    const titleBase = String(project.project.title || "新项目").replace(/\.[^.]+$/, "");
    const chapterCount = project.source.chapters.length || 3;
    const characters = [
      {
        id: "char_001",
        name: "主角",
        aliases: [titleBase.slice(0, 4) || "主人公"],
        identity: "案件推动者",
        description: "围绕原文线索被重新抽取出的主视角人物。",
        first_appearance: {
          chapter_id: project.source.chapters[0] ? project.source.chapters[0].id : "chapter_001",
          excerpt: project.source.chapters[0]
            ? project.source.chapters[0].summary
            : "主角进入故事现场。",
        },
      },
      {
        id: "char_002",
        name: "协作者",
        aliases: [],
        identity: "信息提供者",
        description: "为主角提供事件背景、资料或行动支持。",
        first_appearance: {
          chapter_id: project.source.chapters[1] ? project.source.chapters[1].id : "chapter_001",
          excerpt: project.source.chapters[1]
            ? project.source.chapters[1].summary
            : "协作者补充了一段缺失的信息。",
        },
      },
      {
        id: "char_003",
        name: "关键证人",
        aliases: [],
        identity: "图像或口述证据持有者",
        description: "掌握指向转折的信息节点，是中后段推进的关键。",
        first_appearance: {
          chapter_id: project.source.chapters[2] ? project.source.chapters[2].id : "chapter_001",
          excerpt: project.source.chapters[2]
            ? project.source.chapters[2].summary
            : "关键证人交出了一份证据。",
        },
      },
      {
        id: "char_004",
        name: "隐藏对手",
        aliases: [],
        identity: "阻碍调查的力量",
        description: "在前台或幕后施加阻力，维持悬念与冲突。",
        first_appearance: {
          chapter_id: project.source.chapters[0] ? project.source.chapters[0].id : "chapter_001",
          excerpt: "有人的名字没有被直接写出来，却反复留下痕迹。",
        },
      },
    ];

    const relationships = [
      {
        id: "rel_001",
        from_character_id: "char_001",
        to_character_id: "char_002",
        type: "ally",
        label: "协同",
        description: "两人共同推动线索梳理与事件推进。",
        evidence: {
          chapter_id: project.source.chapters[1] ? project.source.chapters[1].id : "chapter_001",
          excerpt: project.source.chapters[1]
            ? project.source.chapters[1].summary
            : "两人在同一条线索上达成合作。",
        },
        confidence: 0.78,
      },
      {
        id: "rel_002",
        from_character_id: "char_001",
        to_character_id: "char_004",
        type: "enemy",
        label: "对抗",
        description: "主角与隐藏对手之间存在明显冲突。",
        evidence: {
          chapter_id: project.source.chapters[Math.min(2, chapterCount - 1)]
            ? project.source.chapters[Math.min(2, chapterCount - 1)].id
            : "chapter_001",
          excerpt: "关键阻碍反复出现，推动主角改变判断路径。",
        },
        confidence: 0.74,
      },
    ];

    const events = project.source.chapters.slice(0, 4).map((chapter, index) => ({
      id: "event_" + String(index + 1).padStart(3, "0"),
      title: chapter.title || "事件 " + (index + 1),
      summary: chapter.summary || "该章节被前端原型压缩为一条核心剧情事件。",
      chapter_id: chapter.id,
      participants:
        index === 0
          ? ["char_001", "char_004"]
          : index === 1
            ? ["char_001", "char_002"]
            : index === 2
              ? ["char_001", "char_003"]
              : ["char_001", "char_002", "char_003"],
      location_id: locationSeeds[index % locationSeeds.length].id,
      time_label: timeSeeds[index % timeSeeds.length],
      timeline_order: index + 1,
      evidence: {
        excerpt: chapter.summary || chapter.title || "来自上传文本的自动摘要。",
      },
    }));

    const timeline = events.map((event, index) => ({
      order: index + 1,
      event_id: event.id,
    }));

    return {
      characters: characters,
      relationships: relationships,
      story_graph: {
        events: events,
        locations: deepClone(locationSeeds),
        timeline: timeline,
      },
      layout: {
        char_001: { x: 50, y: 26 },
        char_002: { x: 18, y: 52 },
        char_003: { x: 80, y: 52 },
        char_004: { x: 50, y: 78 },
      },
    };
  }

  window.Novel2ScreenData = {
    styleLibrary: styleLibrary,
    deepClone: deepClone,
    nowIso: nowIso,
    createDemoProject: createDemoProject,
    buildScriptFromStoryGraph: buildScriptFromStoryGraph,
    buildStoryboardFromScript: buildStoryboardFromScript,
    buildReviewFromScript: buildReviewFromScript,
    buildQualityFromReview: buildQualityFromReview,
    buildExtractionFromSource: buildExtractionFromSource,
    nextVersion: nextVersion,
  };
})();
