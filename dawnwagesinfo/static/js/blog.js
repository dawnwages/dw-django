/*
 * Behaviour for technical blog posts (see portfolio/tech_blocks.py).
 * Plain JavaScript, no build step. Each feature only runs when its block is
 * on the page, and the heavier libraries (Mermaid, KaTeX) load on demand.
 */
(function () {
  "use strict";

  var CDN = "https://cdn.jsdelivr.net/npm/";

  // Copy buttons -------------------------------------------------------------
  function codeToCopy(button) {
    var figure = button.closest("figure");
    if (!figure) return "";
    var selector = button.getAttribute("data-copy-target");
    if (selector) {
      return Array.prototype.map
        .call(figure.querySelectorAll(selector), function (el) { return el.textContent; })
        .join("\n");
    }
    var panel = figure.querySelector(".dw-tabs__panel:not([hidden])") || figure;
    var code = panel.querySelector("pre code") || panel.querySelector("pre");
    if (!code) return "";
    // Diff blocks: drop the leading +/- markers so the copied code runs.
    if (code.className.indexOf("language-diff-") !== -1) {
      return code.textContent
        .split("\n")
        .filter(function (line) { return line.charAt(0) !== "-"; })
        .map(function (line) { return /^[+ ]/.test(line) ? line.slice(1) : line; })
        .join("\n");
    }
    return code.textContent;
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-copy]");
    if (!button || !navigator.clipboard) return;
    navigator.clipboard.writeText(codeToCopy(button)).then(function () {
      button.textContent = "Copied";
      button.classList.add("is-copied");
      setTimeout(function () {
        button.textContent = "Copy";
        button.classList.remove("is-copied");
      }, 1600);
    });
  });

  // Tabs ---------------------------------------------------------------------
  var tabCount = 0;

  function selectTab(tabs, index, focus) {
    tabs.buttons.forEach(function (button, i) {
      var selected = i === index;
      button.setAttribute("aria-selected", selected ? "true" : "false");
      button.tabIndex = selected ? 0 : -1;
      tabs.panels[i].hidden = !selected;
      if (selected && focus) button.focus();
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-tabs]"), function (root) {
    var id = "dw-tabs-" + ++tabCount;
    var tabs = {
      buttons: Array.prototype.slice.call(root.querySelectorAll('[role="tab"]')),
      panels: Array.prototype.slice.call(root.querySelectorAll('[role="tabpanel"]')),
    };
    tabs.buttons.forEach(function (button, i) {
      button.id = id + "-tab-" + i;
      tabs.panels[i].id = id + "-panel-" + i;
      button.setAttribute("aria-controls", tabs.panels[i].id);
      tabs.panels[i].setAttribute("aria-labelledby", button.id);
      button.addEventListener("click", function () { selectTab(tabs, i, false); });
      button.addEventListener("keydown", function (event) {
        var last = tabs.buttons.length - 1;
        var next = { ArrowRight: i === last ? 0 : i + 1, ArrowLeft: i === 0 ? last : i - 1, Home: 0, End: last }[event.key];
        if (next === undefined) return;
        event.preventDefault();
        selectTab(tabs, next, true);
      });
    });
  });

  // Mermaid diagrams ---------------------------------------------------------
  if (document.querySelector("pre.mermaid")) {
    import(CDN + "mermaid@12.0.0/dist/mermaid.esm.min.mjs").then(function (module) {
      var mermaid = module.default;
      mermaid.initialize({ startOnLoad: false, theme: "neutral", fontFamily: "Arimo, sans-serif" });
      mermaid.run({ querySelector: "pre.mermaid" });
    });
  }

  // KaTeX equations ----------------------------------------------------------
  var equations = document.querySelectorAll("[data-tex]");
  if (equations.length) {
    var css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = CDN + "katex@0.18.9/dist/katex.min.css";
    document.head.appendChild(css);
    var script = document.createElement("script");
    script.src = CDN + "katex@0.18.9/dist/katex.min.js";
    script.onload = function () {
      Array.prototype.forEach.call(equations, function (el) {
        window.katex.render(el.textContent.trim(), el, { displayMode: true, throwOnError: false });
      });
    };
    document.head.appendChild(script);
  }

  // Table of contents: mark the section currently being read -----------------
  var tocLinks = document.querySelectorAll(".dw-toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    Array.prototype.forEach.call(tocLinks, function (link) {
      byId[decodeURIComponent(link.hash.slice(1))] = link;
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          Array.prototype.forEach.call(tocLinks, function (link) { link.removeAttribute("aria-current"); });
          var active = byId[entry.target.id];
          if (active) active.setAttribute("aria-current", "true");
        });
      },
      { rootMargin: "-80px 0px -70% 0px" }
    );
    Object.keys(byId).forEach(function (id) {
      var heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    });
  }
})();
