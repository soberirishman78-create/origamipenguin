(async () => {
  const get = name => document.querySelector('#fold-' + name);
  const panel = get('quest');
  const canvas = get('surface');
  const ctx = canvas.getContext('2d');
  const photo = get('image');
  const status = get('status');
  const next = get('continue');
  const hint = get('hint');
  const access = get('access');
  const picker = get('models');
  const previous = get('previous');
  const size = 400;
  const distance = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  const point = pair => {
    const [x, y] = pair.split(',').map(Number);
    return {x, y};
  };
  const load = async url => {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Fold data unavailable');
    return response;
  };

  let levels, scene, drag, cursor;
  let level = 0;
  let move = 1;
  let part = 0;
  let phase = 'loading';
  let showingHint = false;
  let revision = 0;
  const model = () => levels[level];
  const step = () => model().steps[move];
  const action = () => scene.actions[part];
  const modelId = item => item.name.toLowerCase().replaceAll(' ', '-');

  function image(data) {
    photo.src = '/' + data.src;
    photo.alt = data.alt;
    photo.width = data.width;
    photo.height = data.height;
  }

  async function readScene() {
    if (step().scene) return step().scene;
    const svgText = await (await load('/' + step().image.src)).text();
    const svg = new DOMParser().parseFromString(svgText, 'image/svg+xml');
    const half = step().image.width / 2;
    const penguinDetail = model().name === 'Penguin' && (move === 11 || move === 12);
    const tipDetail = model().name === 'Crane' && (move === 23 || move === 24);
    const detail = penguinDetail || tipDetail;
    const inPanel = ({x}) => detail ? Math.abs(x - half) < (penguinDetail ? 65 : 40) : x < half - 35;
    const layers = [...svg.querySelectorAll('polygon')].map(el => ({
      vertices: el.getAttribute('points').trim().split(/\s+/).map(point),
      fill: el.getAttribute('fill')
    })).filter(layer => layer.vertices.every(inPanel));
    const arrows = [...svg.querySelectorAll('path[marker-end]')].map(el => {
      const points = el.getAttribute('d').match(/-?[\d.]+,-?[\d.]+/g).map(point);
      return {from: points[0], to: points.at(-1)};
    }).filter(arrow => inPanel(arrow.from) && inPanel(arrow.to));
    if (penguinDetail) {
      if (move === 11) arrows.splice(1);
      else arrows.splice(0, 1);
    }
    if (model().name === 'Crane' && move === 10) arrows.splice(1);
    const all = [...layers.flatMap(layer => layer.vertices), ...arrows.flatMap(a => [a.from, a.to])];
    if (!all.length) throw new Error('Missing fold geometry');
    const xs = all.map(p => p.x), ys = all.map(p => p.y);
    const left = Math.min(...xs), right = Math.max(...xs);
    const top = Math.min(...ys), bottom = Math.max(...ys);
    const scale = 290 / Math.max(right - left, bottom - top);
    const fit = p => ({x: 200 + (p.x - (left + right) / 2) * scale, y: 200 + (p.y - (top + bottom) / 2) * scale});
    return {
      layers: layers.map(layer => ({fill: layer.fill, vertices: layer.vertices.map(fit)})),
      actions: arrows.map(a => ({from: fit(a.from), to: fit(a.to)}))
    };
  }

  function shape(vertices) {
    ctx.beginPath();
    for (const [i, p] of vertices.entries()) {
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    }
    ctx.closePath();
  }

  function drawLayers(back = false, layers = scene.layers) {
    for (const layer of layers) {
      shape(layer.vertices);
      ctx.fillStyle = back ? (step().scene ? (layer.fill === '#fffdf6' ? '#f2a676' : '#fffdf6') : model().name === 'Heart' ? '#e898b1' : '#a9cfed') : layer.fill;
      ctx.fill();
      ctx.strokeStyle = '#27394a';
      ctx.lineWidth = 1.6;
      ctx.stroke();
    }
  }

  function mark(p, radius, fill) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.strokeStyle = '#174e50';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  // Reflect the grabbed side across the crease between the corner and pointer.
  function preview({from, layer}, to) {
    const length = distance(from, to);
    if (length < 2) { drawLayers(); return; }
    const angle = Math.atan2(to.y - from.y, to.x - from.x);
    const x = (from.x + to.x) / 2, y = (from.y + to.y) / 2;
    const movingLayers = layer === undefined ? scene.layers : [scene.layers[layer]];
    if (layer !== undefined) drawLayers(false, scene.layers.filter((_, index) => index !== layer));
    for (const moving of [false, true]) {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(angle);
      ctx.beginPath();
      ctx.rect(0, -1200, 1200, 2400);
      ctx.clip();
      if (moving) ctx.scale(-1, 1);
      ctx.rotate(-angle);
      ctx.translate(-x, -y);
      drawLayers(moving, movingLayers);
      ctx.restore();
    }
  }

  function draw() {
    ctx.clearRect(0, 0, size, size);
    const a = action();
    if (drag && a) preview(a, cursor);
    else drawLayers();
    if (!a) return;
    mark(a.to, 12, showingHint ? '#fae297' : '#edf6f3');
    if (showingHint && !drag) {
      ctx.setLineDash([5, 6]);
      ctx.beginPath();
      ctx.moveTo(a.from.x, a.from.y);
      ctx.lineTo(a.to.x, a.to.y);
      ctx.stroke();
      ctx.setLineDash([]);
    }
    mark(drag ? cursor : a.from, 9, '#41ac95');
  }

  function apply() {
    phase = 'applied';
    if (step().result) {
      scene = step().result;
      draw();
    } else {
      canvas.hidden = true;
      photo.hidden = false;
      image(step().image);
    }
    get('caption').textContent = step().title;
    status.textContent = 'Step complete.';
    access.hidden = hint.hidden = true;
    next.hidden = false;
    next.textContent = move === model().steps.length - 1 ? 'Finish tutorial' : 'Next step';
    next.focus();
  }

  function completeDrag() {
    part++;
    if (!action()) { apply(); return; }
    status.textContent = 'Fold the next marked corner or flap.';
    draw();
  }

  async function render(focus = false) {
    const request = ++revision;
    phase = 'loading';
    part = 0;
    showingHint = false;
    drag = null;
    photo.hidden = canvas.hidden = next.hidden = hint.hidden = access.hidden = true;
    get('progress').textContent = 'Step ' + move + ' of ' + (model().steps.length - 1);
    get('goal').textContent = model().name;
    get('tutorial').hidden = !model().url;
    if (model().url) get('tutorial').href = model().url;
    get('setup').textContent = model().steps[0].text;
    get('instruction').textContent = step().text;
    previous.disabled = move === 1;
    previous.textContent = 'Previous step';
    get('caption').textContent = step().title;
    status.textContent = 'Preparing the paperâ€¦';
    try {
      const prepared = await readScene();
      if (request !== revision) return;
      scene = prepared;
    } catch {
      if (request !== revision) return;
      status.textContent = 'The paper could not load. Try restarting the tutorial.';
      return;
    }
    phase = 'fold';
    canvas.hidden = access.hidden = false;
    hint.hidden = !action();
    access.textContent = action() ? 'Apply fold without dragging' : step().title;
    status.textContent = action() ? 'Drag the green corner or flap to the outlined target.' : 'Use the button to turn, open, or check the paper.';
    draw();
    if (focus) (action() ? canvas : access).focus();
  }

  function position(event) {
    const bounds = canvas.getBoundingClientRect();
    return {x: (event.clientX - bounds.left) * size / bounds.width, y: (event.clientY - bounds.top) * size / bounds.height};
  }

  canvas.addEventListener('pointerdown', event => {
    if (phase !== 'fold' || drag || !action() || event.button !== 0) return;
    const p = position(event);
    if (distance(p, action().from) > 23) return;
    event.preventDefault();
    drag = {id: event.pointerId, start: p};
    cursor = action().from;
    canvas.setPointerCapture(event.pointerId);
    draw();
  });
  function track(event) {
    const p = position(event), from = action().from;
    return {x: from.x + p.x - drag.start.x, y: from.y + p.y - drag.start.y};
  }
  canvas.addEventListener('pointermove', event => {
    if (drag?.id !== event.pointerId) return;
    cursor = track(event);
    draw();
  });
  canvas.addEventListener('pointerup', event => {
    if (drag?.id !== event.pointerId) return;
    const drop = track(event);
    const tolerance = Math.min(25, distance(action().from, action().to) * 0.43);
    drag = null;
    if (distance(drop, action().to) <= tolerance) completeDrag();
    else {
      status.textContent = 'The fold did not line up. Drag the green marker into the target ring and release.';
      draw();
    }
  });
  function cancel(event) {
    if (drag?.id !== event.pointerId) return;
    drag = null;
    draw();
  }
  canvas.addEventListener('pointercancel', cancel);
  canvas.addEventListener('lostpointercapture', cancel);

  access.addEventListener('click', () => {
    if (phase !== 'fold') return;
    if (action()) completeDrag();
    else apply();
  });
  hint.addEventListener('click', () => {
    showingHint = true;
    status.textContent = action() ? 'Follow the dotted guide from the green marker to the outlined target.' : step().text;
    draw();
  });
  function restart() {
    move = 1;
    render(true);
  }
  previous.addEventListener('click', () => {
    if (move > 1 && phase !== 'finished') move--;
    render(true);
  });
  next.addEventListener('click', () => {
    if (phase === 'finished') {
      picker.scrollIntoView({block: 'center'});
      picker.querySelector('[aria-pressed="true"]').focus();
    } else if (move === model().steps.length - 1) {
      phase = 'finished';
      if (model().finish) image(model().finish);
      get('caption').textContent = model().name + ' complete!';
      status.textContent = 'You reached the end of this tutorial. Repeat a step or choose another model.';
      previous.disabled = false;
      previous.textContent = 'Repeat final step';
      next.textContent = 'Choose another model';
    } else {
      move++;
      render(true);
    }
  });

  function selectModel(index, focus) {
    level = index;
    move = 1;
    for (const [i, button] of [...picker.querySelectorAll('button')].entries()) {
      button.setAttribute('aria-pressed', String(i === index));
    }
    if (focus) history.replaceState(null, '', '#' + modelId(model()));
    render();
    if (focus) get('goal').focus();
  }

  try {
    const [original, extra] = await Promise.all([
      load('/content/fold-quest.json').then(response => response.json()),
      load('/content/interactive-folds.json').then(response => response.json())
    ]);
    levels = [...extra, ...original];
    for (const [index, item] of levels.entries()) {
      const button = document.createElement('button');
      const name = document.createElement('strong');
      const count = document.createElement('small');
      name.textContent = item.name;
      count.textContent = (item.steps.length - 1) + ' steps';
      button.type = 'button';
      button.append(name, count);
      button.addEventListener('click', () => selectModel(index, true));
      picker.append(button);
    }
    get('reset').addEventListener('click', restart);
    const initial = levels.findIndex(item => '#' + modelId(item) === location.hash);
    selectModel(Math.max(initial, 0), false);
  } catch {
    status.textContent = 'The tutorials could not load. Reload the page to try again.';
    access.hidden = hint.hidden = get('reset').hidden = previous.hidden = true;
  }
  panel.hidden = false;
})();
