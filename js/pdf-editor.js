(() => {
  const get = id => document.getElementById('pdf-' + id);
  const panel = get('editor'), toggle = get('toggle'), canvas = get('canvas');
  const status = get('status'), previous = get('previous'), next = get('next');
  const save = get('save'), undo = get('undo'), text = get('text'), mode = get('mode');
  const source = document.getElementById('reader-output');
  const base = document.createElement('canvas');
  const context = canvas.getContext('2d');
  const libraryUrl = 'https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js';
  const rendererUrl = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/';
  let file, documentView, loadingTask, viewport, page, start;
  let session = 0, view = 0, edits = [], saving = false, libraries;

  function tools() {
    if (!libraries) {
      libraries = Promise.all([
        import(rendererUrl + 'pdf.min.mjs'),
        new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = libraryUrl;
          script.onload = () => resolve(window.PDFLib);
          script.onerror = () => { script.remove(); reject(Error('PDF tools could not load.')); };
          document.head.append(script);
        })
      ]).then(([renderer, writer]) => {
        renderer.GlobalWorkerOptions.workerSrc = rendererUrl + 'pdf.worker.min.mjs';
        return {renderer, writer};
      }).catch(error => { libraries = null; throw error; });
    }
    return libraries;
  }

  function reset(nextFile) {
    session++;
    view++;
    if (loadingTask) loadingTask.destroy().catch(() => {});
    file = nextFile;
    loadingTask = documentView = viewport = start = null;
    saving = false;
    edits = [];
    panel.hidden = true;
    toggle.hidden = !file;
    toggle.disabled = false;
    toggle.textContent = 'Edit PDF';
    toggle.setAttribute('aria-expanded', 'false');
  }

  document.getElementById('reader').addEventListener('reader-pdf-file', event => reset(event.detail));

  function sync() {
    previous.disabled = !viewport || page <= 1;
    next.disabled = !viewport || page >= documentView.numPages;
    save.disabled = !edits.length || saving;
    undo.disabled = !edits.length;
    get('page').textContent = documentView ? 'Page ' + page + ' of ' + documentView.numPages : '';
    text.disabled = mode.value !== 'text';
  }

  function repaint(preview) {
    if (!viewport) return;
    context.drawImage(base, 0, 0);
    for (const item of edits) {
      if (item.page !== page) continue;
      const [x, y] = viewport.convertToViewportPoint(item.x, item.y);
      if (item.kind === 'text') {
        context.fillStyle = '#18283a';
        context.font = item.size * viewport.scale + 'px Helvetica, Arial, sans-serif';
        context.fillText(item.text, x, y);
      } else {
        const [x2, y2] = viewport.convertToViewportPoint(item.x2, item.y2);
        context.fillStyle = '#ffda3b66';
        context.fillRect(x, y, x2 - x, y2 - y);
      }
    }
    if (preview && start) {
      context.fillStyle = '#ffda3b66';
      context.fillRect(start.x, start.y, preview.x - start.x, preview.y - start.y);
    }
  }

  async function render(number) {
    const current = ++view;
    viewport = start = null;
    canvas.hidden = true;
    page = number;
    sync();
    status.textContent = 'Rendering page…';
    try {
      const pdfPage = await documentView.getPage(number);
      const size = pdfPage.getViewport({scale: 1});
      const projection = pdfPage.getViewport({scale: Math.min(2, 1600 / Math.max(size.width, size.height))});
      const stage = document.createElement('canvas');
      stage.width = Math.ceil(projection.width);
      stage.height = Math.ceil(projection.height);
      await pdfPage.render({canvasContext: stage.getContext('2d'), viewport: projection}).promise;
      if (current !== view) return;
      canvas.width = base.width = stage.width;
      canvas.height = base.height = stage.height;
      base.getContext('2d').drawImage(stage, 0, 0);
      viewport = projection;
      canvas.hidden = false;
      repaint();
      sync();
      status.textContent = 'Type your text, then click where it should go. To highlight, select Highlight and drag across the page.';
    } catch {
      if (current === view) status.textContent = 'This page could not be rendered.';
    }
  }

  toggle.onclick = async () => {
    if (!panel.hidden) {
      panel.hidden = true;
      source.hidden = false;
      toggle.textContent = 'Edit PDF';
      toggle.setAttribute('aria-expanded', 'false');
      return;
    }
    panel.hidden = false;
    source.hidden = true;
    toggle.textContent = 'Read PDF';
    toggle.setAttribute('aria-expanded', 'true');
    if (documentView) return;
    const current = session;
    canvas.hidden = true;
    sync();
    toggle.disabled = true;
    status.textContent = 'Loading the PDF editor…';
    try {
      const {renderer} = await tools();
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (current !== session) return;
      loadingTask = renderer.getDocument({data: bytes, isEvalSupported: false, enableXfa: false});
      const loaded = await loadingTask.promise;
      if (current !== session) return;
      documentView = loaded;
      await render(1);
    } catch {
      if (current === session) status.textContent = 'This PDF could not be opened for editing. It may be encrypted, damaged, or the editor could not load.';
    } finally {
      if (current === session) toggle.disabled = false;
    }
  };

  function point(event) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: Math.max(0, Math.min(canvas.width, (event.clientX - rect.left) * canvas.width / rect.width)),
      y: Math.max(0, Math.min(canvas.height, (event.clientY - rect.top) * canvas.height / rect.height))
    };
  }

  canvas.onpointerdown = event => {
    if (!viewport || !event.isPrimary || event.button !== 0) return;
    const p = point(event);
    if (mode.value === 'highlight') {
      start = {...p, pointer: event.pointerId};
      canvas.setPointerCapture(event.pointerId);
      return;
    }
    const value = text.value.trim();
    if (!value) { status.textContent = 'Enter the text you want to add first.'; text.focus(); return; }
    const size = Number(get('size').value);
    const [x, y] = viewport.convertToPdfPoint(p.x, p.y);
    edits.push({kind:'text', page, x, y, text:value, size, rotation:viewport.rotation});
    repaint();
    sync();
    status.textContent = 'Text added. Save an edited copy when you’re ready.';
  };

  canvas.onpointermove = event => { if (start?.pointer === event.pointerId) repaint(point(event)); };
  canvas.onpointerup = event => {
    if (start?.pointer !== event.pointerId) return;
    const finish = point(event);
    if (Math.abs(finish.x - start.x) >= 3 && Math.abs(finish.y - start.y) >= 3) {
      const [x,y] = viewport.convertToPdfPoint(start.x,start.y);
      const [x2,y2] = viewport.convertToPdfPoint(finish.x,finish.y);
      edits.push({kind:'highlight',page,x,y,x2,y2});
      status.textContent = 'Highlight added.';
    }
    start = null;
    repaint();
    sync();
  };
  canvas.onlostpointercapture = () => { if (start) { start = null; repaint(); } };
  mode.onchange = sync;
  previous.onclick = () => render(page - 1);
  next.onclick = () => render(page + 1);
  undo.onclick = () => {
    const edit = edits.pop();
    if (edit.page !== page) render(edit.page);
    else { repaint(); sync(); }
    status.textContent = 'Last edit undone.';
  };

  save.onclick = async () => {
    const current = session, original = file, snapshot = [...edits];
    saving = true;
    sync();
    status.textContent = 'Preparing your edited copy…';
    try {
      const {writer} = await tools();
      const {PDFDocument, StandardFonts, rgb, degrees} = writer;
      const doc = await PDFDocument.load(await original.arrayBuffer(), {updateMetadata:false});
      const font = await doc.embedFont(StandardFonts.Helvetica);
      for (const item of snapshot) {
        const pdfPage = doc.getPage(item.page - 1);
        if (item.kind === 'text') {
          try { font.encodeText(item.text); }
          catch { throw Error('Some characters could not be saved. Undo that text and try letters supported by Helvetica.'); }
          pdfPage.drawText(item.text, {x:item.x,y:item.y,size:item.size,font,rotate:degrees(item.rotation),color:rgb(.094,.157,.227)});
        } else pdfPage.drawRectangle({
          x:Math.min(item.x,item.x2), y:Math.min(item.y,item.y2),
          width:Math.abs(item.x2-item.x), height:Math.abs(item.y2-item.y),
          color:rgb(1,.855,.23), opacity:.4
        });
      }
      const result = await doc.save();
      if (current !== session) return;
      const url = URL.createObjectURL(new Blob([result], {type:'application/pdf'}));
      const link = document.createElement('a');
      link.href = url;
      link.download = original.name.replace(/\.pdf$/i,'') + '-edited.pdf';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
      status.textContent = 'Edited copy saved.';
    } catch (error) {
      if (current === session) status.textContent = error.message || 'The edited PDF could not be saved.';
    } finally {
      if (current === session) { saving = false; sync(); }
    }
  };
})();
