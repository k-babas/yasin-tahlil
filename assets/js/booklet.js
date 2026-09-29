/**
 * booklet.js — Render Yasin + Tahlil from JSON
 */
export async function loadBooklet(container) {
  container.innerHTML = '<p class="loading-text">Memuat...</p>';

  try {
    const [yasinRes, tahlilRes] = await Promise.all([
      fetch('assets/data/yasin.json'),
      fetch('assets/data/tahlil.json')
    ]);

    if (!yasinRes.ok || !tahlilRes.ok) throw new Error('Gagal memuat data');

    const yasin = await yasinRes.json();
    const tahlil = await tahlilRes.json();

    container.innerHTML = '';

    // Back button
    const backWrap = document.createElement('div');
    backWrap.className = 'back-btn-wrap';
    const backBtn = document.createElement('button');
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
    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.textContent = 'Al-Fatihah untuk almarhumah Lia Aris Tiarawati';
    container.appendChild(footer);

  } catch (err) {
    container.innerHTML = '<p class="loading-text">Gagal memuat data. Silakan muat ulang halaman.</p>';
    console.error(err);
  }
}

function renderYasinSection(container, data) {
  const section = document.createElement('section');
  section.className = 'booklet-section yasin-section';

  const title = document.createElement('h2');
  title.className = 'taitial';
  title.textContent = data.surah;
  section.appendChild(title);

  const info = document.createElement('p');
  info.className = 'section-source';
  info.textContent = 'Surah ' + data.surah + ' (' + data.count + 'x)';
  section.appendChild(info);

  // Toggle bar
  const bar = document.createElement('div');
  bar.className = 'toggle-bar';
  bar.appendChild(makeToggle('latin-' + data.surah, 'Latin'));
  bar.appendChild(makeToggle('terjemah-' + data.surah, 'Terjemah'));
  section.appendChild(bar);

  // Ayat
  data.ayat.forEach(function (a) {
    const item = document.createElement('div');
    item.className = 'ayat-item';

    const num = document.createElement('div');
    num.className = 'ayat-num';
    num.textContent = 'Ayat ' + a.n;
    item.appendChild(num);

    const ar = document.createElement('p');
    ar.className = 'arabic';
    ar.textContent = a.ar;
    item.appendChild(ar);

    const latin = document.createElement('p');
    latin.className = 'latin hidden';
    latin.setAttribute('data-show', 'latin-' + data.surah);
    latin.textContent = a.latin;
    item.appendChild(latin);

    const tr = document.createElement('p');
    tr.className = 'terjemah hidden';
    tr.setAttribute('data-show', 'terjemah-' + data.surah);
    tr.textContent = a.id;
    item.appendChild(tr);

    section.appendChild(item);
  });

  container.appendChild(section);
}

function renderTahlilSection(container, data) {
  const section = document.createElement('section');
  section.className = 'booklet-section taitial tahlil-section';

  const title = document.createElement('h2');
  title.className = 'taitial';
  title.textContent = data.title;
  section.appendChild(title);

  const info = document.createElement('p');
  info.className = 'section-source';
  info.textContent = data.count + ' bagian — ' + data.source;
  section.appendChild(info);

  // Toggle bar
  const bar = document.createElement('div');
  bar.className = 'toggle-bar';
  bar.appendChild(makeToggle('latin-tahlil', 'Latin'));
  bar.appendChild(makeToggle('terjemah-tahlil', 'Terjemah'));
  section.appendChild(bar);

  // Bait
  data.bait.forEach(function (b) {
    const item = document.createElement('div');
    item.className = 'bait-item';

    const num = document.createElement('div');
    num.className = 'bait-num';
    num.textContent = b.n + (b.section ? ' (' + b.section + ')' : '');
    item.appendChild(num);

    const ar = document.createElement('p');
    ar.className = 'arabic';
    ar.textContent = b.ar;
    item.appendChild(ar);

    const latin = document.createElement('p');
    latin.className = 'latin hidden';
    latin.setAttribute('data-show', 'latin-tahlil');
    latin.textContent = b.latin;
    item.appendChild(latin);

    const tr = document.createElement('p');
    tr.className = 'terjemah hidden';
    tr.setAttribute('data-show', 'terjemah-tahlil');
    tr.textContent = b.id;
    item.appendChild(tr);

    section.appendChild(item);
  });

  container.appendChild(section);
}

function makeToggle(id, label) {
  const btn = document.createElement('button');
  btn.className = 'btn btn-toggle';
  btn.setAttribute('aria-pressed', 'false');
  btn.setAttribute('data-target', id);
  btn.textContent = label;
  btn.addEventListener('click', function () {
    const pressed = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!pressed));
    document.querySelectorAll('[data-show="' + id + '"]').forEach(function (el) {
      el.classList.toggle('hidden');
    });
  });
  return btn;
}
