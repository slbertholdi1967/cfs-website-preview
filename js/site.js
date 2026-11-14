// CFS Designs US website preview: small, dependency-free interactions.
(function () {
  // Reveal on scroll
  var els = document.querySelectorAll('.rv, .card, .proj, .svc');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
  }

  // Count-up numbers
  var counters = document.querySelectorAll('[data-count]');
  function run(el) {
    var end = +el.dataset.count, start = end > 1000 && end < 3000 ? end - 9 : 0, t0 = null, fmt = el.dataset.fmt, suf = el.dataset.suffix || (el.textContent.indexOf('+') > -1 ? '+' : '');
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / 1600), v = Math.round(start + (end - start) * (1 - Math.pow(1 - k, 3)));
      el.textContent = (fmt ? v.toLocaleString('en-US') : v) + suf;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window && counters.length) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }

  // Portfolio filters
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on');
      window.filterProjects();
    });
  });
  window.filterProjects = function () {
    var on = document.querySelector('.chip.on'), f = on ? on.dataset.f : '', s = document.querySelector('.search');
    var q = s ? s.value.trim().toLowerCase() : '', n = 0;
    document.querySelectorAll('.pall .proj').forEach(function (p) {
      var ok = (!f || p.dataset.sector === f) && (!q || p.dataset.q.indexOf(q) > -1);
      p.classList.toggle('hide', !ok);
      if (ok) n++;
    });
    var c = document.getElementById('cnt');
    if (c) c.textContent = n;
  };

  // Lightbox
  var lb = document.querySelector('.lb');
  if (lb) {
    var items = Array.prototype.slice.call(document.querySelectorAll('.gallery .g')), cur = 0, img = lb.querySelector('img'), cnt = lb.querySelector('.lbc');
    function show(i) { cur = (i + items.length) % items.length; img.src = items[cur].getAttribute('href'); cnt.textContent = (cur + 1) + ' / ' + items.length; lb.classList.add('on'); }
    items.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); show(i); }); });
    lb.querySelector('.lbp').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
    lb.querySelector('.lbn').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
    window.lbClose = function (e) { if (e.target === lb || e.target.classList.contains('lbx')) lb.classList.remove('on'); };
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') lb.classList.remove('on');
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; });
    lb.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); x0 = null; });
  }

  // Close the phone menu after a tap
  document.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('menu'); }); });
})();

// Quote form: preview only, nothing is sent.
function demoSubmit(form) {
  form.querySelector('.demo-note').hidden = false;
  form.querySelector('button').textContent = 'Received (preview)';
  return false;
}

// Tracking: example data only.
function demoTrack(form) {
  var v = form.querySelector('input').value.trim().toUpperCase(), res = document.getElementById('result'), list = document.getElementById('tlist');
  if (v !== 'DEMO-2026') { form.querySelector('input').value = ''; form.querySelector('input').placeholder = 'Preview: try DEMO-2026'; return false; }
  var rows = [
    ['Pallet #14', 'North elevation, 22 panels', 'In production', 'prod', 'Starts Fri'],
    ['Pallet #13', 'North elevation, 31 panels', 'In production', 'prod', 'Cut today'],
    ['Pallet #12', 'East elevation, 38 panels', 'On the way', 'way', 'Loaded Wed 6:55'],
    ['Pallet #11', 'East elevation, 40 panels', 'Delivered', 'done', 'Tue 10:42, signed'],
    ['Pallet #10', 'South elevation, 36 panels', 'Delivered', 'done', 'Tue 10:42, signed'],
    ['Pallet #9', 'Flashing and copings', 'Delivered', 'done', 'Mon 11:15, signed']
  ];
  list.innerHTML = rows.map(function (r) {
    return '<div class="trow"><div><b>' + r[0] + '</b><small>' + r[1] + '</small></div><div class="when"><small>' + r[4] + '</small></div><span class="st ' + r[3] + '">' + r[2] + '</span></div>';
  }).join('');
  res.hidden = false;
  res.scrollIntoView({ behavior: 'smooth' });
  return false;
}

// Aerial film window
function openFilm() {
  var f = document.querySelector('.film'); if (!f) return;
  f.classList.add('on'); var v = f.querySelector('video'); try { v.play(); } catch (e) {}
}
function closeFilm(e) {
  var f = document.querySelector('.film');
  if (e.target === f || e.target.classList.contains('lbx')) { f.classList.remove('on'); f.querySelector('video').pause(); }
}
document.addEventListener('keydown', function (e) { var f = document.querySelector('.film.on'); if (f && e.key === 'Escape') { f.classList.remove('on'); f.querySelector('video').pause(); } });

(function () {
  var el = document.getElementById('mapdata'), info = document.getElementById('mapinfo');
  if (!el || !info) return;
  var data = JSON.parse(el.textContent);
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function show(loc) {
    var v = data[loc]; if (!v) return;
    var n = v.jobs.length + v.projects.length, html = '<div class="mih"><b>' + esc(loc) + '</b><span>' + n + ' project' + (n > 1 ? 's' : '') + '</span><button type="button" class="mix" aria-label="Close">&times;</button></div><ul>';
    v.projects.forEach(function (p) { html += '<li><a href="projects/' + esc(p.slug) + '.html">' + esc(p.name) + ' <span class="pill">Photos</span></a></li>'; });
    v.jobs.forEach(function (j) { html += '<li>' + esc(j) + '</li>'; });
    html += '</ul>';
    if (v.projects.length) html += '<button type="button" class="btn btn-blue mif">Show the ' + (v.projects.length > 1 ? v.projects.length + ' projects' : 'project') + ' with photos below</button>';
    info.innerHTML = html; info.hidden = false;
    document.querySelectorAll('.map .dot.on').forEach(function (d) { d.classList.remove('on'); });
    document.querySelectorAll('.map .dot[data-loc="' + loc.replace(/"/g, '\\"') + '"]').forEach(function (d) { d.classList.add('on'); });
    info.querySelector('.mix').onclick = function () { info.hidden = true; };
    var f = info.querySelector('.mif');
    if (f) f.onclick = function () {
      var s = document.querySelector('.search'); if (!s) return;
      s.value = loc.split(',')[0]; filterProjects();
      document.getElementById('all').scrollIntoView({behavior: 'smooth'});
    };
  }
  document.querySelectorAll('.map .dot').forEach(function (d) {
    d.addEventListener('click', function () { show(d.dataset.loc); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(d.dataset.loc); } });
  });
})();
