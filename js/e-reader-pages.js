(() => {
  const find = id => document.getElementById(id);
  const shell = find('reader');
  const output = find('reader-output');
  const status = find('reader-status');
  const picker = find('reader-file');
  const expand = find('reader-expand');
  const open = find('reader-open');
  const pages = find('reader-pages');
  const position = find('reader-position');
  const previous = find('reader-previous');
  const next = find('reader-next');
  const limit = 80 * 1024 * 1024;
  const decoder = new TextDecoder();
  const popout = find('reader-popout');
  const detached = new URLSearchParams(location.search).has('popout') && !!window.opener;
  let chapter = 0, bookPage = 0, pageCount = 1, sections = [], flow, url, request = 0;
  let activeFile, popup, handoff;

  function xml(text) {
    const doc = new DOMParser().parseFromString(text, 'application/xml');
    if (doc.querySelector('parsererror')) throw Error('This document contains unreadable markup.');
    return doc;
  }

  async function archive(file) {
    const buffer = await file.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    const data = new DataView(buffer);
    const u16 = i => data.getUint16(i, true);
    const u32 = i => data.getUint32(i, true);
    let end = bytes.length - 22;
    const last = Math.max(0, end - 65535);
    while (end >= last && (u32(end) !== 0x06054b50 || end + 22 + u16(end + 20) !== bytes.length)) end--;
    if (end < last || u16(end + 4) || u16(end + 6)) throw Error('This book or document is not a readable ZIP package.');
    const count = u16(end + 10);
    if (count > 10000) throw Error('This document has too many parts.');
    let offset = u32(end + 16);
    const files = new Map();
    let total = 0;
    for (let i = 0; i < count; i++) {
      if (offset + 46 > end || u32(offset) !== 0x02014b50) throw Error('The document index is damaged.');
      const nameSize = u16(offset + 28);
      const name = decoder.decode(bytes.subarray(offset + 46, offset + 46 + nameSize));
      files.set(name, {flags: u16(offset + 8), method: u16(offset + 10), size: u32(offset + 20), expected: u32(offset + 24), local: u32(offset + 42)});
      offset += 46 + nameSize + u16(offset + 30) + u16(offset + 32);
    }
    return {
      has: name => files.has(name),
      async read(name) {
        const entry = files.get(name);
        if (!entry) throw Error('A required part of this document is missing.');
        const {flags, method, size, expected, local} = entry;
        if (flags & 1) throw Error('Password-protected documents are unsupported.');
        const cap = 12 * 1024 * 1024;
        if (expected > cap || (total += expected) > limit) throw Error('This document expands beyond the reader’s size limit.');
        if (local + 30 > bytes.length || u32(local) !== 0x04034b50) throw Error('A document entry is damaged.');
        const start = local + 30 + u16(local + 26) + u16(local + 28);
        if (start + size > bytes.length) throw Error('A document entry is incomplete.');
        const payload = bytes.subarray(start, start + size);
        if (method === 0 && size === expected) return decoder.decode(payload);
        if (method !== 8) throw Error('This document uses an unsupported compression format.');
        let inflater;
        try { inflater = new DecompressionStream('deflate-raw'); }
        catch { throw Error('Update your browser to open compressed EPUB and DOCX files.'); }
        const reader = new Blob([payload]).stream().pipeThrough(inflater).getReader();
        let length = 0, value = '';
        const partDecoder = new TextDecoder();
        try {
          for (;;) {
            const chunk = await reader.read();
            if (chunk.done) break;
            length += chunk.value.length;
            if (length > expected) throw Error('A document entry exceeds its declared size.');
            value += partDecoder.decode(chunk.value, {stream: true});
          }
        } finally { await reader.cancel(); }
        if (length !== expected) throw Error('A document entry is incomplete.');
        return value + partDecoder.decode();
      }
    };
  }

  const tags = new Set('h1 h2 h3 h4 h5 h6 p div section article blockquote pre code ul ol li table thead tbody tr th td em strong b i br hr sup sub dl dt dd'.split(' '));
  const skip = new Set('script style iframe object embed svg math template noscript form audio video link meta'.split(' '));
  function safeHtml(text) {
    // Template contents are inert. Rebuild from allowed elements and text only.
    const inert = document.createElement('template');
    inert.innerHTML = text;
    const result = document.createDocumentFragment();
    function copy(source, dest, depth) {
      if (depth > 80) return;
      for (const node of source.childNodes) {
        if (node.nodeType === 3) dest.append(document.createTextNode(node.textContent));
        if (node.nodeType !== 1 || skip.has(node.localName)) continue;
        if (node.localName === 'img') {
          const alt = node.getAttribute('alt');
          if (alt) dest.append(document.createTextNode('[' + alt + ']'));
        } else if (tags.has(node.localName)) {
          const clean = document.createElement(node.localName);
          copy(node, clean, depth + 1);
          dest.append(clean);
        } else copy(node, dest, depth + 1);
      }
    }
    copy(inert.content, result, 0);
    return result;
  }

  async function epub(file) {
    const zip = await archive(file);
    const packageName = xml(await zip.read('META-INF/container.xml')).getElementsByTagNameNS('*', 'rootfile')[0]?.getAttribute('full-path');
    const packageDoc = xml(await zip.read(packageName));
    const base = 'https://book.invalid/' + packageName.split('/').map(encodeURIComponent).join('/');
    const manifest = new Map([...packageDoc.getElementsByTagNameNS('*', 'item')].map(item => [item.getAttribute('id'), item]));
    const spine = [...packageDoc.getElementsByTagNameNS('*', 'itemref')];
    if (spine.length > 1000) throw Error('This EPUB has too many chapters.');
    const chapters = [];
    for (const ref of spine) {
      const item = manifest.get(ref.getAttribute('idref'));
      if (!item || !['application/xhtml+xml', 'text/html'].includes(item.getAttribute('media-type'))) continue;
      const target = new URL(item.getAttribute('href'), base);
      if (target.origin !== 'https://book.invalid') continue;
      const path = decodeURIComponent(target.pathname.slice(1));
      if (zip.has(path)) chapters.push(await zip.read(path));
    }
    if (!chapters.length) throw Error('No readable EPUB chapters were found. DRM-protected books are unsupported.');
    return chapters;
  }

  async function word(file) {
    const zip = await archive(file);
    const doc = xml(await zip.read('word/document.xml'));
    const content = document.createDocumentFragment();
    const ns = doc.documentElement.namespaceURI;
    for (const paragraph of doc.getElementsByTagNameNS(ns, 'p')) {
      const p = document.createElement('p');
      const text = [...paragraph.getElementsByTagNameNS(ns, 't')].map(node => node.textContent).join('');
      p.textContent = text || '\u00a0';
      content.append(p);
    }
    return content;
  }

  function layoutBook() {
    if (!flow || !output.clientWidth) return;
    const width = output.clientWidth;
    pageCount = Math.max(1, Math.ceil((flow.scrollWidth - 1) / width));
    bookPage = Math.min(bookPage, pageCount - 1);
    output.scrollLeft = bookPage * width;
    previous.disabled = chapter === 0 && bookPage === 0;
    next.disabled = chapter === sections.length - 1 && bookPage === pageCount - 1;
    position.textContent = 'Chapter ' + (chapter + 1) + ' of ' + sections.length +
      ' · Page ' + (bookPage + 1) + ' of ' + pageCount;
  }

  function displayChapter(page = 0) {
    flow = document.createElement('div');
    flow.className = 'reader-book-flow';
    flow.append(safeHtml(sections[chapter]));
    output.replaceChildren(flow);
    bookPage = page;
    layoutBook();
  }

  previous.onclick = () => {
    if (bookPage > 0) { bookPage--; layoutBook(); }
    else if (chapter > 0) { chapter--; displayChapter(Number.MAX_SAFE_INTEGER); }
  };
  next.onclick = () => {
    if (bookPage + 1 < pageCount) { bookPage++; layoutBook(); }
    else if (chapter + 1 < sections.length) { chapter++; displayChapter(); }
  };
  new ResizeObserver(layoutBook).observe(output);
  output.addEventListener('keydown', event => {
    if (!flow || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    (event.key === 'ArrowLeft' ? previous : next).click();
  });

  async function read(file, locationInBook) {
    if (!file) return;
    const current = ++request;
    activeFile = file;
    flow = null;
    popout.disabled = false;
    shell.dispatchEvent(new CustomEvent('reader-pdf-file'));
    if (url) URL.revokeObjectURL(url);
    url = null;
    output.replaceChildren();
    output.classList.remove('reader-media', 'reader-book');
    output.scrollLeft = 0;
    open.hidden = pages.hidden = true;
    output.hidden = true;
    status.textContent = 'Opening ' + file.name + '…';
    const ext = file.name.split('.').at(-1).toLowerCase();
    try {
      if (file.size > limit) throw Error('Choose a file under 80 MB.');
      if (ext === 'epub') {
        const chapters = await epub(file);
        if (current !== request) return;
        sections = chapters;
        chapter = Math.max(0, Math.min(locationInBook?.chapter || 0, sections.length - 1));
        output.classList.add('reader-book');
        output.hidden = pages.hidden = false;
        displayChapter(Math.max(0, locationInBook?.bookPage || 0));
      } else if (ext === 'docx' || ext === 'html' || ext === 'htm' || ['txt', 'md', 'csv', 'log', 'json'].includes(ext)) {
        const data = ext === 'docx' ? await word(file) : await file.text();
        if (current !== request) return;
        if (ext === 'docx') output.append(data);
        else if (ext === 'html' || ext === 'htm') output.append(safeHtml(data));
        else {
          const pre = document.createElement('pre');
          pre.textContent = data;
          output.append(pre);
        }
      } else if (['pdf', 'png', 'jpg', 'jpeg', 'webp', 'gif', 'avif', 'bmp'].includes(ext)) {
        const mime = {pdf:'application/pdf', png:'image/png', jpg:'image/jpeg', jpeg:'image/jpeg', webp:'image/webp', gif:'image/gif', avif:'image/avif', bmp:'image/bmp'};
        url = URL.createObjectURL(new Blob([file], {type: mime[ext]}));
        const media = document.createElement(ext === 'pdf' ? 'iframe' : 'img');
        media.src = url;
        if (ext === 'pdf') {
          media.title = 'PDF document';
          output.classList.add('reader-media');
          shell.dispatchEvent(new CustomEvent('reader-pdf-file', {detail:file}));
        } else media.alt = file.name;
        output.append(media);
        open.href = url;
        open.hidden = false;
      } else throw Error('This format is unsupported. Try EPUB, PDF, DOCX, HTML, a text file, or an image.');
      output.hidden = false;
      status.textContent = file.name + (ext === 'pdf' ? ' · If the PDF preview is blank, use Open separately.' : '');
    } catch (error) {
      if (current === request) status.textContent = error instanceof RangeError ? 'This document is damaged or too large to open.' : error.message || 'This file could not be opened.';
    }
  }

  window.addEventListener('message', event => {
    if (event.origin !== location.origin) return;
    if (event.source === popup && event.data?.type === 'origami-reader-ready' && handoff) {
      popup.postMessage({type:'origami-reader-open', ...handoff}, location.origin);
      handoff = null;
    } else if (detached && event.source === window.opener && event.data?.type === 'origami-reader-open' && event.data.file instanceof File) {
      read(event.data.file, event.data.locationInBook);
    }
  });
  popout.onclick = () => {
    if (!activeFile) return;
    handoff = {file:activeFile, locationInBook:flow ? {chapter, bookPage} : null};
    popup = window.open('/e-reader?popout=1', '_blank', 'popup,width=900,height=820');
    if (!popup) {
      handoff = null;
      status.textContent = 'Allow pop-ups for this site, then choose Pop out reader again.';
    }
  };
  if (detached) {
    document.body.classList.add('reader-detached');
    popout.hidden = true;
    setExpanded(true);
    window.opener.postMessage({type:'origami-reader-ready'}, location.origin);
  }

  picker.addEventListener('change', () => {
    read(picker.files[0]);
    picker.value = '';
  });
  window.addEventListener('dragover', event => {
    if (event.dataTransfer.types.includes('Files')) event.preventDefault();
  });
  window.addEventListener('drop', event => {
    if (!event.dataTransfer.files.length) return;
    event.preventDefault();
    if (shell.contains(event.target)) read(event.dataTransfer.files[0]);
  });
  function setExpanded(value) {
    shell.classList.toggle('reader-expanded', value);
    document.body.classList.toggle('reader-lock', value);
    expand.setAttribute('aria-pressed', String(value));
    expand.textContent = value ? 'Exit expanded view' : 'Expand reader';
  }
  expand.onclick = () => setExpanded(!shell.classList.contains('reader-expanded'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && shell.classList.contains('reader-expanded')) {
      setExpanded(false);
      expand.focus();
    }
  });
})();
