/* ==========================================================================
   Doriax Engine — Documentation Theme Scripts
   ========================================================================== */
(function () {
  'use strict';

  const BASE = (window.DORIAX_BASE_URL || '').replace(/\/$/, '');

  document.addEventListener('DOMContentLoaded', function () {
    initSidebar();
    initNavSections();
    initCopyButtons();
    initScrollSpy();
    initSearch();
    initVersions();
  });

  /* ---------------------------------------------------------------- Sidebar */
  function initSidebar() {
    const toggle = document.getElementById('dx-sidebar-toggle');
    const sidebar = document.getElementById('dx-sidebar');
    const scrim = document.getElementById('dx-sidebar-scrim');
    if (!toggle || !sidebar) return;

    function close() {
      sidebar.classList.remove('is-open');
      scrim && scrim.classList.remove('is-open');
      toggle.classList.remove('is-active');
      toggle.setAttribute('aria-expanded', 'false');
    }
    function open() {
      sidebar.classList.add('is-open');
      scrim && scrim.classList.add('is-open');
      toggle.classList.add('is-active');
      toggle.setAttribute('aria-expanded', 'true');
    }

    toggle.addEventListener('click', function () {
      sidebar.classList.contains('is-open') ? close() : open();
    });
    scrim && scrim.addEventListener('click', close);
    sidebar.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        if (window.innerWidth <= 900) close();
      });
    });
  }

  /* ----------------------------------------------------- Collapsible nav */
  function initNavSections() {
    document.querySelectorAll('.dx-nav-section-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const section = btn.closest('.dx-nav-section');
        const expanded = section.classList.toggle('is-expanded');
        btn.setAttribute('aria-expanded', String(expanded));
      });
    });

    // Ensure the active link's section is visible.
    const active = document.querySelector('.dx-nav-link.is-active');
    if (active) {
      let el = active.closest('.dx-nav-section');
      while (el) {
        el.classList.add('is-expanded');
        const t = el.querySelector(':scope > .dx-nav-section-toggle');
        t && t.setAttribute('aria-expanded', 'true');
        el = el.parentElement.closest('.dx-nav-section');
      }
      active.scrollIntoView({ block: 'center' });
    }
  }

  /* -------------------------------------------------- Code copy buttons */
  function initCopyButtons() {
    document.querySelectorAll('.md-typeset pre > code').forEach(function (code) {
      const pre = code.parentElement;
      if (pre.querySelector('.dx-copy-btn')) return;
      const btn = document.createElement('button');
      btn.className = 'dx-copy-btn';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Copy code');
      btn.innerHTML = copyIcon();
      btn.addEventListener('click', function () {
        navigator.clipboard.writeText(code.innerText).then(function () {
          btn.classList.add('is-copied');
          btn.innerHTML = checkIcon();
          setTimeout(function () {
            btn.classList.remove('is-copied');
            btn.innerHTML = copyIcon();
          }, 1600);
        });
      });
      pre.appendChild(btn);
    });
  }

  function copyIcon() {
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  }
  function checkIcon() {
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  }

  /* ------------------------------------------------------ TOC scrollspy */
  function initScrollSpy() {
    const links = Array.prototype.slice.call(document.querySelectorAll('.dx-toc-link'));
    if (!links.length) return;
    const map = {};
    const targets = [];
    links.forEach(function (link) {
      const id = decodeURIComponent((link.getAttribute('href') || '').replace('#', ''));
      const el = id && document.getElementById(id);
      if (el) { map[id] = link; targets.push(el); }
    });
    if (!targets.length) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          const link = map[entry.target.id];
          link && link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });

    targets.forEach(function (t) { observer.observe(t); });
  }

  /* ----------------------------------------------------------- Search */
  function initSearch() {
    const trigger = document.getElementById('dx-search-trigger');
    const overlay = document.getElementById('dx-search-overlay');
    const input = document.getElementById('dx-search-input');
    const results = document.getElementById('dx-search-results');
    const empty = document.getElementById('dx-search-empty');
    if (!overlay || !input || !results) return;

    let index = null;
    let loading = false;
    let selected = -1;
    let previousFocus = null;

    function loadIndex() {
      if (index || loading) return;
      loading = true;
      fetch(BASE + '/search/search_index.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          index = (data && data.docs) || [];
          // Re-run search if the user already typed before the index was ready
          var pending = input.value.trim();
          if (pending) runSearch(pending);
        })
        .catch(function () { index = []; });
    }

    function openSearch() {
      loadIndex();
      previousFocus = document.activeElement;
      overlay.hidden = false;
      document.body.style.overflow = 'hidden';
      setTimeout(function () { input.focus(); }, 30);
    }
    function closeSearch() {
      overlay.hidden = true;
      document.body.style.overflow = '';
      input.value = '';
      results.innerHTML = '';
      empty.hidden = true;
      selected = -1;
      if (previousFocus) { previousFocus.focus(); previousFocus = null; }
    }

    trigger && trigger.addEventListener('click', openSearch);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSearch();
    });
    // Focus trap: keep Tab cycling inside the modal
    overlay.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || overlay.hidden) return;
      var focusable = Array.prototype.slice.call(
        overlay.querySelectorAll('a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])')
      );
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey) {
        if (document.activeElement === first) { e.preventDefault(); last.focus(); }
      } else {
        if (document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && overlay.hidden && !isTyping(e.target)) {
        e.preventDefault();
        openSearch();
      } else if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        overlay.hidden ? openSearch() : closeSearch();
      } else if (e.key === 'Escape' && !overlay.hidden) {
        closeSearch();
      }
    });

    input.addEventListener('input', function () {
      runSearch(input.value.trim());
    });

    input.addEventListener('keydown', function (e) {
      const items = results.querySelectorAll('.dx-search-result');
      if (!items.length) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selected = (selected + 1) % items.length;
        updateSelection(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selected = (selected - 1 + items.length) % items.length;
        updateSelection(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const target = selected >= 0 ? items[selected] : items[0];
        const link = target && target.querySelector('a');
        if (link) window.location.href = link.href;
      }
    });

    function updateSelection(items) {
      items.forEach(function (it, i) {
        it.classList.toggle('is-selected', i === selected);
        if (i === selected) it.scrollIntoView({ block: 'nearest' });
      });
    }

    function runSearch(query) {
      selected = -1;
      if (!query || query.length < 2) {
        results.innerHTML = '';
        empty.hidden = true;
        return;
      }
      if (!index) {
        results.innerHTML = '';
        return;
      }
      const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
      const scored = [];
      index.forEach(function (doc) {
        if (!doc.title || !doc.location) return;
        const title = cleanText(doc.title).toLowerCase();
        const text = cleanText(doc.text || '').toLowerCase();
        let score = 0;
        terms.forEach(function (t) {
          if (title.indexOf(t) !== -1) score += 10;
          const ti = text.indexOf(t);
          if (ti !== -1) score += 3;
        });
        // require all terms to appear somewhere
        const allPresent = terms.every(function (t) {
          return title.indexOf(t) !== -1 || text.indexOf(t) !== -1;
        });
        if (score > 0 && allPresent) scored.push({ doc: doc, score: score });
      });
      scored.sort(function (a, b) { return b.score - a.score; });
      render(scored.slice(0, 12), terms);
    }

    function render(items, terms) {
      if (!items.length) {
        results.innerHTML = '';
        empty.hidden = false;
        return;
      }
      empty.hidden = true;
      results.innerHTML = items.map(function (it) {
        const doc = it.doc;
        const url = BASE + '/' + doc.location;
        const section = topSection(doc.location);
        const title = cleanText(doc.title);
        const rawText = cleanText(doc.text || '');
        const snippet = makeSnippet(rawText, terms);
        return '<li class="dx-search-result">' +
          '<a href="' + escapeAttr(url) + '">' +
          (section ? '<div class="dx-search-result-section">' + escapeHtml(section) + '</div>' : '') +
          '<div class="dx-search-result-title">' + highlight(title, terms) + '</div>' +
          (snippet ? '<div class="dx-search-result-text">' + snippet + '</div>' : '') +
          '</a></li>';
      }).join('');
    }

    function makeSnippet(text, terms) {
      if (!text) return '';
      const lower = text.toLowerCase();
      let pos = -1;
      for (let i = 0; i < terms.length; i++) {
        const p = lower.indexOf(terms[i]);
        if (p !== -1) { pos = p; break; }
      }
      let start = pos > 60 ? pos - 60 : 0;
      let slice = text.substring(start, start + 160);
      if (start > 0) slice = '… ' + slice;
      return highlight(slice, terms);
    }

    function topSection(location) {
      const parts = location.split('/');
      if (parts.length > 1 && parts[0]) {
        return parts[0].replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
      }
      return '';
    }

    function highlight(str, terms) {
      let out = escapeHtml(str);
      terms.forEach(function (t) {
        if (!t) return;
        const re = new RegExp('(' + escapeRegex(t) + ')', 'ig');
        out = out.replace(re, '<mark>$1</mark>');
      });
      return out;
    }
  }

  /* --------------------------------------------------------- helpers */
  /* --------------------------------------------------------------- Versions */
  function initVersions() {
    const wrap = document.getElementById('dx-version-select');
    const url = window.DORIAX_VERSIONS_URL;
    if (!wrap || !url) return;

    fetch(url, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !Array.isArray(data.versions) || !data.versions.length) return;
        const root = new URL('.', new URL(url, location.href)).href;
        buildVersionMenu(wrap, data, root);
        buildVersionBanner(data, root);
      })
      // No versions.json (a plain `mkdocs serve`, say) — leave the picker hidden.
      .catch(function () {});
  }

  function versionHref(root, id) {
    return root + id + '/' + (window.DORIAX_PAGE_URL || '');
  }

  function buildVersionMenu(wrap, data, root) {
    const trigger = document.getElementById('dx-version-trigger');
    const menu = document.getElementById('dx-version-menu');
    const current = document.getElementById('dx-version-current');
    if (!trigger || !menu) return;

    const active = data.versions.filter(function (v) { return v.id === window.DORIAX_VERSION; })[0];
    if (active && current) current.textContent = active.title;

    data.versions.forEach(function (v) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = versionHref(root, v.id);
      if (v.id === window.DORIAX_VERSION) {
        a.className = 'is-current';
        a.setAttribute('aria-current', 'true');
      }

      const label = document.createElement('span');
      label.className = 'dx-version-label';
      label.textContent = v.title;
      a.appendChild(label);

      if (v.note) {
        const note = document.createElement('span');
        note.className = 'dx-version-note';
        note.textContent = v.note;
        a.appendChild(note);
      }

      // The page may not exist in the target version — fall back to its home.
      a.addEventListener('click', function (ev) {
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
        ev.preventDefault();
        const target = a.href;
        fetch(target, { method: 'HEAD' })
          .then(function (r) { location.href = r.ok ? target : root + v.id + '/'; })
          .catch(function () { location.href = root + v.id + '/'; });
      });

      li.appendChild(a);
      menu.appendChild(li);
    });

    function close() {
      wrap.classList.remove('is-open');
      menu.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
    }
    function open() {
      wrap.classList.add('is-open');
      menu.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
    }

    trigger.addEventListener('click', function (ev) {
      ev.stopPropagation();
      menu.hidden ? open() : close();
    });
    document.addEventListener('click', function (ev) {
      if (!wrap.contains(ev.target)) close();
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') close();
    });

    wrap.hidden = false;
  }

  function buildVersionBanner(data, root) {
    const el = document.getElementById('dx-version-banner');
    if (!el) return;

    const current = window.DORIAX_VERSION;
    const latest = data.versions.filter(function (v) { return v.id === data.latest; })[0];
    if (!latest || current === data.latest) return;

    const link = document.createElement('a');
    link.href = versionHref(root, latest.id);
    const text = document.createElement('span');

    if (current === 'unstable') {
      text.textContent = 'You are reading the development documentation for the next release. ';
      link.textContent = 'Switch to the stable ' + latest.title + ' docs';
    } else {
      el.classList.add('is-outdated');
      text.textContent = 'You are reading the documentation for an older release. ';
      link.textContent = 'Switch to the latest version (' + latest.title + ')';
    }

    el.appendChild(text);
    el.appendChild(link);
    el.hidden = false;
  }

  function isTyping(el) {
    if (!el) return false;
    const tag = el.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || el.isContentEditable;
  }
  // Decode HTML entities stored in the MkDocs search index
  function decodeHtml(s) {
    const el = document.createElement('textarea');
    el.innerHTML = s;
    return el.value;
  }
  // Strip MkDocs heading permalink pilcrow characters
  function cleanText(s) {
    return decodeHtml(s).replace(/\s*¶\s*/g, ' ').trim();
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function escapeAttr(s) { return escapeHtml(s); }
  function escapeRegex(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
})();
