/**
 * cover.js — Render cover view from memorial data
 */
export function renderCover(container, data) {
  container.innerHTML = '';

  // Portrait
  const frame = document.createElement('div');
  frame.className = 'portrait-frame';
  const img = document.createElement('img');
  img.src = data.foto;
  img.alt = data.fotoAlt;
  img.loading = 'eager';
  img.width = 577;
  img.height = 707;
  frame.appendChild(img);
  container.appendChild(frame);

  // Info
  const info = document.createElement('div');
  info.className = 'cover-info';

  const name = document.createElement('h1');
  name.textContent = data.nama;
  info.appendChild(name);

  const dates = document.createElement('p');
  dates.className = 'dates';
  dates.textContent = data.lahir + ' — ' + data.wafat;
  info.appendChild(dates);

  // Keluarga
  const fam = document.createElement('ul');
  fam.className = 'keluarga';
  data.keluarga.forEach(function (k) {
    const li = document.createElement('li');
    li.textContent = k.nama + ' ';
    const span = document.createElement('span');
    span.className = 'hubungan';
    span.textContent = '(' + k.hubungan + ')';
    li.appendChild(span);
    fam.appendChild(li);
  });
  info.appendChild(fam);

  container.appendChild(info);

  // Doa
  if (data.doa && data.doa.length) {
    const doas = document.createElement('div');
    doas.className = 'cover-doas';
    data.doa.forEach(function (d) {
      const p = document.createElement('p');
      p.className = 'arabic';
      p.textContent = d;
      doas.appendChild(p);
    });
    container.appendChild(doas);
  }

  // Mulai button
  const btn = document.createElement('button');
  btn.id = 'mulai-btn';
  btn.className = 'btn btn-primary';
  btn.textContent = 'Mulai';
  btn.setAttribute('aria-label', 'Buka buku Yasin dan Tahlil');
  container.appendChild(btn);
}
