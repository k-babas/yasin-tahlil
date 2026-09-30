/**
 * view.js — Cover <-> Booklet crossfade transitions
 */
export function initViews() {
  var cover = document.getElementById('cover-view');
  var booklet = document.getElementById('booklet-view');
  return { cover: cover, booklet: booklet };
}

export function showBooklet(views) {
  views.cover.style.opacity = '0';
  views.cover.style.pointerEvents = 'none';
  setTimeout(function () {
    views.cover.classList.add('hidden');
    views.booklet.classList.remove('hidden');
    views.booklet.classList.add('active');
    views.booklet.style.opacity = '0';
    // Force reflow
    views.booklet.offsetHeight;
    views.booklet.style.opacity = '1';
    views.booklet.style.pointerEvents = 'auto';
    window.scrollTo({ top: 0 });

    // Trigger back button slide-in
    var backWrap = document.querySelector('.back-btn-wrap');
    if (backWrap) {
      backWrap.classList.remove('slide-in');
      void backWrap.offsetWidth;
      backWrap.classList.add('slide-in');
    }
  }, 300);
}

export function showCover(views) {
  views.booklet.style.opacity = '0';
  views.booklet.style.pointerEvents = 'none';
  setTimeout(function () {
    views.booklet.classList.remove('active');
    views.booklet.classList.add('hidden');
    views.cover.classList.remove('hidden');
    views.cover.style.opacity = '1';
    views.cover.style.pointerEvents = 'auto';
    window.scrollTo({ top: 0 });
  }, 300);
}
