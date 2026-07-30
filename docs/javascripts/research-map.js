(function () {
  "use strict";

  var SVG_NS = "http://www.w3.org/2000/svg";
  var GROUP_LAYOUT = {
    llm: { x: 330, y: 286, radius: 205 },
    generation_multimodal: { x: 760, y: 168, radius: 122 },
    decision_embodied: { x: 750, y: 414, radius: 138 }
  };

  function svgElement(name, attributes) {
    var element = document.createElementNS(SVG_NS, name);
    Object.keys(attributes || {}).forEach(function (key) {
      element.setAttribute(key, String(attributes[key]));
    });
    return element;
  }

  function shortLabel(value) {
    return value
      .replace("机器人 / 具身智能", "具身智能")
      .replace("生成与多模态", "生成 / 多模态")
      .replace("LLM 机制与可解释性", "LLM 可解释性")
      .replace("强化学习", "RL")
      .slice(0, 15);
  }

  function categoryPositions(categories) {
    var positions = {};
    Object.keys(GROUP_LAYOUT).forEach(function (groupId) {
      var groupCategories = categories
        .filter(function (category) {
          return category.group === groupId && category.count > 0;
        })
        .sort(function (left, right) {
          return right.count - left.count || left.label.localeCompare(right.label);
        });
      var layout = GROUP_LAYOUT[groupId];
      groupCategories.forEach(function (category, index) {
        var start = groupId === "llm" ? -Math.PI * 0.88 : -Math.PI * 0.72;
        var angle = start + (Math.PI * 2 * index) / Math.max(groupCategories.length, 1);
        var ring = layout.radius * (0.66 + (index % 2) * 0.22);
        positions[category.id] = {
          x: layout.x + Math.cos(angle) * ring,
          y: layout.y + Math.sin(angle) * ring,
          group: groupId
        };
      });
    });
    return positions;
  }

  function updateDetail(detail, title, text, href) {
    if (!detail) return;
    var heading = detail.querySelector("strong");
    var paragraph = detail.querySelector("p");
    if (heading) heading.textContent = title;
    if (paragraph) paragraph.textContent = text;
    var existing = detail.querySelector("a");
    if (existing) existing.remove();
    if (href) {
      var link = document.createElement("a");
      link.href = href;
      link.textContent = "查看该方向";
      detail.appendChild(link);
    }
  }

  function renderNetwork(root, data) {
    var canvas = root.querySelector("[data-map-network]");
    if (!canvas || canvas.dataset.ready === "true") return;
    canvas.dataset.ready = "true";
    var detail = root.querySelector("[data-map-detail]");
    var activeCategories = data.categories.filter(function (category) {
      return category.count > 0;
    });
    var categoriesById = {};
    activeCategories.forEach(function (category) {
      categoriesById[category.id] = category;
    });
    var positions = categoryPositions(activeCategories);

    Object.keys(GROUP_LAYOUT).forEach(function (groupId) {
      var layout = GROUP_LAYOUT[groupId];
      var group = (data.groups || []).find(function (item) {
        return item.id === groupId;
      });
      var orbit = svgElement("circle", {
        cx: layout.x,
        cy: layout.y,
        r: layout.radius,
        class: "research-orbit",
        "data-map-group": groupId
      });
      canvas.appendChild(orbit);
      var groupLabel = svgElement("text", {
        x: layout.x,
        y: layout.y + 4,
        class: "research-orbit__label",
        "text-anchor": "middle",
        "data-map-group": groupId
      });
      groupLabel.textContent = group ? group.label : groupId;
      canvas.appendChild(groupLabel);
    });

    (data.connections || []).forEach(function (connection) {
      var source = positions[connection.source];
      var target = positions[connection.target];
      if (!source || !target) return;
      var line = svgElement("line", {
        x1: source.x,
        y1: source.y,
        x2: target.x,
        y2: target.y,
        class: "research-edge",
        "stroke-width": Math.min(7, 1 + connection.count * 0.72),
        tabindex: "0"
      });
      var title = svgElement("title");
      title.textContent = connection.source_label + " × " + connection.target_label + "：" + connection.count + " 篇";
      line.appendChild(title);
      function showConnection() {
        updateDetail(
          detail,
          connection.source_label + " × " + connection.target_label,
          "共有 " + connection.count + " 篇论文同时进入这两个方向。"
        );
      }
      line.addEventListener("mouseenter", showConnection);
      line.addEventListener("focus", showConnection);
      canvas.appendChild(line);
    });

    var maximum = Math.max.apply(
      null,
      activeCategories.map(function (category) {
        return category.count;
      }).concat([1])
    );
    activeCategories.forEach(function (category) {
      var position = positions[category.id];
      if (!position) return;
      var radius = 9 + Math.sqrt(category.count / maximum) * 17;
      var link = svgElement("a", {
        href: category.href,
        class: "research-network__node",
        "data-map-group": category.group
      });
      var title = svgElement("title");
      title.textContent = category.label + "：" + category.count + " 篇";
      var circle = svgElement("circle", {
        cx: position.x,
        cy: position.y,
        r: radius
      });
      var count = svgElement("text", {
        x: position.x,
        y: position.y + 4,
        "text-anchor": "middle",
        class: "research-network__count"
      });
      count.textContent = category.count;
      var label = svgElement("text", {
        x: position.x,
        y: position.y + radius + 15,
        "text-anchor": "middle",
        class: "research-network__label"
      });
      label.textContent = shortLabel(category.label);
      function showCategory() {
        var delta = category.delta > 0 ? "+" + category.delta : String(category.delta);
        updateDetail(
          detail,
          category.label,
          "累计 " + category.count + " 篇，最新日变化 " + delta + " 篇。",
          category.href
        );
      }
      link.addEventListener("mouseenter", showCategory);
      link.addEventListener("focus", showCategory);
      link.appendChild(title);
      link.appendChild(circle);
      link.appendChild(count);
      link.appendChild(label);
      canvas.appendChild(link);
    });
  }

  function initResearchMap() {
    document.querySelectorAll("[data-research-map]").forEach(function (root) {
      if (root.dataset.ready === "true") return;
      root.dataset.ready = "true";
      var payload = root.querySelector("[data-research-map-data]");
      if (!payload) return;
      var data;
      try {
        data = JSON.parse(payload.textContent);
      } catch (error) {
        return;
      }
      var buttons = Array.from(root.querySelectorAll("[data-map-view]"));
      var panels = Array.from(root.querySelectorAll("[data-map-panel]"));
      buttons.forEach(function (button) {
        button.addEventListener("click", function () {
          var selected = button.dataset.mapView;
          buttons.forEach(function (candidate) {
            var active = candidate === button;
            candidate.classList.toggle("is-active", active);
            candidate.setAttribute("aria-selected", String(active));
          });
          panels.forEach(function (panel) {
            var active = panel.dataset.mapPanel === selected;
            panel.classList.toggle("is-active", active);
            panel.hidden = !active;
          });
        });
      });
      renderNetwork(root, data);
    });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initResearchMap);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResearchMap);
  } else {
    initResearchMap();
  }
})();
