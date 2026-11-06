(() => {
  const panel = document.querySelector('#math-practice');
  const get = id => document.querySelector('#practice-' + id);
  const topic = get('topic');
  const answer = get('answer');
  const feedback = get('feedback');
  let index = 0;
  let questions = [];
  let solved = 0;
  let finished = false;
  const fractions = [[1,2,2],[1,3,3],[2,3,2],[3,4,2],[2,5,3],[3,5,2],[4,5,2],[1,4,3]];
  const multiplication = [[3,4],[6,7],[8,4],[9,6],[12,3],[7,8],[4,9],[11,5]];
  function render() {
    const [a,b,k] = questions[index];
    const fraction = topic.value === 'fractions';
    get('progress').textContent = 'Question ' + (index + 1) + ' of 5';
    get('question').textContent = fraction ? a + '/' + b + ' = ?/' + b*k : a + ' × ' + b + ' = ?';
    answer.value = '';
    get('form').hidden = false;
    answer.disabled = finished = false;
    get('form').querySelector('button').disabled = false;
    get('hint').hidden = get('reveal').hidden = false;
    get('next').hidden = get('restart').hidden = true;
    feedback.textContent = '';
  }
  function start() {
    const pool = [...(topic.value === 'fractions' ? fractions : multiplication)];
    questions = Array.from({length:5}, () => pool.splice(Math.floor(Math.random()*pool.length),1)[0]);
    index = solved = 0;
    render();
  }
  function resolve(correct) {
    if (finished) return;
    const [a,b,k] = questions[index];
    finished = answer.disabled = get('form').querySelector('button').disabled = true;
    if (correct) solved++;
    feedback.textContent = (correct ? 'Correct. ' : '') + (k ? 'Multiply both parts by ' + k + '. ' + a + '/' + b + ' = ' + a*k + '/' + b*k + '.' : a + ' groups of ' + b + ' make ' + a*b + '.');
    get('hint').hidden = get('reveal').hidden = true;
    get('next').hidden = false;
    get('next').textContent = index === 4 ? 'See results' : 'Next question';
    get('next').focus();
  }
  get('form').addEventListener('submit', event => {
    event.preventDefault();
    const [a,b,k] = questions[index];
    if (Number(answer.value) === a*(k || b)) resolve(true);
    else feedback.textContent = 'Try again, or use the hint.';
  });
  get('hint').addEventListener('click', () => {
    const [a,b,k] = questions[index];
    feedback.textContent = k ? 'What do you multiply ' + b + ' by to get ' + b*k + '? Multiply the numerator by the same number.' : 'Think of ' + a + ' equal groups, each with ' + b + ' items.';
  });
  get('reveal').addEventListener('click', () => resolve(false));
  get('next').addEventListener('click', () => {
    if (++index < 5) {render();answer.focus();return;}
    get('form').hidden = get('next').hidden = true;
    feedback.textContent = 'Round complete. You solved ' + solved + ' of 5 before revealing the answer.';
    get('restart').hidden = false;
    get('restart').focus();
  });
  get('restart').addEventListener('click', () => {start();answer.focus();});
  topic.addEventListener('change', start);
  if (new URLSearchParams(location.search).get('topic') === 'multiplication') topic.value = 'multiplication';
  start();
  panel.hidden = false;
})();
