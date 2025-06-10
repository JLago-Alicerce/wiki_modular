(function () {
  const STORAGE_KEY = 'theme';
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const saved = localStorage.getItem(STORAGE_KEY);
  const current = saved || (systemPrefersDark ? 'dark' : 'light');
  const root = document.documentElement;
  root.classList.toggle('dark', current === 'dark');

  function updateButton(isDark) {
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.textContent = isDark ? '🌙' : '☀️';
    }
  }

  updateButton(current === 'dark');

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.addEventListener('click', function () {
        const isDark = !root.classList.contains('dark');
        root.classList.toggle('dark', isDark);
        localStorage.setItem(STORAGE_KEY, isDark ? 'dark' : 'light');
        updateButton(isDark);
      });
    }
  });
})();
