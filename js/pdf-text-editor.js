(() => {
  const get = id => document.getElementById('pdf-' + id);
  const panel = get('editor'), toggle = get('toggle'), canvas = get('canvas');
  const status = get('status'), previous = get('previous'), next = get('next');
  const save = get('save'), undo = get('undo'), text = get('text'), mode = get('mode');
  const targets = get('targets'), replacement = get('replacement'), apply = get('apply');
  let selectedText, textItems = [];
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
    selectedText = null;
    targets.replaceChildren();
    replacement.value = '';
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
    targets.hidden = mode.value !== 'replace' || !viewport;
    get('replace-controls').hidden = mode.value !== 'replace';
    apply.disabled = !selectedText;
  }

  function visibleEdits(items) {
    return items.filter((item,index) => item.kind !== 'replace' || !items.slice(index+1).some(later => later.kind==='replace' && later.page===item.page && later.index===item.index));
  }

  function repaint(preview) {
    if (!viewport) return;
    context.drawImage(base, 0, 0);
    for (const item of visibleEdits(edits)) {
      if (item.page !== page) continue;
      const [x, y] = viewport.convertToViewportPoint(item.x, item.y);
      if (item.kind === 'replace') {
        context.fillStyle = 'white';
        context.fillRect(item.left - 1, item.top - 1, item.width + 2, item.height + 3);
        context.fillStyle = '#18283a';
        context.font = item.size * viewport.scale + 'px Helvetica, Arial, sans-serif';
        context.fillText(item.text, item.left, item.baseline);
      } else if (item.kind === 'text') {
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
    selectedText = null;
    targets.replaceChildren();
    canvas.hidden = true;
    page = number;
    sync();
    status.textContent = 'Rendering page…';
    try {
      const pdfPage = await documentView.getPage(number);
      const content = await pdfPage.getTextContent();
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
      const {renderer} = await tools();
      textItems = content.items.filter(item => item.str?.trim()).map(item => {
        const transform = renderer.Util.transform(projection.transform, item.transform);
        const height = Math.hypot(transform[2], transform[3]);
        return {text:item.str, left:transform[4], top:transform[5]-height,
          baseline:transform[5], width:Math.max(item.width*projection.scale, 4), height,
          size:height/projection.scale};
      });
      for (const [index, item] of textItems.entries()) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'pdf-text-target';
        button.setAttribute('aria-label', 'Edit ' + item.text);
        button.style.cssText = 'left:'+item.left/canvas.width*100+'%;top:'+item.top/canvas.height*100+'%;width:'+item.width/canvas.width*100+'%;height:'+item.height/canvas.height*100+'%';
        button.onclick = () => {
          selectedText = {...item, index};
          replacement.value = [...edits].reverse().find(edit => edit.kind==='replace' && edit.page===page && edit.index===index)?.text ?? item.text;
          replacement.focus();
          sync();
          status.textContent = 'Change the selected text, then choose Apply replacement.';
        };
        targets.append(button);
      }
      canvas.hidden = false;
      repaint();
      sync();
      status.textContent = 'Choose Replace text and click a text box on the page. Enter the replacement above, then apply it.';
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
    if (mode.value === 'replace') return;
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
  apply.onclick = () => {
    if (!selectedText || !viewport) return;
    const item = {...selectedText, kind:'replace', page, text:replacement.value.replace(/[\r\n]+/g,' ')};
    // Keep an edit history so Undo restores an earlier replacement.
    edits.push(item);
    repaint();
    sync();
    status.textContent = 'Text replaced. Save an edited copy when ready.';
  };
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
    const current = session, original = file, snapshot = visibleEdits(edits);
    saving = true;
    sync();
    status.textContent = 'Preparing your edited copy…';
    try {
      const {writer} = await tools();
      const {PDFDocument, StandardFonts, rgb, degrees} = writer;
      const doc = await PDFDocument.load(await original.arrayBuffer(), {updateMetadata:false});
      const font = await doc.embedFont(StandardFonts.Helvetica);
      const flattened = new Set(snapshot.filter(item => item.kind === 'replace').map(item => item.page));
      for (const pageNumber of flattened) {
        const rendered = await documentView.getPage(pageNumber);
        const vp = rendered.getViewport({scale:2});
        if (vp.width * vp.height > 24000000) throw Error('This page is too large to save with text replacements.');
        const image = document.createElement('canvas');
        image.width = Math.ceil(vp.width);
        image.height = Math.ceil(vp.height);
        const ctx = image.getContext('2d');
        await rendered.render({canvasContext:ctx,viewport:vp}).promise;
        for (const edit of snapshot.filter(item => item.page === pageNumber)) {
          const [x,y] = vp.convertToViewportPoint(edit.x || 0,edit.y || 0);
          if (edit.kind === 'replace') {
            const factor = vp.scale / (Math.min(2, 1600 / Math.max(rendered.getViewport({scale:1}).width, rendered.getViewport({scale:1}).height)));
            ctx.fillStyle='white';
            ctx.fillRect((edit.left-1)*factor,(edit.top-1)*factor,(edit.width+2)*factor,(edit.height+3)*factor);
            ctx.fillStyle='#18283a';
            ctx.font=edit.size*vp.scale+'px Helvetica, Arial, sans-serif';
            ctx.fillText(edit.text,edit.left*factor,edit.baseline*factor);
          } else if (edit.kind === 'text') {
            ctx.fillStyle='#18283a'; ctx.font=edit.size*vp.scale+'px Helvetica, Arial, sans-serif';
            ctx.fillText(edit.text,x,y);
          } else {
            const [x2,y2]=vp.convertToViewportPoint(edit.x2,edit.y2);
            ctx.fillStyle='#ffda3b66';ctx.fillRect(x,y,x2-x,y2-y);
          }
        }
        const embedded=await doc.embedPng(image.toDataURL('image/png'));
        doc.removePage(pageNumber-1);
        const resultPage=doc.insertPage(pageNumber-1,[vp.width/2,vp.height/2]);
        resultPage.drawImage(embedded,{x:0,y:0,width:vp.width/2,height:vp.height/2});
      }
      for (const item of snapshot) {
        if (flattened.has(item.page)) continue;
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
