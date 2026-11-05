(()=>{
  const form=document.querySelector('#resource-filters');if(!form)return;
  const grade=form.querySelector('#resource-grade'),subject=form.querySelector('#resource-subject');
  const cards=[...document.querySelectorAll('.resource-card')],groups=[...document.querySelectorAll('.resource-subject')];
  const count=document.querySelector('#resource-filter-count'),empty=document.querySelector('#resource-filter-empty');
  function update(){
    let visible=0;
    cards.forEach(card=>{
      const match=(grade.value==='all'||card.dataset.grades.split(' ').includes(grade.value))&&(subject.value==='all'||card.dataset.subject===subject.value);
      card.hidden=!match;if(match)visible++;
    });
    groups.forEach(group=>{group.hidden=![...group.querySelectorAll('.resource-card')].some(card=>!card.hidden);});
    count.textContent=visible+' of '+cards.length+' sheets';empty.hidden=visible!==0;
  }
  form.addEventListener('submit',event=>event.preventDefault());
  form.addEventListener('change',update);
  form.addEventListener('reset',()=>{grade.value='all';subject.value='all';update();});
  const jumps=document.querySelector('.resource-jumps');if(jumps)jumps.hidden=true;
  form.hidden=false;update();
})();
