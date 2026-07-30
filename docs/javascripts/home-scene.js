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
    var colors = ["#37c8b2", "#ffb347", "#ef6f61", "#d7e04b"];
    var points = [];
    var signals = [];
    var anchors = [];
    var width = 0;
    var height = 0;
    var pointer = { x: -1000, y: -1000 };
    var frame = 0;

    function seed() {
      var count = Math.max(18, Math.min(36, Math.round(width / 42)));
      points = Array.from({ length: count }, function (_, index) {
        return {
          x: width * (0.46 + Math.random() * 0.58),
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.22,
          vy: (Math.random() - 0.5) * 0.18,
          size: 5 + Math.random() * 9,
          color: colors[index % colors.length],
          phase: Math.random() * Math.PI * 2
        };
      });
      anchors = [
        { x: width * 0.46, y: height * 0.68 },
        { x: width * 0.61, y: height * 0.47 },
        { x: width * 0.76, y: height * 0.58 },
        { x: width * 0.92, y: height * 0.31 }
      ];
      signals = Array.from({ length: 11 }, function (_, index) {
        return {
          progress: index / 11,
          speed: 0.000025 + (index % 3) * 0.000004,
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

    function drawGrid() {
      context.strokeStyle = "rgba(220, 238, 234, 0.055)";
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

    function drawPipeline(time) {
      if (!anchors.length) return;
      context.strokeStyle = "rgba(205, 226, 221, 0.18)";
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
        context.strokeStyle = "rgba(114, 216, 202, 0.28)";
        context.strokeRect(anchor.x - pulse, anchor.y - pulse, pulse * 2, pulse * 2);
        context.fillStyle = colors[index % colors.length];
        context.fillRect(anchor.x - 2.8, anchor.y - 2.8, 5.6, 5.6);
      });

      signals.forEach(function (signal, index) {
        if (!reduceMotion) signal.progress = (signal.progress + signal.speed * 16.7) % 1;
        var position = pathPoint(signal.progress);
        context.save();
        context.translate(position.x, position.y);
        context.rotate(-0.18 + Math.sin(time * 0.001 + index) * 0.08);
        context.fillStyle = index % 3 === 0 ? "rgba(242, 247, 244, 0.92)" : signal.color;
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
      context.clearRect(0, 0, width, height);
      context.fillStyle = "#11191a";
      context.fillRect(0, 0, width, height);
      drawGrid();
      drawPipeline(time);

      for (var i = 0; i < points.length; i += 1) {
        var a = points[i];
        for (var j = i + 1; j < points.length; j += 1) {
          var b = points[j];
          var dx = a.x - b.x;
          var dy = a.y - b.y;
          var distance = Math.sqrt(dx * dx + dy * dy);
          if (distance < 155) {
            context.strokeStyle = "rgba(175, 205, 200," + ((1 - distance / 155) * 0.2) + ")";
            context.beginPath();
            context.moveTo(a.x, a.y);
            context.lineTo(b.x, b.y);
            context.stroke();
          }
        }
      }

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
    resize();

    if (!reduceMotion) frame = window.requestAnimationFrame(draw);
    window.addEventListener("pagehide", function () {
      if (frame) window.cancelAnimationFrame(frame);
    }, { once: true });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initHomeScene);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHomeScene);
  } else {
    initHomeScene();
  }
})();
