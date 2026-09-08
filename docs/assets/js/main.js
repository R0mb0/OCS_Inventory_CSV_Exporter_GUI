(function () {
  "use strict";

  // Update these once the repository is published / renamed.
  var GITHUB_REPO_URL = "https://github.com/R0mb0/OCS_Inventory_CSV_Exporter_GUI";
  var GITHUB_RELEASES_URL = GITHUB_REPO_URL + "/releases/latest";

  var THEME_KEY = "ocs-exporter-site-theme"; // "light" | "dark" | absent = follow system
  var LANG_KEY = "ocs-exporter-site-lang";

  /* ---------------- Theme ---------------- */

  function getStoredTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function storeTheme(value) {
    try {
      if (value) {
        localStorage.setItem(THEME_KEY, value);
      } else {
        localStorage.removeItem(THEME_KEY);
      }
    } catch (e) {
      /* ignore, e.g. private browsing */
    }
  }

  function systemPrefersDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function applyTheme(theme) {
    var root = document.documentElement;
    if (theme === "light" || theme === "dark") {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
    updateThemeButton();
  }

  function currentEffectiveTheme() {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    return systemPrefersDark() ? "dark" : "light";
  }

  function updateThemeButton() {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var effective = currentEffectiveTheme();
    btn.textContent = effective === "dark" ? "☀️" : "🌙";
  }

  function toggleTheme() {
    var effective = currentEffectiveTheme();
    var next = effective === "dark" ? "light" : "dark";
    storeTheme(next);
    applyTheme(next);
  }

  function initTheme() {
    var stored = getStoredTheme();
    applyTheme(stored);
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.addEventListener("click", toggleTheme);

    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () {
        if (!getStoredTheme()) {
          applyTheme(null);
        }
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }

  /* ---------------- i18n ---------------- */

  function detectBrowserLang() {
    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || DEFAULT_LANG];
    for (var i = 0; i < langs.length; i++) {
      var code = String(langs[i]).slice(0, 2).toLowerCase();
      if (SUPPORTED_LANGS.indexOf(code) !== -1) return code;
    }
    return DEFAULT_LANG;
  }

  function getStoredLang() {
    try {
      return localStorage.getItem(LANG_KEY);
    } catch (e) {
      return null;
    }
  }

  function storeLang(code) {
    try {
      localStorage.setItem(LANG_KEY, code);
    } catch (e) {
      /* ignore */
    }
  }

  function lookup(dict, path) {
    var parts = path.split(".");
    var node = dict;
    for (var i = 0; i < parts.length; i++) {
      if (node == null) return null;
      node = node[parts[i]];
    }
    return typeof node === "string" ? node : null;
  }

  function applyLang(code) {
    if (!TRANSLATIONS[code]) code = DEFAULT_LANG;
    var dict = TRANSLATIONS[code];

    document.documentElement.setAttribute("lang", code);

    var nodes = document.querySelectorAll("[data-i18n]");
    for (var i = 0; i < nodes.length; i++) {
      var key = nodes[i].getAttribute("data-i18n");
      var value = lookup(dict, key) || lookup(TRANSLATIONS[DEFAULT_LANG], key);
      if (value != null) nodes[i].textContent = value;
    }

    var attrNodes = document.querySelectorAll("[data-i18n-attr]");
    for (var j = 0; j < attrNodes.length; j++) {
      var spec = attrNodes[j].getAttribute("data-i18n-attr"); // format: "attr:key.path"
      var parts = spec.split(":");
      var attr = parts[0];
      var key2 = parts[1];
      var value2 = lookup(dict, key2) || lookup(TRANSLATIONS[DEFAULT_LANG], key2);
      if (value2 != null) attrNodes[j].setAttribute(attr, value2);
    }

    var titleValue = lookup(dict, "meta.title");
    if (titleValue) document.title = titleValue;
    var descValue = lookup(dict, "meta.description");
    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && descValue) metaDesc.setAttribute("content", descValue);

    var select = document.getElementById("lang-select");
    if (select) select.value = code;
  }

  function setLang(code) {
    storeLang(code);
    applyLang(code);
  }

  function initLang() {
    var stored = getStoredLang();
    var initial = stored && SUPPORTED_LANGS.indexOf(stored) !== -1 ? stored : detectBrowserLang();
    applyLang(initial);

    var select = document.getElementById("lang-select");
    if (select) {
      select.addEventListener("change", function () {
        setLang(select.value);
      });
    }
  }

  /* ---------------- Links ---------------- */

  function initLinks() {
    var githubLinks = document.querySelectorAll("[data-github-link]");
    for (var i = 0; i < githubLinks.length; i++) githubLinks[i].setAttribute("href", GITHUB_REPO_URL);

    var releaseLinks = document.querySelectorAll("[data-release-link]");
    for (var j = 0; j < releaseLinks.length; j++) releaseLinks[j].setAttribute("href", GITHUB_RELEASES_URL);

    var yearEl = document.getElementById("current-year");
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initLang();
    initLinks();
  });
})();
