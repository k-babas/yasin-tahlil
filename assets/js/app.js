/**
 * app.js — Orchestrator
 */
import { memorial } from '../../data.js';
import { renderCover } from './cover.js';
import { loadBooklet } from './booklet.js';
import { initViews, showBooklet, showCover } from './view.js';

(function () {
  'use strict';

  const views = initViews();
  const coverContainer = document.getElementById('cover-content');
  const bookletContainer = document.getElementById('booklet-content');
  let bookletLoaded = false;

  // Render cover
  renderCover(coverContainer, memorial);

  // Mulai click -> load booklet lazily, then transition
  const mulaiBtn = document.getElementById('mulai-btn');
  mulaiBtn.addEventListener('click', async function () {
    if (!bookletLoaded) {
      await loadBooklet(bookletContainer);
      bookletLoaded = true;
      // Wire back button
      const backBtn = document.getElementById('back-btn');
      if (backBtn) {
        backBtn.addEventListener('click', function () {
          showCover(views);
        });
      }
    }
    showBooklet(views);
  });

  // Cover transition style
  views.cover.style.transition = 'opacity var(--transition-normal)';
  views.booklet.style.transition = 'opacity var(--transition-normal)';
})();
