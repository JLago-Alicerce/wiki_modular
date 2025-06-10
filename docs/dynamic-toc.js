(function () {
  var containerId = 'dynamic-toc';

  function slugify(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[^\w\-\s]/g, '')
      .replace(/\s+/g, '-');
  }

  function buildToc() {
    var container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    var content = document.querySelector('.markdown-section') || document.body;
    var headings = content.querySelectorAll('h2, h3');
    if (!headings.length) return;

    var ul = document.createElement('ul');
    headings.forEach(function (h) {
      var id = h.id || slugify(h.textContent);
      h.id = id;
      var li = document.createElement('li');
      li.className = 'toc-level-' + h.tagName.toLowerCase();
      var a = document.createElement('a');
      a.href = '#' + id;
      a.textContent = h.textContent;
      li.appendChild(a);
      ul.appendChild(li);
    });

    container.appendChild(ul);
    syncScroll();
  }

  function syncScroll() {
    var container = document.getElementById(containerId);
    if (!container) return;
    var links = container.querySelectorAll('a');
    if (!links.length) return;

    var sections = Array.from(links).map(function (a) {
      var target = document.getElementById(a.getAttribute('href').slice(1));
      return { link: a, el: target };
    });

    var offset = 80;
    var current = sections[0];
    sections.forEach(function (s) {
      if (s.el.getBoundingClientRect().top - offset < 0) {
        current = s;
      }
    });
    sections.forEach(function (s) {
      s.link.classList.toggle('active', s === current);
    });
  }

  function init() {
    buildToc();
    window.removeEventListener('scroll', syncScroll);
    window.addEventListener('scroll', syncScroll);
  }

  if (window.$docsify) {
    var oldDone = window.$docsify.doneEach;
    window.$docsify.doneEach = function () {
      if (typeof oldDone === 'function') oldDone.apply(this, arguments);
      setTimeout(init, 0);
    };
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
