(function() {
  function addCopyButtons() {
    document.querySelectorAll('pre > code').forEach(function(codeBlock) {
      var pre = codeBlock.parentNode;
      if (pre.classList.contains('has-copy-btn')) return;
      pre.classList.add('has-copy-btn');
      var button = document.createElement('button');
      button.className = 'copy-button';
      button.type = 'button';
      button.textContent = 'Copiar';
      button.addEventListener('click', function() {
        navigator.clipboard.writeText(codeBlock.innerText).then(function() {
          button.textContent = '\u00a1Copiado!';
          setTimeout(function() {
            button.textContent = 'Copiar';
          }, 2000);
        });
      });
      pre.style.position = 'relative';
      pre.appendChild(button);
    });
  }

  if (window.$docsify) {
    window.$docsify.plugins = [].concat(function(hook) {
      hook.doneEach(function() {
        addCopyButtons();
      });
    }, window.$docsify.plugins || []);
  } else {
    document.addEventListener('DOMContentLoaded', addCopyButtons);
  }
})();
