/**
 * booklet.js — Render Yasin + Tahlil from JSON, with smooth toggle transitions
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

    if (!yasinRes.ok || !tahlilRes.ok) throw new Error('Gagal memuat data');

    var yasin = await yasinRes.json();
    var tahlil = await tahlilRes.json();

    container.innerHTML = '';

    // Back button
    var backWrap = document.createElement('div');
    backWrap.className = 'back-btn-wrap';
    var backBtn = document.createElement('button');
    backBtn.className = 'btn-back';
    backBtn.id = 'back-btn';
    backBtn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10 3L5 8l5 5"/></svg> Kembali';
    backWrap.appendChild(backBtn);
    container.appendChild(backWrap);

    // Yasin section
    renderYasinSection(container, yasin);

    // Tahlil section
    renderTahlilSection(container, tahlil);

    // Footer
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

  } catch (err) {
    container.innerHTML = '<p class="loading-text">Gagal memuat data. Silakan muat ulang halaman.</p>';
    console.error(err);
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
  info.textContent = 'Surah ' + data.surah + ' \u2014 ' + data.count + ' ayat';
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

    // Arabic (above transliteration)
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
  info.textContent = data.count + ' bagian \u2014 ' + data.source;
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

    // Number badge
    var num = document.createElement('div');
    num.className = 'bait-num';
    num.textContent = b.n;
    item.appendChild(num);

    // Section label
    if (b.section) {
      var secLabel = document.createElement('span');
      secLabel.className = 'bait-num-full';
      secLabel.textContent = ' \u2014 ' + b.section;
      secLabel.style.color = 'var(--accent)';
      item.appendChild(secLabel);
    }

    // Arabic (above transliteration)
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

    // Smooth toggle with height transition
    var targets = document.querySelectorAll('[data-show="' + id + '"]');
    targets.forEach(function (el) {
      if (!pressed) {
        // Show
        el.classList.add('show');
      } else {
        // Hide
        el.classList.remove('show');
      }
    });
  });
  return btn;
}
