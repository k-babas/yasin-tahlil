/**
 * app.js — Orchestrator
 * Manages theme toggle, cover rendering, booklet loading, and view transitions.
 */
import { memorial } from '../../data.js';
import { renderCover } from './cover.js';
import { loadBooklet } from './booklet.js';
import { initViews, showBooklet, showCover } from './view.js';

(function () {
  'use strict';

  // --- Theme Toggle ---
  const themeToggle = document.getElementById('theme-toggle');
  const htmlEl = document.documentElement;

  // Load saved theme or respect system preference
  function initTheme() {
    const saved = localStorage.getItem('memorial-theme');
    if (saved) {
      htmlEl.setAttribute('data-theme', saved);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      htmlEl.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
  }

  function toggleTheme() {
    const current = htmlEl.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', next);
    localStorage.setItem('memorial-theme', next);

    // Spin animation
    themeToggle.classList.add('theme-toggle--spinning');
    setTimeout(function () {
      themeToggle.classList.remove('theme-toggle--spinning');
    }, 400);
  }

  initTheme();
  themeToggle.addEventListener('click', toggleTheme);

  // Progressive enhancement: enable stagger animations only when JS is ready
  document.documentElement.classList.add('stagger-ready');

  // --- Views ---
  const views = initViews();
  const coverContainer = document.getElementById('cover-content');
  const bookletContainer = document.getElementById('booklet-content');
  let bookletLoaded = false;

  // --- Render Cover ---
  renderCover(coverContainer, memorial);

  // --- Mulai Button ---
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

  // --- Cover transition styles ---
  views.cover.style.transition = 'opacity var(--transition-normal)';
  views.booklet.style.transition = 'opacity var(--transition-normal)';
})();
