(async () => {
  const panel = document.querySelector('#fold-quest');
  const get = name => document.querySelector('#fold-' + name);
  const choices = get('choices');
  const paper = get('paper');
  const status = get('status');
  const next = get('continue');
  const hint = get('hint');
  let levels;
  try {
    const response = await fetch('/content/fold-quest.json');
    if (!response.ok) throw new Error('Fold data unavailable');
    levels = await response.json();
  } catch {
    status.textContent = 'The folds could not load. Reload the page to try again, or open the paper tutorial below.';
    hint.hidden = get('reset').hidden = true;
    panel.hidden = false;
    return;
  }
  let level = 0;
  let move = 1;
  let phase = 'choose';
  let correctFirst = 0;
  let tried = false;
  let drag = null;
  const model = () => levels[level];
  const step = () => model().steps[move];
  function image(data) {
    const sheet = get('image');
    sheet.src = '/' + data.src;
    sheet.alt = data.alt;
    sheet.width = data.width;
    sheet.height = data.height;
  }
  function shuffle(items) {
    for (let i = items.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    return items;
  }
  function render() {
    phase = 'choose';
    tried = false;
    drag = null;
    next.hidden = true;
    hint.hidden = false;
    choices.replaceChildren();
    get('progress').textContent = 'Level ' + (level + 1) + ' of ' + levels.length + ' · Move ' + move + ' of ' + (model().steps.length - 1);
    get('goal').textContent = 'Fold a ' + model().name.toLowerCase();
    get('tutorial').href = model().url;
    get('caption').textContent = 'Tap a move, or drag it onto the paper.';
    image(model().steps[move - 1].image);
    const alternatives = [...new Set(model().steps.map(s => s.title))].filter(title => title !== step().title);
    const options = shuffle([step().title, ...shuffle(alternatives).slice(0, 2)]);
    for (const title of options) {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = title;
      button.draggable = true;
      button.addEventListener('click', () => apply(title));
      button.addEventListener('dragstart', event => {
        drag = title;
        event.dataTransfer.setData('text/plain', title);
        event.dataTransfer.effectAllowed = 'move';
        paper.classList.add('is-target');
      });
      button.addEventListener('dragend', () => {
        drag = null;
        paper.classList.remove('is-target');
      });
      choices.append(button);
    }
    status.textContent = 'Which move comes next? Use the hint whenever you like.';
  }
  function apply(title) {
    if (phase !== 'choose') return;
    if (title !== step().title) {
      tried = true;
      status.textContent = 'That move comes at a different point. Try another move or ask for a hint.';
      return;
    }
    if (!tried) correctFirst++;
    phase = 'applied';
    image(step().image);
    get('caption').textContent = step().title;
    status.textContent = step().text;
    choices.replaceChildren();
    hint.hidden = true;
    next.hidden = false;
    next.textContent = move === model().steps.length - 1 ? 'Finish level' : 'Next move';
    next.focus();
  }
  function finish() {
    phase = 'finished';
    image(model().finish || step().image);
    get('caption').textContent = model().name + ' complete!';
    const last = level === levels.length - 1;
    status.textContent = last ? 'All three levels complete! You chose ' + correctFirst + ' moves correctly on the first try without a hint.' : 'You folded a ' + model().name.toLowerCase() + '! The next level starts with a fresh sheet.';
    next.textContent = last ? 'Play again' : 'Next level';
    next.focus();
  }
  function restart() {
    level = 0;
    move = 1;
    correctFirst = 0;
    render();
    get('goal').focus();
  }
  hint.addEventListener('click', () => {
    tried = true;
    status.textContent = step().text;
  });
  next.addEventListener('click', () => {
    if (phase === 'finished') {
      if (level === levels.length - 1) restart();
      else { level++; move = 1; render(); get('goal').focus(); }
    } else if (move === model().steps.length - 1) {
      finish();
    } else {
      move++;
      render();
      choices.querySelector('button').focus();
    }
  });
  paper.addEventListener('dragover', event => { if (drag) event.preventDefault(); });
  paper.addEventListener('drop', event => {
    if (!drag) return;
    event.preventDefault();
    const title = drag;
    drag = null;
    paper.classList.remove('is-target');
    apply(title);
  });
  get('reset').addEventListener('click', restart);
  render();
  panel.hidden = false;
})();

