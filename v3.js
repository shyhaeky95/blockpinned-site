// BlockPinned design-v3 WOW pass — progressive enhancement only.
// Every number and every conclusion remains readable with JavaScript disabled.
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Theme state is explicit for assistive technology and survives reloads.
  var themeButton = document.getElementById("nut-nen");
  function isDark() {
    var chosen = root.getAttribute("data-theme");
    return chosen === "toi" || (!chosen && matchMedia("(prefers-color-scheme: dark)").matches);
  }
  function syncThemeButton() {
    if (!themeButton) return;
    var dark = isDark();
    themeButton.setAttribute("aria-pressed", String(dark));
    themeButton.setAttribute("aria-label", dark ? "Chuyển sang nền sáng" : "Chuyển sang nền tối");
  }
  if (themeButton) {
    syncThemeButton();
    themeButton.addEventListener("click", function () {
      var next = isDark() ? "sang" : "toi";
      root.setAttribute("data-theme", next);
      localStorage.setItem("bp-nen", next);
      syncThemeButton();
    });
  }

  // Global Quick Find: one compact map of every public surface. Resolve every
  // destination from the logo's home link: it already knows whether this page is
  // production, `/thu-v3/`, or a local file preview. The design mockup filenames
  // must never escape into the published navigation.
  var quickHome = document.querySelector("a.ten");
  var quickRoot = quickHome ? quickHome.href : new URL(".", location.href).href;
  function quickHref(path) { return new URL(path, quickRoot).href; }
  var quickRoutes = [
    { href: quickHref(""), code: "00", kind: "Bắt đầu", title: "Trang\u00a0chủ", copy: "Bản đồ nội dung và tài sản công khai của BlockPinned", tags: "home so goc bản đồ trang chủ", tone: "home" },
    { href: quickHref("bai/"), code: "01", kind: "Điều\u00a0tra", title: "Tất cả bài\u00a0viết", copy: "Tìm, lọc token và mở toàn bộ bài\u00a0điều\u00a0tra", tags: "article bai viet dieu tra kho tìm kiếm kết luận bằng chứng", tone: "article" },
    { href: quickHref("token/"), code: "02", kind: "Token", title: "Token Directory", copy: "Bản đồ độ phủ và lối vào từng hồ\u00a0sơ", tags: "token directory coverage logo", tone: "token" },
    { href: quickHref("token/uni/"), code: "UNI", kind: "Hồ\u00a0sơ", title: "Uniswap · UNI", copy: "Claim ledger, trạng thái và lịch sử hiệu chỉnh", tags: "uniswap uni claim hồ sơ", tone: "uni" },
    { href: quickHref("facts/"), code: "03", kind: "Tự\u00a0kiểm", title: "Facts", copy: "Con số, block và lệnh để đọc lại", tags: "facts con số block lệnh proof", tone: "facts" },
    { href: quickHref("track-record/"), code: "04", kind: "Sổ công khai", title: "Track record", copy: "Những gì được ghi\u00a0trước đặt cạnh kết quả đến sau", tags: "track record ghi trước kết quả", tone: "track" },
    { href: quickHref("du-lieu/"), code: "05", kind: "Hiện vật", title: "Dữ liệu thô", copy: "JSON, SHA-256 và lệnh tải để tự đếm lại", tags: "du lieu data json hash sha curl hien vat", tone: "data" }
  ];
  var quickHost = themeButton && themeButton.parentNode;
  if (quickHost) {
    var quickButton = document.createElement("button");
    quickButton.type = "button";
    quickButton.className = "quick-find-trigger";
    quickButton.setAttribute("aria-haspopup", "dialog");
    quickButton.setAttribute("aria-controls", "quick-find");
    quickButton.innerHTML = '<span aria-hidden="true">⌕</span><b>Tìm nhanh</b><kbd>⌘K</kbd>';
    quickHost.insertBefore(quickButton, themeButton);

    var quickDialog = document.createElement("dialog");
    quickDialog.id = "quick-find";
    quickDialog.className = "quick-find";
    quickDialog.setAttribute("aria-labelledby", "quick-find-title");
    quickDialog.innerHTML = '<div class="quick-find-shell">'
      + '<header class="quick-find-head"><span class="quick-find-mark" aria-hidden="true">BP</span>'
      + '<label><span id="quick-find-title">Tìm trong BlockPinned</span><input type="search" data-quick-input placeholder="Gõ tên khu, token hoặc cách kiểm…" autocomplete="off" spellcheck="false" aria-controls="quick-find-results"></label>'
      + '<button type="button" data-quick-close aria-label="Đóng tìm nhanh">ESC</button></header>'
      + '<div class="quick-find-meta"><span>PUBLIC RESEARCH MAP</span><b data-quick-count>07 đích</b></div>'
      + '<div class="quick-find-results" id="quick-find-results" role="listbox" aria-label="Kết quả tìm nhanh"></div>'
      + '<footer class="quick-find-foot"><span><kbd>↑</kbd><kbd>↓</kbd> chọn</span><span><kbd>↵</kbd> mở</span><span><kbd>esc</kbd> đóng</span><i>Không rời bàn phím</i></footer>'
      + '</div>';
    document.body.appendChild(quickDialog);

    var quickInput = quickDialog.querySelector("[data-quick-input]");
    var quickResults = quickDialog.querySelector(".quick-find-results");
    var quickCount = quickDialog.querySelector("[data-quick-count]");
    var quickSelected = 0;
    var quickVisible = [];

    function quickNormalise(value) {
      return (value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    }
    function quickRouteKey(value) {
      try {
        return new URL(value, location.href).href.replace(/index\.html(?:[?#].*)?$/, "").replace(/[?#].*$/, "").replace(/\/$/, "");
      } catch (ignore) { return value; }
    }
    function currentQuickPage() {
      return quickRouteKey(location.href);
    }
    function paintQuickSelection() {
      var links = quickResults.querySelectorAll("[data-quick-result]");
      links.forEach(function (link, index) {
        var active = index === quickSelected;
        link.classList.toggle("is-selected", active);
        link.setAttribute("aria-selected", String(active));
        if (active) quickInput.setAttribute("aria-activedescendant", link.id);
      });
      if (links[quickSelected]) links[quickSelected].scrollIntoView({ block: "nearest" });
    }
    function renderQuickFind() {
      var query = quickNormalise(quickInput.value);
      var current = currentQuickPage();
      quickVisible = quickRoutes.filter(function (route) {
        return !query || quickNormalise(route.kind + " " + route.title + " " + route.copy + " " + route.tags).indexOf(query) !== -1;
      });
      quickSelected = Math.min(quickSelected, Math.max(0, quickVisible.length - 1));
      quickResults.innerHTML = quickVisible.length ? quickVisible.map(function (route, index) {
        var here = quickRouteKey(route.href) === current;
        return '<a id="quick-result-' + index + '" class="quick-find-result" data-quick-result data-tone="' + route.tone + '" href="' + route.href + '" role="option" aria-selected="false">'
          + '<span class="quick-find-code" aria-hidden="true">' + route.code + '</span>'
          + '<span class="quick-find-copy"><small>' + route.kind + '</small><b>' + route.title + '</b><em>' + route.copy + '</em></span>'
          + (here ? '<span class="quick-find-here">Đang xem</span>' : '<span class="quick-find-go" aria-hidden="true">↗</span>')
          + '</a>';
      }).join("") : '<p class="quick-find-empty"><b>Không có đích phù hợp.</b><span>Thử “token”, “fact”, “tự\u00a0kiểm” hoặc “track”.</span></p>';
      quickCount.textContent = (quickVisible.length < 10 ? "0" : "") + quickVisible.length + "\u00a0đích";
      paintQuickSelection();
    }
    function openQuickFind() {
      if (quickDialog.open) return;
      quickInput.value = "";
      quickSelected = 0;
      renderQuickFind();
      quickDialog.showModal();
      document.body.classList.add("quick-find-open");
      requestAnimationFrame(function () { quickInput.focus(); });
    }
    function closeQuickFind() {
      if (quickDialog.open) quickDialog.close();
    }
    quickButton.addEventListener("click", openQuickFind);
    quickDialog.querySelector("[data-quick-close]").addEventListener("click", closeQuickFind);
    quickDialog.addEventListener("close", function () {
      document.body.classList.remove("quick-find-open");
      quickButton.focus();
    });
    quickDialog.addEventListener("click", function (event) {
      if (event.target === quickDialog) closeQuickFind();
    });
    quickInput.addEventListener("input", function () { quickSelected = 0; renderQuickFind(); });
    quickInput.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        if (!quickVisible.length) return;
        quickSelected = (quickSelected + (event.key === "ArrowDown" ? 1 : -1) + quickVisible.length) % quickVisible.length;
        paintQuickSelection();
      } else if (event.key === "Enter" && quickVisible.length) {
        event.preventDefault();
        quickResults.querySelectorAll("[data-quick-result]")[quickSelected].click();
      }
    });
    quickResults.addEventListener("mousemove", function (event) {
      var result = event.target.closest("[data-quick-result]");
      if (!result) return;
      var links = Array.prototype.slice.call(quickResults.querySelectorAll("[data-quick-result]"));
      var nextSelected = links.indexOf(result);
      if (nextSelected === quickSelected) return;
      quickSelected = nextSelected;
      paintQuickSelection();
    });
    document.addEventListener("keydown", function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        if (quickDialog.open) closeQuickFind(); else openQuickFind();
      }
    });
    if (!/Mac|iPhone|iPad/.test(navigator.platform || "")) quickButton.querySelector("kbd").textContent = "Ctrl K";
  }

  // Mobile navigation keeps every destination reachable.
  var menuButton = document.querySelector(".nut-menu");
  var menu = document.getElementById("site-nav");
  function closeMenu() {
    if (!menuButton || !menu) return;
    menu.classList.remove("mo");
    menuButton.setAttribute("aria-expanded", "false");
  }
  if (menuButton && menu) {
    menuButton.addEventListener("click", function () {
      var open = menuButton.getAttribute("aria-expanded") === "true";
      menu.classList.toggle("mo", !open);
      menuButton.setAttribute("aria-expanded", String(!open));
    });
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("click", function (event) {
      if (!menu.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { closeMenu(); menuButton.focus(); }
    });
  }

  // Progress is a quiet orientation cue on long research pages.
  var progress = document.getElementById("bp-tien");
  if (progress) {
    var progressTick = false;
    function drawProgress() {
      var page = document.documentElement;
      var value = page.scrollTop / Math.max(1, page.scrollHeight - page.clientHeight);
      progress.style.transform = "scaleX(" + Math.min(1, Math.max(0, value)) + ")";
      progressTick = false;
    }
    addEventListener("scroll", function () {
      if (progressTick) return;
      progressTick = true;
      requestAnimationFrame(drawProgress);
    }, { passive: true });
    drawProgress();
  }

  // Reveal only major story beats. Reduced-motion users see everything immediately.
  var revealItems = document.querySelectorAll(".finding-home,.article-verdict,.may-hero,.token-overview,.token-card,.numrow,.chart-card,.cred,.ho-so,.evidence,.than>h2,.than>figure,.ba-so,.fact-protocol,.facts-ledger-head,.fact-wow,.track-score,.track-ledger-head,.track-entry,.uni-vault,.uni-coverage,.uni-ledger-head,.uni-claim,.uni-articles,.home-articles,.article-archive-head,.article-archive-card,.data-protocol,.data-ledger-head,.data-file,.data-note");
  if (!reduce && "IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    }, { threshold: 0, rootMargin: "0px 0px -5%" });
    revealItems.forEach(function (item, index) {
      item.classList.add("reveal-ready");
      item.style.transitionDelay = Math.min(index % 4, 2) * 45 + "ms";
      revealObserver.observe(item);
    });
    // A reveal is decoration, never a visibility gate. Large blocks can be taller
    // than the viewport and headless/static captures may not deliver observer events.
    // The fallback makes every story beat visible even when that happens.
    setTimeout(function () {
      revealItems.forEach(function (item) { item.classList.add("is-visible"); });
    }, 1400);
  }

  // A very soft local glow makes the primary data surface feel alive.
  document.querySelectorAll("[data-spotlight]").forEach(function (surface) {
    surface.addEventListener("pointermove", function (event) {
      if (event.pointerType && event.pointerType !== "mouse") return;
      var box = surface.getBoundingClientRect();
      surface.style.setProperty("--mx", (event.clientX - box.left) + "px");
      surface.style.setProperty("--my", (event.clientY - box.top) + "px");
    });
  });

  // Exactly one cursor scan on the homepage. It eases toward the pointer and
  // stops requesting frames as soon as it settles — no autonomous sweep.
  if (!reduce && matchMedia("(pointer: fine)").matches) {
    document.querySelectorAll("[data-cursor-scan]").forEach(function (surface) {
      var beam = surface.querySelector(".cursor-scan");
      if (!beam) return;
      var x = 0, y = 0, targetX = 0, targetY = 0, frame = 0, entered = false;
      function paint() {
        x += (targetX - x) * .115;
        y += (targetY - y) * .115;
        beam.style.transform = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0) rotate(7deg)";
        if (Math.abs(targetX - x) > .08 || Math.abs(targetY - y) > .08) {
          frame = requestAnimationFrame(paint);
        } else {
          x = targetX; y = targetY; frame = 0;
          beam.style.transform = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0) rotate(7deg)";
        }
      }
      function aim(event) {
        var box = surface.getBoundingClientRect();
        targetX = event.clientX - box.left;
        targetY = event.clientY - box.top;
        if (!entered) { x = targetX - 32; y = targetY; entered = true; }
        if (!frame) frame = requestAnimationFrame(paint);
      }
      surface.addEventListener("pointerenter", function (event) {
        surface.classList.add("scan-active");
        aim(event);
      });
      surface.addEventListener("pointermove", aim);
      surface.addEventListener("pointerleave", function () {
        surface.classList.remove("scan-active"); entered = false;
        if (frame) cancelAnimationFrame(frame); frame = 0;
      });
    });
  }

  var tip = document.getElementById("ch-tip");
  if (tip) {
    tip.setAttribute("role", "tooltip");
    tip.setAttribute("aria-live", "polite");
  }

  function placeTip(text, x, y, html) {
    if (!tip) return;
    if (html) tip.innerHTML = text; else tip.textContent = text;
    tip.style.whiteSpace = html ? "nowrap" : "normal";
    tip.style.maxWidth = html ? "none" : "min(320px, calc(100vw - 24px))";
    tip.classList.add("hien");
    var left = Math.min(x + 14, innerWidth - tip.offsetWidth - 10);
    var top = Math.min(y + 16, innerHeight - tip.offsetHeight - 10);
    tip.style.transform = "translate(" + Math.max(8, left) + "px," + Math.max(8, top) + "px)";
  }
  function hideTip() { if (tip) tip.classList.remove("hien"); }

  // Generic explanations work with mouse, keyboard and tap.
  document.querySelectorAll("[data-tip]").forEach(function (target) {
    if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "0");
    function showFromTarget() {
      var box = target.getBoundingClientRect();
      placeTip(target.getAttribute("data-tip"), box.left + box.width / 2, box.bottom, false);
    }
    target.addEventListener("mouseenter", showFromTarget);
    target.addEventListener("focus", showFromTarget);
    target.addEventListener("click", showFromTarget);
    target.addEventListener("mouseleave", hideTip);
    target.addEventListener("blur", hideTip);
  });

  // Hero chart: pointer, keyboard and two mobile jump points share one state.
  var data = window.BP_CHART_DATA;
  var svg = document.querySelector(".chart svg");
  var scroller = document.querySelector(".chart-cuon");
  if (svg && scroller && Array.isArray(data) && data.length) {
    var line = svg.querySelector("#soi");
    var point = svg.querySelector("#soidiem");
    var selected = data.length - 1;
    svg.setAttribute("tabindex", "0");
    svg.setAttribute("aria-describedby", "ch-tip");

    function money(value) {
      return "$" + String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }
    function pointOnScreen(row) {
      var matrix = svg.getScreenCTM();
      if (!matrix) return { x: innerWidth / 2, y: innerHeight / 2 };
      var p = svg.createSVGPoint(); p.x = row[2]; p.y = row[3];
      var out = p.matrixTransform(matrix);
      return { x: out.x, y: out.y };
    }
    function showPoint(index, screenX, screenY) {
      selected = Math.min(data.length - 1, Math.max(0, index));
      var row = data[selected];
      if (line) {
        line.setAttribute("x1", row[2]); line.setAttribute("x2", row[2]); line.style.opacity = ".55";
      }
      if (point) {
        point.setAttribute("cx", row[2]); point.setAttribute("cy", row[3]); point.style.opacity = "1";
      }
      var onScreen = pointOnScreen(row);
      var delta = selected ? row[1] - data[selected - 1][1] : 0;
      var pct = selected && data[selected - 1][1] ? delta / data[selected - 1][1] * 100 : 0;
      var deltaText = selected ? '<span class="delta ' + (delta >= 0 ? 'up' : 'down') + '">' +
        (delta >= 0 ? '▲ +' : '▼ −') + Math.abs(pct).toFixed(1).replace('.', ',') + '% so với ngày trước</span>' : '';
      placeTip('<span class="ngay">' + row[0] + '/2026</span>' + money(row[1]) + deltaText,
        screenX == null ? onScreen.x : screenX, screenY == null ? onScreen.y : screenY, true);
    }
    function nearest(clientX) {
      var matrix = svg.getScreenCTM();
      if (!matrix) return selected;
      var p = svg.createSVGPoint(); p.x = clientX; p.y = 0;
      var local = p.matrixTransform(matrix.inverse());
      var best = 0, distance = Infinity;
      data.forEach(function (row, index) {
        var next = Math.abs(row[2] - local.x);
        if (next < distance) { distance = next; best = index; }
      });
      return best;
    }
    function clearPoint() {
      if (line) line.style.opacity = "0";
      if (point) point.style.opacity = "0";
      hideTip();
    }
    svg.addEventListener("pointermove", function (event) {
      if (event.pointerType && event.pointerType !== "mouse") return;
      showPoint(nearest(event.clientX), event.clientX, event.clientY);
    });
    svg.addEventListener("click", function (event) {
      showPoint(nearest(event.clientX), event.clientX, event.clientY);
    });
    svg.addEventListener("mouseleave", function () {
      if (document.activeElement !== svg) clearPoint();
    });
    svg.addEventListener("focus", function () { showPoint(selected); });
    svg.addEventListener("blur", clearPoint);
    svg.addEventListener("keydown", function (event) {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight" && event.key !== "Home" && event.key !== "End") return;
      event.preventDefault();
      if (event.key === "ArrowLeft") selected--;
      if (event.key === "ArrowRight") selected++;
      if (event.key === "Home") selected = 0;
      if (event.key === "End") selected = data.length - 1;
      showPoint(selected);
    });

    function jumpTo(index, button) {
      selected = index;
      var contentX = data[index][2] / 1000 * svg.scrollWidth;
      scroller.scrollTo({ left: Math.max(0, contentX - scroller.clientWidth / 2), behavior: reduce ? "auto" : "smooth" });
      document.querySelectorAll("[data-chart-jump]").forEach(function (item) { item.classList.toggle("tai", item === button); });
      setTimeout(function () { showPoint(index); }, reduce ? 0 : 280);
    }
    document.querySelectorAll("[data-chart-jump]").forEach(function (button) {
      button.addEventListener("click", function () {
        jumpTo(button.dataset.chartJump === "pin" ? 15 : data.length - 1, button);
      });
    });
    if (matchMedia("(max-width: 640px)").matches) {
      requestAnimationFrame(function () { scroller.scrollLeft = scroller.scrollWidth - scroller.clientWidth; });
    }
  }

  // Hero ghost follows the reader by a few pixels: depth without moving content.
  if (!reduce) {
    document.querySelectorAll(".hero").forEach(function (hero) {
      var ghost = hero.querySelector(".ghost-num");
      if (!ghost) return;
      hero.addEventListener("pointermove", function (event) {
        if (event.pointerType && event.pointerType !== "mouse") return;
        var box = hero.getBoundingClientRect();
        var x = (event.clientX - box.left) / box.width - .5;
        var y = (event.clientY - box.top) / box.height - .5;
        ghost.style.transform = "translate(" + (x * 13).toFixed(1) + "px," + (y * 9).toFixed(1) + "px)";
      });
      hero.addEventListener("pointerleave", function () { ghost.style.transform = ""; });
    });
  }

  // Primer console: preview a layer on hover/focus, lock it on click.
  // The interaction only changes emphasis; every number remains visible in HTML.
  document.querySelectorAll("[data-system-console]").forEach(function (consoleBox) {
    var tabs = consoleBox.querySelectorAll("[data-system-tab]");
    var locked = "";
    function focusLayer(layer) {
      if (layer) consoleBox.setAttribute("data-system-focus", layer);
      else consoleBox.removeAttribute("data-system-focus");
      tabs.forEach(function (tab) {
        tab.setAttribute("aria-pressed", String(tab.dataset.systemTab === locked));
      });
    }
    tabs.forEach(function (tab) {
      tab.addEventListener("pointerenter", function () { if (!locked) focusLayer(tab.dataset.systemTab); });
      tab.addEventListener("pointerleave", function () { if (!locked) focusLayer(""); });
      tab.addEventListener("focus", function () { if (!locked) focusLayer(tab.dataset.systemTab); });
      tab.addEventListener("blur", function () { if (!locked) focusLayer(""); });
      tab.addEventListener("click", function () {
        locked = locked === tab.dataset.systemTab ? "" : tab.dataset.systemTab;
        focusLayer(locked);
      });
    });
  });

  // Token directory: filtering changes only the view, never the underlying data.
  var tokenFilterButtons = document.querySelectorAll("[data-token-filter]");
  var tokenTagButtons = document.querySelectorAll("[data-token-tag]");
  var tokenCards = document.querySelectorAll("[data-token-card]");
  var tokenFilterStatus = document.querySelector(".token-filter-status");
  var tokenDirectory = document.querySelector(".token-directory");
  if (tokenFilterButtons.length && tokenCards.length) {
    function renderTokenCards(test, label) {
      var shown = 0;
      tokenCards.forEach(function (card) {
        var visible = test(card);
        card.hidden = !visible;
        if (visible) shown++;
      });
      if (tokenFilterStatus) tokenFilterStatus.textContent = "Đang hiện " + shown + "\u00a0token" + (label ? " · " + label : "");
    }
    tokenFilterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var filter = button.dataset.tokenFilter;
        tokenFilterButtons.forEach(function (item) {
          item.setAttribute("aria-pressed", String(item === button));
        });
        tokenTagButtons.forEach(function (item) {
          item.setAttribute("aria-pressed", String(filter === "all" && item.dataset.tokenTag === "all"));
        });
        renderTokenCards(function (card) { return filter === "all" || card.dataset.profile === filter; }, "");
      });
    });
    tokenTagButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var tag = button.dataset.tokenTag;
        tokenTagButtons.forEach(function (item) {
          item.setAttribute("aria-pressed", String(item === button));
        });
        tokenFilterButtons.forEach(function (item) {
          item.setAttribute("aria-pressed", String(tag === "all" && item.dataset.tokenFilter === "all"));
        });
        renderTokenCards(function (card) { return tag === "all" || card.dataset.token === tag; }, tag === "all" ? "" : tag.toUpperCase());
        if (tokenDirectory) requestAnimationFrame(function () {
          tokenDirectory.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
        });
      });
    });
  }

  // Primer map follows the section currently in view.
  var mapLinks = document.querySelectorAll(".primer-map a[href^='#']");
  if (mapLinks.length && "IntersectionObserver" in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        mapLinks.forEach(function (link) {
          link.classList.toggle("tai", link.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-35% 0px -55%", threshold: 0 });
    mapLinks.forEach(function (link) {
      var section = document.querySelector(link.getAttribute("href"));
      if (section) sectionObserver.observe(section);
    });
  }

  // Facts: the sticky ledger index follows the proof currently being read.
  var factLinks = document.querySelectorAll("[data-fact-link]");
  var factCards = document.querySelectorAll("[data-fact]");
  if (factLinks.length && factCards.length) {
    function selectFact(id) {
      factLinks.forEach(function (link) {
        var selected = link.getAttribute("href") === "#" + id;
        link.classList.toggle("tai", selected);
        if (selected) link.setAttribute("aria-current", "true");
        else link.removeAttribute("aria-current");
      });
    }
    if ("IntersectionObserver" in window) {
      var factObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) selectFact(entry.target.id);
        });
      }, { rootMargin: "-24% 0px -62%", threshold: 0 });
      factCards.forEach(function (card) { factObserver.observe(card); });
    }
    var firstFact = location.hash ? document.querySelector(location.hash) : factCards[0];
    if (firstFact && firstFact.matches("[data-fact]")) selectFact(firstFact.id);
  }

  // One clipboard path serves commands and exact evidence anchors.
  function fallbackCopyText(value) {
    var field = document.createElement("textarea");
    field.value = value;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.appendChild(field);
    field.select();
    var copied = document.execCommand("copy");
    field.remove();
    return copied;
  }
  function copyPlainText(value) {
    return navigator.clipboard && navigator.clipboard.writeText
      ? navigator.clipboard.writeText(value).then(function () { return true; })
        .catch(function () { return fallbackCopyText(value); })
      : Promise.resolve(fallbackCopyText(value));
  }
  function evidenceLink(id) {
    var canonical = document.querySelector('link[rel="canonical"]');
    var base = canonical ? canonical.href : location.href;
    return base.replace(/#.*$/, "") + "#" + encodeURIComponent(id);
  }
  function copyEvidenceLink(button, id, idleLabel) {
    var url = evidenceLink(id);
    try { if (history.replaceState) history.replaceState(null, "", "#" + id); } catch (ignore) { /* local file fallback */ }
    copyPlainText(url).then(function (copied) {
      button.classList.toggle("da-chep", copied);
      button.querySelector("span").textContent = copied ? "Đã sao chép ✓" : "Hãy sao chép thủ công";
      button.setAttribute("aria-label", copied ? "Đã sao chép link bằng\u00a0chứng" : "Không thể tự sao chép link bằng\u00a0chứng");
      setTimeout(function () {
        button.classList.remove("da-chep");
        button.querySelector("span").textContent = idleLabel;
        button.setAttribute("aria-label", idleLabel);
      }, 1900);
    }).catch(function () { button.querySelector("span").textContent = "Hãy sao chép thủ công"; });
  }
  function makeEvidenceLinkButton(id, label) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "evidence-link-copy";
    button.setAttribute("aria-label", label);
    button.innerHTML = '<i aria-hidden="true">↗</i><span>' + label + '</span>';
    button.addEventListener("click", function () { copyEvidenceLink(button, id, label); });
    return button;
  }

  factCards.forEach(function (card) {
    if (!card.id) return;
    var ribbon = card.querySelector(".fact-ribbon");
    if (!ribbon) return;
    var index = card.dataset.factIndex || card.id.replace(/\D/g, "");
    ribbon.appendChild(makeEvidenceLinkButton(card.id, "Sao chép link Fact " + index));
  });

  document.querySelectorAll("[data-uni-claim][id]").forEach(function (claim) {
    var actions = claim.querySelector(".tro");
    var detailsBody = claim.querySelector(".tu-mo");
    if (!detailsBody) return;
    if (!actions) {
      actions = document.createElement("p");
      actions.className = "tro";
      detailsBody.appendChild(actions);
    }
    actions.classList.add("has-evidence-link");
    actions.insertBefore(makeEvidenceLinkButton(claim.id, "Sao chép link claim " + claim.dataset.uniIndex), actions.firstChild);
  });

  // Article claims live inside a collapsed evidence ledger. A permalink must open
  // that ledger before scrolling; otherwise the URL points to real evidence that
  // remains invisible. The copy button uses the same canonical-aware path as Facts.
  var articleClaims = Array.prototype.slice.call(document.querySelectorAll("[data-article-claim][id]"));
  articleClaims.forEach(function (claim) {
    var actions = claim.querySelector(".case-claim-actions");
    if (!actions) return;
    actions.appendChild(makeEvidenceLinkButton(claim.id, "Sao chép link claim " + claim.id));
  });
  function openArticleClaim() {
    if (!location.hash || location.hash === "#so-claim") return;
    var claim;
    try { claim = document.querySelector(location.hash); } catch (ignore) { return; }
    if (!claim || !claim.matches("[data-article-claim]")) return;
    var ledger = claim.closest("details.case-evidence");
    if (ledger) ledger.open = true;
    requestAnimationFrame(function () { claim.scrollIntoView({ block: "start" }); });
  }
  openArticleClaim();
  addEventListener("hashchange", openArticleClaim);

  // The data archive exposes two exact byte-level handles: a stable anchor for the
  // file record, plus copy controls for its SHA-256 and download command.
  document.querySelectorAll("[data-data-file][id]").forEach(function (file) {
    var actions = file.querySelector(".data-file-actions");
    if (!actions) return;
    actions.appendChild(makeEvidenceLinkButton(file.id, "Sao chép link file " + file.dataset.fileIndex));
  });
  document.querySelectorAll("[data-copy-text]").forEach(function (button) {
    var idle = button.dataset.copyIdle || button.textContent;
    button.addEventListener("click", function () {
      copyPlainText(button.dataset.copyText || "").then(function (copied) {
        button.textContent = copied ? "Đã sao chép ✓" : "Hãy chọn thủ công";
        button.classList.toggle("da-chep", copied);
        setTimeout(function () {
          button.textContent = idle;
          button.classList.remove("da-chep");
        }, 1800);
      }).catch(function () { button.textContent = "Hãy chọn thủ công"; });
    });
  });

  // A copy control exists only when JavaScript can actually copy the command.
  document.querySelectorAll(".fact-wow details.lenh").forEach(function (details) {
    var command = details.querySelector(".cmd");
    if (!command) return;
    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "command-copy";
    copy.textContent = "Sao chép lệnh";
    copy.setAttribute("aria-label", "Sao chép lệnh tự\u00a0kiểm");
    details.insertBefore(copy, command);

    copy.addEventListener("click", function () {
      copyPlainText(command.textContent).then(function (copied) {
        copy.textContent = copied ? "Đã sao chép ✓" : "Hãy chọn lệnh thủ công";
        copy.classList.toggle("da-chep", copied);
        setTimeout(function () {
          copy.textContent = "Sao chép lệnh";
          copy.classList.remove("da-chep");
        }, 1800);
      }).catch(function () { copy.textContent = "Hãy chọn lệnh thủ công"; });
    });
  });

  // Track record: status filters change the lens, never the ledger itself.
  var trackFilters = document.querySelectorAll("[data-track-filter]");
  var trackEntries = document.querySelectorAll("[data-track]");
  var trackStatus = document.querySelector(".track-filter-status");
  var trackLedger = document.querySelector(".track-ledger");
  if (trackFilters.length && trackEntries.length) {
    var trackLabels = { xac: "đã xác nhận", song: "đang chờ", bac: "đã bị bác\u00a0bỏ", sua: "đã sửa", cho: "chưa phân\u00a0định" };
    trackFilters.forEach(function (button) {
      button.addEventListener("click", function () {
        var filter = button.dataset.trackFilter;
        var shown = 0;
        trackFilters.forEach(function (item) { item.setAttribute("aria-pressed", String(item === button)); });
        trackEntries.forEach(function (entry) {
          var visible = filter === "all" || entry.dataset.trackState === filter;
          entry.hidden = !visible;
          if (visible) shown++;
        });
        if (trackStatus) trackStatus.textContent = "Đang hiện " + shown + "\u00a0dòng" + (filter === "all" ? "" : " · " + trackLabels[filter]);
        if (trackLedger) requestAnimationFrame(function () {
          trackLedger.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
        });
      });
    });
  }

  // Article archive: the homepage remains a concise preview; this page carries
  // the complete index. Filtering never removes cards from the document, and
  // "more" reveals a bounded batch so the same layout works at 12 or 120 posts.
  var archiveCards = Array.prototype.slice.call(document.querySelectorAll("[data-article-card]"));
  var archiveFilters = document.querySelectorAll("[data-article-filter]");
  var archiveSearch = document.querySelector("[data-article-search]");
  var archiveStatus = document.querySelector("[data-article-status]");
  var archiveEmpty = document.querySelector("[data-article-empty]");
  var archiveMore = document.querySelector("[data-article-more]");
  if (archiveCards.length) {
    var archiveActive = "all";
    var archiveLimit = 12;
    function archiveNormalise(value) {
      return (value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    }
    function renderArticleArchive(resetLimit) {
      if (resetLimit) archiveLimit = 12;
      var query = archiveNormalise(archiveSearch ? archiveSearch.value : "");
      var matches = archiveCards.filter(function (card) {
        return (archiveActive === "all" || card.dataset.articleToken === archiveActive)
          && (!query || archiveNormalise(card.dataset.articleText + " " + card.textContent).indexOf(query) !== -1);
      });
      archiveCards.forEach(function (card) {
        var index = matches.indexOf(card);
        card.hidden = index < 0 || index >= archiveLimit;
      });
      var shown = Math.min(matches.length, archiveLimit);
      if (archiveStatus) archiveStatus.textContent = "Đang hiện " + shown + "\u00a0/\u00a0" + matches.length + "\u00a0bài\u00a0viết" + (archiveActive === "all" ? "" : " · " + archiveActive.toUpperCase());
      if (archiveEmpty) archiveEmpty.hidden = matches.length !== 0;
      if (archiveMore) {
        archiveMore.hidden = matches.length <= archiveLimit;
        archiveMore.textContent = "Mở thêm " + Math.min(12, Math.max(0, matches.length - archiveLimit)) + "\u00a0bài\u00a0viết ↓";
      }
    }
    function selectArchiveFilter(filter, updateUrl) {
      archiveActive = filter;
      archiveFilters.forEach(function (button) {
        button.setAttribute("aria-pressed", String(button.dataset.articleFilter === filter));
      });
      if (updateUrl && history.replaceState) {
        var url = new URL(location.href);
        if (filter === "all") url.searchParams.delete("token"); else url.searchParams.set("token", filter);
        history.replaceState(null, "", url.pathname + url.search + url.hash);
      }
      renderArticleArchive(true);
    }
    archiveFilters.forEach(function (button) {
      button.addEventListener("click", function () { selectArchiveFilter(button.dataset.articleFilter, true); });
    });
    if (archiveSearch) {
      archiveSearch.addEventListener("input", function () { renderArticleArchive(true); });
      archiveSearch.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;
        archiveSearch.value = "";
        renderArticleArchive(true);
      });
      document.addEventListener("keydown", function (event) {
        var target = event.target;
        var typing = target && (target.matches("input,textarea,select") || target.isContentEditable);
        if (event.key === "/" && !typing) { event.preventDefault(); archiveSearch.focus(); }
      });
    }
    if (archiveMore) archiveMore.addEventListener("click", function () {
      archiveLimit += 12;
      renderArticleArchive(false);
    });
    var requestedToken = new URLSearchParams(location.search).get("token")
      || (location.hash.indexOf("#token-") === 0 ? location.hash.slice(7) : "");
    var requestedButton = requestedToken && Array.prototype.slice.call(archiveFilters).find(function (button) {
      return button.dataset.articleFilter === requestedToken.toLowerCase();
    });
    selectArchiveFilter(requestedButton ? requestedToken.toLowerCase() : "all", false);
  }

  // UNI profile: one evidence vault, with local search and non-destructive lenses.
  var uniClaims = Array.prototype.slice.call(document.querySelectorAll("[data-uni-claim]"));
  var uniFilters = document.querySelectorAll("[data-uni-filter]");
  var uniSearch = document.querySelector("[data-uni-search]");
  var uniStatus = document.querySelector(".uni-filter-status");
  var uniEmpty = document.querySelector("[data-uni-empty]");
  if (uniClaims.length) {
    var uniActiveFilter = "all";
    var uniLabels = { xac: "đã xác nhận", song: "vẫn đứng\u00a0vững", sua: "đã sửa", bac: "đã bị bác\u00a0bỏ", changed: "đã đổi trạng thái" };

    function uniNormalise(value) {
      return (value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    }
    function renderUniClaims() {
      var query = uniNormalise(uniSearch ? uniSearch.value : "");
      var shown = 0;
      uniClaims.forEach(function (claim) {
        var stateMatch = uniActiveFilter === "all"
          || claim.dataset.uniState === uniActiveFilter
          || (uniActiveFilter === "changed" && claim.dataset.uniChanged === "1");
        var queryMatch = !query || uniNormalise(claim.textContent + " " + claim.dataset.uniIndex).indexOf(query) !== -1;
        var visible = stateMatch && queryMatch;
        claim.hidden = !visible;
        if (visible) shown++;
      });
      if (uniStatus) {
        var lens = uniActiveFilter === "all" ? "" : " · " + uniLabels[uniActiveFilter];
        uniStatus.textContent = "Đang hiện " + shown + "\u00a0claim" + lens + (query ? " · có từ khoá" : "");
      }
      if (uniEmpty) uniEmpty.hidden = shown !== 0;
    }

    uniFilters.forEach(function (button) {
      button.addEventListener("click", function () {
        uniActiveFilter = button.dataset.uniFilter;
        uniFilters.forEach(function (item) { item.setAttribute("aria-pressed", String(item === button)); });
        renderUniClaims();
      });
    });
    if (uniSearch) {
      uniSearch.addEventListener("input", renderUniClaims);
      uniSearch.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;
        uniSearch.value = "";
        renderUniClaims();
      });
      document.addEventListener("keydown", function (event) {
        var target = event.target;
        var typing = target && (target.matches("input,textarea,select") || target.isContentEditable);
        if (event.key === "/" && !typing) {
          event.preventDefault();
          uniSearch.focus();
        }
      });
    }
    document.querySelectorAll("[data-uni-open]").forEach(function (button) {
      button.addEventListener("click", function () {
        var open = button.dataset.uniOpen === "all";
        uniClaims.forEach(function (claim) {
          if (!claim.hidden) claim.querySelector("details").open = open;
        });
      });
    });

    function openUniHash() {
      if (!location.hash || location.hash.indexOf("#uni-claim-") !== 0) return;
      var claim = document.querySelector(location.hash);
      if (!claim) return;
      claim.hidden = false;
      var details = claim.querySelector("details");
      if (details) details.open = true;
    }
    openUniHash();
    addEventListener("hashchange", openUniHash);
  }

  // The article rail remains usable without drag precision.
  document.querySelectorAll(".khu-bai [data-rail]").forEach(function (button) {
    button.addEventListener("click", function () {
      var rail = button.closest(".khu-bai").querySelector(".rail");
      if (!rail) return;
      rail.scrollBy({ left: Number(button.dataset.rail) * Math.min(420, rail.clientWidth * .82), behavior: reduce ? "auto" : "smooth" });
    });
  });
})();
