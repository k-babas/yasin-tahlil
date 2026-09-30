/**
 * booklet.js — Tab-based Yasin + Tahlil renderer
 * After Mulai: default ke tab Yasin. Tab buttons switch content.
 */
export async function loadBooklet(container) {
  container.innerHTML = '<p class="loading-text">Memuat...</p>';

  try {
    var responses = await Promise.all([
      fetch('assets/data/yasin.json'),
      fetch('assets/data/tahlil.json')
    ]);

    var yasinRes = responses[0];
    var tahlilRes = responses[1];

    if (!yasinRes.ok) throw new Error('Gagal memuat Yasin: ' + yasinRes.status);
    if (!tahlilRes.ok) throw new Error('Gagal memuat Tahlil: ' + tahlilRes.status);

    var yasin = await yasinRes.json();
    var tahlil = await tahlilRes.json();

    container.innerHTML = '';

    // === Back button ===
    var backWrap = document.createElement('div');
    backWrap.className = 'back-btn-wrap';
    var backBtn = document.createElement('button');
    backBtn.className = 'btn-back';
    backBtn.id = 'back-btn';
    backBtn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10 3L5 8l5 5"/></svg> Kembali';
    backWrap.appendChild(backBtn);

    // === Tab bar ===
    var tabBar = document.createElement('div');
    tabBar.className = 'tab-bar';

    var tabYasin = document.createElement('button');
    tabYasin.className = 'tab-btn tab-btn--active';
    tabYasin.setAttribute('data-tab', 'yasin');
    tabYasin.textContent = 'Yasin';
    tabBar.appendChild(tabYasin);

    var tabTahlil = document.createElement('button');
    tabTahlil.className = 'tab-btn';
    tabTahlil.setAttribute('data-tab', 'tahlil');
    tabTahlil.textContent = 'Tahlil';
    tabBar.appendChild(tabTahlil);

    backWrap.appendChild(tabBar);
    container.appendChild(backWrap);

    // === Tab content wrappers ===
    var yasinContent = document.createElement('div');
    yasinContent.className = 'tab-content tab-content--active';
    yasinContent.id = 'tab-yasin';

    var tahlilContent = document.createElement('div');
    tahlilContent.className = 'tab-content';
    tahlilContent.id = 'tab-tahlil';

    // Render Yasin
    renderYasinSection(yasinContent, yasin);

    // Render Tahlil
    renderTahlilSection(tahlilContent, tahlil);

    container.appendChild(yasinContent);
    container.appendChild(tahlilContent);

    // === Footer ===
    var footer = document.createElement('footer');
    footer.className = 'site-footer';
    var footerText = document.createElement('p');
    footerText.textContent = 'Al-Fatihah untuk almarhumah';
    footer.appendChild(footerText);
    var footerArabic = document.createElement('p');
    footerArabic.className = 'arabic';
    footerArabic.textContent = 'الفَاتِحَة';
    footer.appendChild(footerArabic);
    container.appendChild(footer);

    // === Tab switching logic ===
    function switchTab(tabName) {
      // Update tab buttons
      tabBar.querySelectorAll('.tab-btn').forEach(function (b) {
        b.classList.toggle('tab-btn--active', b.getAttribute('data-tab') === tabName);
      });
      // Update content
      yasinContent.classList.toggle('tab-content--active', tabName === 'yasin');
      tahlilContent.classList.toggle('tab-content--active', tabName === 'tahlil');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    tabYasin.addEventListener('click', function () { switchTab('yasin'); });
    tabTahlil.addEventListener('click', function () { switchTab('tahlil'); });

  } catch (err) {
    console.error('Booklet load error:', err);
    container.innerHTML = '<p class="loading-text">Gagal memuat data. Silakan muat ulang halaman.</p>';
  }
}

function renderYasinSection(container, data) {
  var section = document.createElement('section');
  section.className = 'booklet-section yasin-section';

  var title = document.createElement('h2');
  title.className = 'section-title';
  title.textContent = data.surah;
  section.appendChild(title);

  var info = document.createElement('p');
  info.className = 'section-source';
  info.textContent = 'Surah ' + data.surah + ' — ' + data.count + ' ayat';
  section.appendChild(info);

  // Toggle bar
  var bar = document.createElement('div');
  bar.className = 'toggle-bar';
  bar.appendChild(makeToggle('latin-yasin', 'Latin'));
  bar.appendChild(makeToggle('terjemah-yasin', 'Terjemah'));
  section.appendChild(bar);

  // Ayat
  data.ayat.forEach(function (a) {
    var item = document.createElement('div');
    item.className = 'ayat-item';

    // Number badge
    var num = document.createElement('div');
    num.className = 'ayat-num';
    num.textContent = a.n;
    item.appendChild(num);

    // Arabic
    var ar = document.createElement('p');
    ar.className = 'arabic';
    ar.textContent = a.ar;
    item.appendChild(ar);

    // Latin (toggleable, hidden by default)
    var latin = document.createElement('p');
    latin.className = 'latin';
    latin.setAttribute('data-show', 'latin-yasin');
    latin.textContent = a.latin;
    item.appendChild(latin);

    // Terjemah (toggleable, hidden by default)
    var tr = document.createElement('p');
    tr.className = 'terjemah';
    tr.setAttribute('data-show', 'terjemah-yasin');
    tr.textContent = a.id;
    item.appendChild(tr);

    section.appendChild(item);
  });

  container.appendChild(section);
}

function renderTahlilSection(container, data) {
  var section = document.createElement('section');
  section.className = 'booklet-section tahlil-section';

  var title = document.createElement('h2');
  title.className = 'section-title';
  title.textContent = data.title;
  section.appendChild(title);

  var info = document.createElement('p');
  info.className = 'section-source';
  info.textContent = data.count + ' bagian — ' + data.source;
  section.appendChild(info);

  // Toggle bar
  var bar = document.createElement('div');
  bar.className = 'toggle-bar';
  bar.appendChild(makeToggle('latin-tahlil', 'Latin'));
  bar.appendChild(makeToggle('terjemah-tahlil', 'Terjemah'));
  section.appendChild(bar);

  // Bait
  data.bait.forEach(function (b) {
    var item = document.createElement('div');
    item.className = 'bait-item';

    // Number + section label
    var numWrap = document.createElement('div');
    numWrap.className = 'bait-header';
    var num = document.createElement('span');
    num.className = 'bait-num';
    num.textContent = b.n;
    numWrap.appendChild(num);
    if (b.section) {
      var secLabel = document.createElement('span');
      secLabel.className = 'bait-section-label';
      secLabel.textContent = b.section;
      numWrap.appendChild(secLabel);
    }
    item.appendChild(numWrap);

    // Arabic
    var ar = document.createElement('p');
    ar.className = 'arabic';
    ar.textContent = b.ar;
    item.appendChild(ar);

    // Latin (toggleable)
    var latin = document.createElement('p');
    latin.className = 'latin';
    latin.setAttribute('data-show', 'latin-tahlil');
    latin.textContent = b.latin;
    item.appendChild(latin);

    // Terjemah (toggleable)
    var tr = document.createElement('p');
    tr.className = 'terjemah';
    tr.setAttribute('data-show', 'terjemah-tahlil');
    tr.textContent = b.id;
    item.appendChild(tr);

    section.appendChild(item);
  });

  container.appendChild(section);
}

function makeToggle(id, label) {
  var btn = document.createElement('button');
  btn.className = 'btn btn-toggle';
  btn.setAttribute('aria-pressed', 'false');
  btn.setAttribute('data-target', id);
  btn.textContent = label;
  btn.addEventListener('click', function () {
    var pressed = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!pressed));

    var targets = document.querySelectorAll('[data-show="' + id + '"]');
    targets.forEach(function (el) {
      if (!pressed) {
        el.classList.add('show');
      } else {
        el.classList.remove('show');
      }
    });
  });
  return btn;
}
