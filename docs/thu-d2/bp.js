/* =====================================================================
   BlockPinned — JS dùng chung cho cả 6 trang. Vanilla, không framework.
   Nguyên tắc: JS chỉ THÊM tiện nghi. Mọi con số phải nằm sẵn trong HTML —
   tắt JS thì trang mất hiệu ứng, không được mất một chữ số nào.
   🔴 KHÔNG có hiệu ứng đếm-lên: đếm-lên in ra những số CHƯA TỪNG ĐO trong
   ~0,9 giây (ảnh chụp bắt đúng lúc đó là một con số sai mang tên kênh này).
   ===================================================================== */
(function () {
  'use strict';
  var itMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function soVN(x, n) { return x.toLocaleString('vi-VN', { minimumFractionDigits: n, maximumFractionDigits: n }); }

  /* ---------- nền sáng/tối ---------- */
  var saved = localStorage.getItem('bp-theme');
  var dark = saved ? saved === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('#themeBtn'); if (!b) return;
    var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('bp-theme', next);
  });

  document.addEventListener('DOMContentLoaded', function () {

    /* ---------- hiện dần khi lọt tầm mắt (số đã có sẵn trong HTML) ---------- */
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        if (el.dataset.w !== undefined) el.style.width = el.dataset.w + '%';
        else if (!itMotion) el.animate(
          [{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }],
          { duration: 380, easing: 'cubic-bezier(.16,.84,.44,1)' });
        io.unobserve(el);
      });
    }, { threshold: 0.35 });
    document.querySelectorAll('.kpi .v, .fill[data-w], .seg[data-w]').forEach(function (el) { io.observe(el); });

    /* ---------- mục lục bám chỗ đang đọc ---------- */
    var links = [].slice.call(document.querySelectorAll('.toc a'));
    if (links.length) {
      var muc = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
      var io2 = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
        });
      }, { rootMargin: '-70px 0px -65% 0px' });
      muc.forEach(function (m) { io2.observe(m); });
    }

    /* ---------- chú giải bay theo chuột ---------- */
    var tip = document.getElementById('tip');
    if (tip) document.querySelectorAll('[data-tip]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { tip.textContent = el.dataset.tip; tip.classList.add('on'); });
      el.addEventListener('mousemove', function (ev) {
        tip.style.left = Math.min(ev.clientX + 14, innerWidth - tip.offsetWidth - 10) + 'px';
        tip.style.top = (ev.clientY + 18) + 'px';
      });
      el.addEventListener('mouseleave', function () { tip.classList.remove('on'); });
    });

    /* ---------- lọc theo trạng thái ---------- */
    var legend = document.getElementById('legend');
    var note = document.getElementById('boardNote');
    var loc = document.getElementById('locTarget');   /* khối chứa các thẻ lọc được */
    if (legend && loc) {
      var goc = note ? note.textContent : '';
      var the = [].slice.call(loc.children);
      legend.addEventListener('click', function (ev) {
        var b = ev.target.closest('.lg'); if (!b) return;
        var bat = b.getAttribute('aria-pressed') !== 'true';
        legend.querySelectorAll('.lg').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', bat ? 'true' : 'false');
        var hien = 0;
        the.forEach(function (c) {
          var ok = !bat || c.classList.contains(b.dataset.st) || c.querySelector('.' + b.dataset.st);
          c.hidden = !ok; if (ok) hien++;
        });
        if (note) note.textContent = bat
          ? 'Lọc trạng thái ' + b.dataset.ten + ' — trang này còn ' + hien + '/' + the.length + ' mục. '
            + '(Con số ' + b.dataset.n + ' trên chip là của cả sổ gốc.) Bấm lần nữa để bỏ lọc.'
          : goc;
      });
    }

    /* ---------- chép link · chép lệnh ---------- */
    function bao(b, chu) {
      var cu = b.textContent; b.textContent = chu; b.classList.add('done');
      setTimeout(function () { b.textContent = cu; b.classList.remove('done'); }, 1600);
    }
    document.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-copy-link], [data-copy]'); if (!b) return;
      var chu = b.dataset.copyLink
        ? location.origin + location.pathname + b.dataset.copyLink
        : b.dataset.copy;
      navigator.clipboard.writeText(chu).then(function () { bao(b, '✓ đã chép'); }, function () { bao(b, '✕ không chép được'); });
    });

    /* ---------- ĐO LẠI: gọi RPC thật, không in sẵn số nào ---------- */
    var RPC = ['https://ethereum-rpc.publicnode.com', 'https://eth.drpc.org'];
    function rpcGoi(ep, method, params) {
      return fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: method, params: params })
      }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (j) { if (j.error) throw new Error(j.error.message || 'lỗi RPC'); return j.result; });
    }
    document.querySelectorAll('button.dolai').forEach(function (b) {
      b.addEventListener('click', async function () {
        var o = b.dataset, ra = b.closest('.dolai-box').querySelector('.ketqua');
        b.disabled = true; ra.className = 'ketqua show'; ra.textContent = 'đang gọi RPC…';
        var loi = [];
        for (var i = 0; i < RPC.length; i++) {
          var ep = RPC[i];
          try {
            var blk = await rpcGoi(ep, 'eth_blockNumber', []);
            var kq = await rpcGoi(ep, 'eth_call', [{ to: o.to, data: o.data }, blk]);
            var h = kq.slice(2), w = [];
            for (var k = 0; k < h.length; k += 64) w.push(BigInt('0x' + h.slice(k, k + 64)));
            var tu = Number(o.tu), sc = Number(o.chuSo), ghim = Number(o.ghim);
            var v = Number(w[tu]) / Math.pow(10, Number(o.thapPhan));
            var doi = Math.abs(v - ghim) >= Math.pow(10, -sc) / 2;
            ra.innerHTML = '<b class="' + (doi ? 'lech' : 'khop') + '">' + (doi ? '✎ ' : '✓ ') + soVN(v, sc) + ' ' + o.donVi
              + ' · ' + (doi ? 'ĐÃ ĐỔI so với số ghim ' + soVN(ghim, sc) : 'KHÔNG ĐỔI — khớp số ghim') + '</b>'
              + ' <span style="color:var(--faint)">tại block ' + BigInt(blk).toLocaleString('vi-VN') + '</span>'
              + '<span class="nguon">đọc từ ' + ep.replace('https://', '') + '</span>';
            b.disabled = false; return;
          } catch (e) { loi.push(ep.replace('https://', '') + ': ' + e.message); }
        }
        ra.innerHTML = '<b class="loi">✕ không đo được</b> — cả hai endpoint đều lỗi, nên trang không in số nào.'
          + '<span class="nguon">' + loi.join(' · ') + '</span>';
        b.disabled = false;
      });
    });
  });
})();
