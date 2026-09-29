/**
 * view.js — Cover <-> Booklet transition
 */
export function initViews() {
  const cover = document.getElementById('cover-view');
  const booklet = document.getElementById('booklet-view');
  return { cover, booklet };
}

export function showBooklet({ cover, booklet }) {
  cover.style.opacity = '0';
  cover.style.pointerEvents = 'none';
  setTimeout(() => {
    cover.classList.add('hidden');
    booklet.classList.remove('hidden');
    booklet.classList.add('active');
    booklet.style.opacity = '0';
    // force reflow
    booklet.offsetHeight;
    booklet.style.opacity = '1';
    window.scrollTo({ top: 0 });
  }, 300);
}

export function showCover({ cover, booklet }) {
  booklet.style.opacity = '0';
  booklet.style.pointerEvents = 'none';
  setTimeout(() => {
    booklet.classList.remove('active');
    booklet.classList.add('hidden');
    cover.classList.remove('hidden');
    cover.style.opacity = '1';
    cover.style.pointerEvents = 'auto';
    window.scrollTo({ top: 0 });
  }, 300);
}
