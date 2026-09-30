/**
 * cover.js — Render cover view with staggered fade-in animations
 */
export function renderCover(container, data) {
  container.innerHTML = '';

  var staggerIndex = 0;

  function createStagger(text) {
    var el = document.createElement('div');
    el.className = 'stagger';
    el.style.animationDelay = (staggerIndex * 100) + 'ms';
    staggerIndex++;
    if (text) el.textContent = text;
    return el;
  }

  // Dedication text (before photo)
  var dedication = createStagger();
  dedication.className = 'stagger cover-dedication';
  dedication.textContent = 'Dipersembahkan suami untuk almarhumah';
  container.appendChild(dedication);

  // Portrait
  var frameWrap = createStagger();
  var frame = document.createElement('div');
  frame.className = 'portrait-frame';
  var img = document.createElement('img');
  img.src = data.foto;
  img.alt = data.fotoAlt;
  img.loading = 'eager';
  img.width = 577;
  img.height = 707;
  frame.appendChild(img);
  frameWrap.appendChild(frame);
  container.appendChild(frameWrap);

  // Info block
  var info = document.createElement('div');
  info.className = 'cover-info';

  // Name
  var nameStagger = createStagger();
  var name = document.createElement('h1');
  name.textContent = data.nama;
  nameStagger.appendChild(name);
  info.appendChild(nameStagger);

  // Dates
  var datesStagger = createStagger();
  var dates = document.createElement('p');
  dates.className = 'dates';
  dates.textContent = data.lahir + ' \u2014 ' + data.wafat;
  datesStagger.appendChild(dates);
  info.appendChild(datesStagger);

  // Keluarga
  var famStagger = createStagger();
  var fam = document.createElement('ul');
  fam.className = 'keluarga';
  data.keluarga.forEach(function (k) {
    var li = document.createElement('li');
    li.textContent = k.nama + ' ';
    var span = document.createElement('span');
    span.className = 'hubungan';
    span.textContent = '(' + k.hubungan + ')';
    li.appendChild(span);
    fam.appendChild(li);
  });
  famStagger.appendChild(fam);
  info.appendChild(famStagger);

  container.appendChild(info);

  // Doa
  if (data.doa && data.doa.length) {
    var doaStagger = createStagger();
    var doas = document.createElement('div');
    doas.className = 'cover-doas';

    // Decorative divider
    var divider = document.createElement('div');
    divider.className = 'doa-divider';
    doas.appendChild(divider);

    data.doa.forEach(function (d) {
      var p = document.createElement('p');
      p.className = 'arabic';
      p.textContent = d;
      doas.appendChild(p);
    });
    doaStagger.appendChild(doas);
    container.appendChild(doaStagger);
  }

  // Mulai button
  var btnStagger = createStagger();
  var btn = document.createElement('button');
  btn.id = 'mulai-btn';
  btn.className = 'btn btn-primary';
  btn.textContent = 'Mulai';
  btn.setAttribute('aria-label', 'Buka buku Yasin dan Tahlil');
  btnStagger.appendChild(btn);
  container.appendChild(btnStagger);

  // Trigger staggered animations
  requestAnimationFrame(function () {
    var staggerEls = container.querySelectorAll('.stagger');
    staggerEls.forEach(function (el) {
      el.classList.add('visible');
    });
  });
}
