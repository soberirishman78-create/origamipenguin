(()=>{
  const form=document.querySelector('#resource-filters');if(!form)return;
  const grade=form.querySelector('#resource-grade'),subject=form.querySelector('#resource-subject'),topic=form.querySelector('#resource-topic'),query=form.querySelector('#resource-query');
  const cards=[...document.querySelectorAll('.resource-card')],groups=[...document.querySelectorAll('.resource-subject')];
  const count=document.querySelector('#resource-filter-count'),empty=document.querySelector('#resource-filter-empty');
  const normalize=s=>s.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
  function update(sync=true){
    const terms=normalize(query.value).trim().split(/\s+/).filter(Boolean);let visible=0;
    cards.forEach(card=>{
      const match=(grade.value==='all'||card.dataset.grades.split(' ').includes(grade.value))&&(subject.value==='all'||card.dataset.subject===subject.value)&&(topic.value==='all'||card.dataset.topic===topic.value)&&terms.every(term=>normalize(card.dataset.search).includes(term));
      card.hidden=!match;if(match)visible++;
    });
    groups.forEach(group=>{group.hidden=![...group.querySelectorAll('.resource-card')].some(card=>!card.hidden);});
    count.textContent=visible+' of '+cards.length+' sheets';empty.hidden=visible!==0;
    if(sync){const url=new URL(location.href);for(const [key,value] of [['grade',grade.value],['subject',subject.value],['topic',topic.value],['q',query.value.trim()]]){if(value&&value!=='all')url.searchParams.set(key,value);else url.searchParams.delete(key);}history.replaceState(null,'',url);}
  }
  const params=new URLSearchParams(location.search);
  for(const [key,select] of [['grade',grade],['subject',subject],['topic',topic]]){const value=params.get(key);if([...select.options].some(o=>o.value===value))select.value=value;}
  query.value=(params.get('q')||'').slice(0,120);
  form.addEventListener('submit',event=>event.preventDefault());form.addEventListener('change',()=>update());query.addEventListener('input',()=>update());
  form.addEventListener('reset',()=>{grade.value='all';subject.value='all';topic.value='all';query.value='';update();});
  const jumps=document.querySelector('.resource-jumps');if(jumps)jumps.hidden=true;
  form.hidden=false;update(false);
  if(location.hash==='#starter-packs'){const packs=document.querySelector('#starter-packs');if(packs)packs.open=true;}
})();
