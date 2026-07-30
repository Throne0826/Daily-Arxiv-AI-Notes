(function () {
  "use strict";

  var indexPromise = null;
  var categoryLabels = {
    llm_reasoning: "LLM Reasoning",
    llm_agent: "LLM Agent",
    multi_agent: "Multi-Agent",
    llm_alignment: "对齐 / RLHF",
    llm_safety: "LLM 安全",
    hallucination: "幻觉检测",
    llm_evaluation: "LLM 评测",
    llm_efficiency: "LLM 效率",
    llm_pretraining: "预训练",
    knowledge_editing: "知识编辑",
    llm_interpretability: "LLM 机制与可解释性",
    llm_nlp: "LLM 其他",
    image_generation: "图像生成",
    video_generation: "视频生成",
    multimodal_vlm: "多模态 VLM",
    vlm_reasoning: "VLM Reasoning",
    vlm_efficiency: "VLM Efficiency",
    autonomous_driving: "自动驾驶",
    robotics: "机器人 / 具身智能",
    reinforcement_learning: "强化学习",
    recommender: "推荐系统"
  };

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function paperMeta(location) {
    var match = /^arxiv_daily\/(\d{4}-\d{2}-\d{2})\/([^/]+)\/[^/]+\/?$/.exec(location);
    return match ? { date: match[1], category: match[2] } : null;
  }

  function loadIndex() {
    if (indexPromise) return indexPromise;
    var url = new URL("../search/search_index.json", window.location.href);
    indexPromise = fetch(url)
      .then(function (response) {
        if (!response.ok) throw new Error("search index HTTP " + response.status);
        return response.json();
      })
      .then(function (payload) {
        return (payload.docs || [])
          .map(function (doc) {
            var meta = paperMeta(doc.location || "");
            if (!meta) return null;
            var tags = Array.isArray(doc.tags) ? doc.tags.join(" ") : "";
            return {
              location: doc.location,
              title: String(doc.title || "").replace(/^\[论文解读\]\s*/, ""),
              text: String(doc.text || ""),
              date: meta.date,
              category: meta.category,
              haystack: [doc.title || "", doc.text || "", tags, categoryLabels[meta.category] || ""]
                .join(" ")
                .toLowerCase()
            };
          })
          .filter(Boolean)
          .sort(function (a, b) {
            return b.date.localeCompare(a.date) || a.title.localeCompare(b.title);
          });
      });
    return indexPromise;
  }

  function queryParts(value) {
    return value
      .toLowerCase()
      .trim()
      .split(/[\s,，。:：;；/]+/)
      .filter(Boolean);
  }

  function readParams() {
    var params = new URLSearchParams(window.location.search);
    return { q: params.get("q") || "", category: params.get("category") || "" };
  }

  function updateUrl(query, category) {
    var params = new URLSearchParams();
    if (query) params.set("q", query);
    if (category) params.set("category", category);
    var next = window.location.pathname + (params.toString() ? "?" + params.toString() : "");
    window.history.replaceState(null, "", next);
  }

  function populateCategories(select, docs) {
    var present = Object.create(null);
    docs.forEach(function (doc) { present[doc.category] = true; });
    Object.keys(categoryLabels).forEach(function (category) {
      if (!present[category]) return;
      var option = document.createElement("option");
      option.value = category;
      option.textContent = categoryLabels[category];
      select.appendChild(option);
    });
  }

  function render(docs, input, select, status, results) {
    var query = input.value.trim();
    var category = select.value;
    var parts = queryParts(query);
    var filtered = docs.filter(function (doc) {
      if (category && doc.category !== category) return false;
      return parts.every(function (part) { return doc.haystack.indexOf(part) >= 0; });
    });
    updateUrl(query, category);

    if (!query && !category) {
      status.textContent = "输入关键词或选择领域开始检索，共收录 " + docs.length + " 篇。";
      results.innerHTML = "";
      return;
    }

    status.textContent = "找到 " + filtered.length + " 篇论文";
    var base = new URL("../", window.location.href);
    results.innerHTML = filtered.slice(0, 100).map(function (doc) {
      var href = new URL(doc.location, base).href;
      var snippet = doc.text ? '<div class="daily-search-snippet">' + escapeHtml(doc.text) + "</div>" : "";
      return '<li class="daily-search-hit">' +
        '<a href="' + escapeHtml(href) + '">' + escapeHtml(doc.title) + "</a>" +
        '<div class="daily-search-meta">' + escapeHtml(doc.date) + " · " +
        escapeHtml(categoryLabels[doc.category] || doc.category) + "</div>" + snippet + "</li>";
    }).join("");
  }

  function init() {
    var root = document.getElementById("daily-search-root");
    if (!root || root.dataset.ready === "true") return;
    root.dataset.ready = "true";
    var input = document.getElementById("daily-search-input");
    var select = document.getElementById("daily-search-category");
    var status = document.getElementById("daily-search-status");
    var results = document.getElementById("daily-search-results");
    var initial = readParams();
    input.value = initial.q;

    loadIndex().then(function (docs) {
      populateCategories(select, docs);
      if (categoryLabels[initial.category]) select.value = initial.category;
      var timer = null;
      function run() { render(docs, input, select, status, results); }
      input.addEventListener("input", function () {
        window.clearTimeout(timer);
        timer = window.setTimeout(run, 140);
      });
      select.addEventListener("change", run);
      run();
    }).catch(function () {
      status.textContent = "搜索索引加载失败，请先构建站点。";
    });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
