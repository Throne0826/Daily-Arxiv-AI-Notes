(function () {
  "use strict";

  function initHomeScene() {
    var canvas = document.getElementById("home-scene");
    if (!canvas || canvas.dataset.ready === "true") return;
    canvas.dataset.ready = "true";
    document.documentElement.classList.add("has-home-scene");

    var context = canvas.getContext("2d");
    var hero = canvas.closest(".home-hero");
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var points = [];
    var signals = [];
    var anchors = [];
    var width = 0;
    var height = 0;
    var pointer = { x: -1000, y: -1000 };
    var frame = 0;

    function palette() {
      var dark = document.documentElement.getAttribute("data-md-color-scheme") === "slate";
      return dark
        ? {
            background: "#101819",
            grid: "rgba(220, 238, 234, 0.06)",
            line: "rgba(205, 226, 221, 0.22)",
            link: "rgba(175, 205, 200, 0.22)",
            signal: "rgba(242, 247, 244, 0.94)",
            halo: "rgba(104, 216, 204, 0.18)",
            colors: ["#68d8cc", "#ffd080", "#ff9388", "#a7d66d"]
          }
        : {
            background: "#edf3f0",
            grid: "rgba(32, 67, 63, 0.075)",
            line: "rgba(32, 91, 84, 0.23)",
            link: "rgba(45, 91, 85, 0.2)",
            signal: "rgba(23, 34, 35, 0.88)",
            halo: "rgba(8, 127, 117, 0.12)",
            colors: ["#087f75", "#b36f08", "#d9584c", "#728d1f"]
          };
    }

    function seed() {
      var colors = palette().colors;
      var count = Math.max(28, Math.min(52, Math.round(width / 29)));
      points = Array.from({ length: count }, function (_, index) {
        return {
          x: width * (0.015 + Math.random() * 0.97),
          y: height * (0.04 + Math.random() * 0.9),
          vx: (Math.random() - 0.5) * 0.2,
          vy: (Math.random() - 0.5) * 0.16,
          size: 4 + Math.random() * 8,
          color: colors[index % colors.length],
          phase: Math.random() * Math.PI * 2,
          alpha: 0.48 + Math.random() * 0.42
        };
      });
      anchors = [
        { x: width * 0.04, y: height * 0.74 },
        { x: width * 0.24, y: height * 0.54 },
        { x: width * 0.47, y: height * 0.64 },
        { x: width * 0.7, y: height * 0.4 },
        { x: width * 0.94, y: height * 0.57 }
      ];
      signals = Array.from({ length: 15 }, function (_, index) {
        return {
          progress: index / 15,
          speed: 0.000022 + (index % 4) * 0.000003,
          color: colors[index % colors.length]
        };
      });
    }

    function resize() {
      var rect = hero.getBoundingClientRect();
      width = Math.max(1, Math.round(rect.width));
      height = Math.max(1, Math.round(rect.height));
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      seed();
      draw(0);
    }

    function drawGrid(theme) {
      context.strokeStyle = theme.grid;
      context.lineWidth = 1;
      for (var x = 28; x < width; x += 56) {
        context.beginPath();
        context.moveTo(x, 0);
        context.lineTo(x, height);
        context.stroke();
      }
      for (var y = 28; y < height; y += 56) {
        context.beginPath();
        context.moveTo(0, y);
        context.lineTo(width, y);
        context.stroke();
      }
    }

    function pathPoint(progress) {
      var scaled = Math.max(0, Math.min(0.9999, progress)) * (anchors.length - 1);
      var index = Math.floor(scaled);
      var local = scaled - index;
      var smooth = local * local * (3 - 2 * local);
      var start = anchors[index];
      var end = anchors[Math.min(index + 1, anchors.length - 1)];
      return {
        x: start.x + (end.x - start.x) * smooth,
        y: start.y + (end.y - start.y) * smooth
      };
    }

    function drawPipeline(time, theme) {
      if (!anchors.length) return;
      context.strokeStyle = theme.line;
      context.lineWidth = 1.5;
      context.beginPath();
      context.moveTo(anchors[0].x, anchors[0].y);
      for (var i = 1; i < anchors.length; i += 1) {
        var previous = anchors[i - 1];
        var current = anchors[i];
        var middle = (previous.x + current.x) / 2;
        context.bezierCurveTo(middle, previous.y, middle, current.y, current.x, current.y);
      }
      context.stroke();

      anchors.forEach(function (anchor, index) {
        var pulse = 11 + Math.sin(time * 0.0013 + index) * 2;
        context.strokeStyle = theme.halo;
        context.strokeRect(anchor.x - pulse, anchor.y - pulse, pulse * 2, pulse * 2);
        context.fillStyle = theme.colors[index % theme.colors.length];
        context.fillRect(anchor.x - 2.8, anchor.y - 2.8, 5.6, 5.6);
      });

      signals.forEach(function (signal, index) {
        if (!reduceMotion) signal.progress = (signal.progress + signal.speed * 16.7) % 1;
        var position = pathPoint(signal.progress);
        context.save();
        context.translate(position.x, position.y);
        context.rotate(-0.18 + Math.sin(time * 0.001 + index) * 0.08);
        context.fillStyle = index % 3 === 0 ? theme.signal : signal.color;
        context.fillRect(-5, -6.5, 10, 13);
        if (index % 3 === 0) {
          context.fillStyle = signal.color;
          context.fillRect(-3, -2.5, 6, 1.2);
          context.fillRect(-3, 1, 4.5, 1);
        }
        context.restore();
      });
    }

    function draw(time) {
      if (!canvas.isConnected) {
        if (frame) window.cancelAnimationFrame(frame);
        window.removeEventListener("resize", resize);
        return;
      }
      var theme = palette();
      context.clearRect(0, 0, width, height);
      context.fillStyle = theme.background;
      context.fillRect(0, 0, width, height);
      drawGrid(theme);
      drawPipeline(time, theme);

      for (var i = 0; i < points.length; i += 1) {
        var a = points[i];
        for (var j = i + 1; j < points.length; j += 1) {
          var b = points[j];
          var dx = a.x - b.x;
          var dy = a.y - b.y;
          var distance = Math.sqrt(dx * dx + dy * dy);
          if (distance < 142) {
            context.globalAlpha = (1 - distance / 142) * 0.9;
            context.strokeStyle = theme.link;
            context.beginPath();
            context.moveTo(a.x, a.y);
            context.lineTo(b.x, b.y);
            context.stroke();
          }
        }
      }
      context.globalAlpha = 1;

      points.forEach(function (point) {
        var dx = point.x - pointer.x;
        var dy = point.y - pointer.y;
        var distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < 110 && distance > 0) {
          point.x += (dx / distance) * 0.7;
          point.y += (dy / distance) * 0.7;
        }

        if (!reduceMotion) {
          point.x += point.vx;
          point.y += point.vy + Math.sin(time * 0.0005 + point.phase) * 0.035;
          if (point.x < -24) point.x = width + 24;
          if (point.x > width + 24) point.x = -24;
          if (point.y < -24) point.y = height + 24;
          if (point.y > height + 24) point.y = -24;
        }

        context.save();
        context.globalAlpha = point.alpha;
        context.translate(point.x, point.y);
        context.rotate(Math.PI / 4 + Math.sin(time * 0.0004 + point.phase) * 0.08);
        context.fillStyle = point.color;
        context.fillRect(
          -point.size * 0.26,
          -point.size * 0.26,
          point.size * 0.52,
          point.size * 0.52
        );
        context.restore();
      });

      if (!reduceMotion) frame = window.requestAnimationFrame(draw);
    }

    hero.addEventListener("pointermove", function (event) {
      var rect = hero.getBoundingClientRect();
      pointer.x = event.clientX - rect.left;
      pointer.y = event.clientY - rect.top;
    });
    hero.addEventListener("pointerleave", function () {
      pointer.x = -1000;
      pointer.y = -1000;
    });
    window.addEventListener("resize", resize, { passive: true });
    var themeObserver = new MutationObserver(function (changes) {
      if (changes.some(function (change) { return change.attributeName === "data-md-color-scheme"; })) {
        seed();
        draw(performance.now());
      }
    });
    themeObserver.observe(document.documentElement, { attributes: true });
    resize();

    if (!reduceMotion) frame = window.requestAnimationFrame(draw);
    window.addEventListener("pagehide", function () {
      if (frame) window.cancelAnimationFrame(frame);
      themeObserver.disconnect();
    }, { once: true });
  }

  function initHomePipeline() {
    var lab = document.querySelector(".home-reading-lab");
    if (!lab || lab.dataset.ready === "true") return;
    lab.dataset.ready = "true";

    var steps = Array.prototype.slice.call(lab.querySelectorAll("[data-pipeline-step]"));
    var caption = lab.querySelector("[data-pipeline-caption]");
    var counter = lab.querySelector("[data-pipeline-counter]");
    var captions = [
      "过滤噪声，留下真正相关的工作",
      "把一篇论文放回它所属的研究网络",
      "沿原文章节还原问题、方法与公式",
      "让每个关键结论都能回到原文证据"
    ];
    var active = 0;
    var timer = 0;
    var visible = false;
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function selectStep(index) {
      active = (index + steps.length) % steps.length;
      lab.dataset.activeStep = String(active);
      steps.forEach(function (step, stepIndex) {
        var selected = stepIndex === active;
        step.classList.toggle("is-active", selected);
        if (selected) step.setAttribute("aria-current", "step");
        else step.removeAttribute("aria-current");
      });
      if (caption) caption.textContent = captions[active];
      if (counter) counter.textContent = String(active + 1).padStart(2, "0");
    }

    function stopRotation() {
      if (timer) window.clearInterval(timer);
      timer = 0;
    }

    function startRotation() {
      stopRotation();
      if (!reduceMotion && visible) {
        timer = window.setInterval(function () { selectStep(active + 1); }, 3200);
      }
    }

    steps.forEach(function (step, index) {
      ["pointerenter", "focusin", "click"].forEach(function (eventName) {
        step.addEventListener(eventName, function () {
          selectStep(index);
          startRotation();
        });
      });
    });

    var visibilityObserver = new IntersectionObserver(function (entries) {
      visible = entries[0] && entries[0].isIntersecting;
      if (visible) startRotation();
      else stopRotation();
    }, { threshold: 0.3 });
    visibilityObserver.observe(lab);

    var stepObserver = new IntersectionObserver(function (entries) {
      if (window.innerWidth > 760) return;
      var leading = entries
        .filter(function (entry) { return entry.isIntersecting; })
        .sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; })[0];
      if (leading) selectStep(Number(leading.target.dataset.pipelineStep));
    }, { rootMargin: "-28% 0px -42%", threshold: [0.35, 0.6, 0.9] });
    steps.forEach(function (step) { stepObserver.observe(step); });

    selectStep(0);
    window.addEventListener("pagehide", function () {
      stopRotation();
      visibilityObserver.disconnect();
      stepObserver.disconnect();
    }, { once: true });
  }

  function initHome() {
    initHomeScene();
    initHomePipeline();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initHome);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHome);
  } else {
    initHome();
  }
})();
