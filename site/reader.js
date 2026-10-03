(() => {
  const params = new URLSearchParams(location.search);
  const path = params.get('path') || '';
  const content = document.getElementById('reader-content');
  const title = document.getElementById('reader-title');
  const prefix = document.body.dataset.contentPrefix;
  const locale = document.body.dataset.locale;
  const messages = {
    zh: ['正在读取正文…', '正文加载失败。请稍后重试。'],
    en: ['Loading the article…', 'Could not load the article. Please try again.'],
    ja: ['本文を読み込んでいます…', '本文を読み込めませんでした。後でもう一度お試しください。']
  };
  const escapeHtml = value => value.replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const safePath = value => /^(book|cities)\/(?!.*(?:^|\/)\.\.?\/)[^?#]+\.md$/.test(value);
  const normalize = value => {
    const parts = path.split('/').slice(0, -1);
    for (const part of value.split('/')) {
      if (part === '..') parts.pop();
      else if (part && part !== '.') parts.push(part);
    }
    const result = parts.join('/');
    return safePath(result) ? result : null;
  };
  const link = (label, target) => {
    if (/^https?:\/\//.test(target)) return `<a href="${escapeHtml(target)}">${label}</a>`;
    const [file, hash = ''] = target.split('#');
    const next = normalize(file);
    if (!next) return label;
    return `<a href="reader.html?path=${encodeURIComponent(next)}${hash ? '#' + encodeURIComponent(hash) : ''}">${label}</a>`;
  };
  const inline = value => {
    let result = escapeHtml(value);
    result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, target) => link(label, target.replaceAll('&amp;', '&')));
    result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    return result.replace(/`([^`]+)`/g, '<code>$1</code>');
  };
  function markdown(source) {
    const lines = source.replace(/\r\n/g, '\n').split('\n');
    const blocks = [];
    let paragraph = [], list = [], listTag = '';
    const flush = () => {
      if (paragraph.length) { blocks.push(`<p>${inline(paragraph.join(' '))}</p>`); paragraph = []; }
      if (list.length) { blocks.push(`<${listTag}>${list.map(item => `<li>${inline(item)}</li>`).join('')}</${listTag}>`); list = []; listTag = ''; }
    };
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) { flush(); continue; }
      const tableSeparator = /^\|[\s:|-]+\|$/;
      if (line.startsWith('|') && i + 1 < lines.length && tableSeparator.test(lines[i + 1].trim())) {
        flush();
        const cells = row => row.slice(1, -1).split('|').map(cell => cell.trim());
        const head = cells(line); i += 2;
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith('|')) { rows.push(cells(lines[i].trim())); i++; }
        i--;
        blocks.push(`<div class="table-scroll"><table><thead><tr>${head.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${inline(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
        continue;
      }
      const heading = line.match(/^(#{1,6})\s+(.+)$/);
      if (heading) { flush(); const n = heading[1].length; blocks.push(`<h${n}>${inline(heading[2])}</h${n}>`); continue; }
      if (/^>\s?/.test(line)) { flush(); blocks.push(`<blockquote>${inline(line.replace(/^>\s?/, ''))}</blockquote>`); continue; }
      const item = line.match(/^([-*]|\d+\.)\s+(.+)$/);
      if (item) {
        if (paragraph.length) flush();
        const tag = /\d/.test(item[1][0]) ? 'ol' : 'ul';
        if (list.length && listTag !== tag) flush();
        listTag = tag; list.push(item[2]); continue;
      }
      if (list.length) flush();
      paragraph.push(line);
    }
    flush();
    return blocks.join('\n');
  }
  for (const anchor of document.querySelectorAll('[data-reader-lang]')) {
    const lang = anchor.dataset.readerLang;
    anchor.href = `${lang === 'zh' ? prefix : (locale === 'zh' ? '' : '../') + lang + '/'}reader.html?path=${encodeURIComponent(path)}`;
    if (lang === locale) anchor.setAttribute('aria-current', 'page');
  }
  if (!safePath(path)) { content.textContent = messages[locale][1]; return; }
  content.textContent = messages[locale][0];
  const asset = prefix + 'content/' + path.split('/').map(encodeURIComponent).join('/');
  fetch(asset).then(response => {
    if (!response.ok) throw new Error(String(response.status));
    return response.text();
  }).then(source => {
    const heading = source.match(/^#\s+(.+)$/m);
    if (heading) { title.textContent = heading[1]; document.title = heading[1] + ' · ' + document.title; }
    content.innerHTML = markdown(source.replace(/^#\s+.+\n?/, ''));
  }).catch(() => { content.textContent = messages[locale][1]; });
})();
