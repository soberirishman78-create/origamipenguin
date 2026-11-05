(()=>{
  const panel=document.querySelector('#chill-player');if(!panel)return;
  const frame=document.querySelector('#chill-player-frame'),heading=document.querySelector('#chill-player-title'),status=document.querySelector('#chill-player-status'),stop=document.querySelector('#chill-player-stop'),start=document.querySelector('#chill-player-start'),external=document.querySelector('#chill-player-external');
  const links=[...document.querySelectorAll('.chill-play')],cards=[...document.querySelectorAll('.video-card')];
  const records=cards.map(card=>({card,id:card.querySelector('.chill-play').dataset.video,name:card.querySelector('.chill-play').dataset.name,seconds:Number(card.dataset.seconds),format:card.dataset.format,sound:card.dataset.sound,text:card.textContent.toLowerCase()}));
  const form=document.querySelector('#chill-filters'),query=form.querySelector('#chill-query'),format=form.querySelector('#chill-format'),duration=form.querySelector('#chill-duration'),sound=form.querySelector('#chill-sound');
  const shuffleFiltered=document.querySelector('#chill-shuffle-filtered');
  let player=null,generation=0,apiPromise;
  const previousButton=document.querySelector('#chill-previous'),nextButton=document.querySelector('#chill-next');
  function youtubeAPI(){
    if(window.YT?.Player)return Promise.resolve(window.YT);
    if(!apiPromise)apiPromise=new Promise((resolve,reject)=>{
      const earlier=window.onYouTubeIframeAPIReady;
      const timer=setTimeout(()=>reject(new Error('YouTube API unavailable')),15000);
      window.onYouTubeIframeAPIReady=()=>{clearTimeout(timer);if(typeof earlier==='function')earlier();resolve(window.YT);};
      const script=document.createElement('script');script.src='https://www.youtube.com/iframe_api';script.onerror=()=>{clearTimeout(timer);reject(new Error('YouTube API unavailable'));};document.head.append(script);
    });
    return apiPromise;
  }
  function visible(){return records.filter(r=>!r.card.hidden);}
  function update(){
    const terms=query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    for(const r of records){const minutes=Math.round(r.seconds/60);const type=format.value==='all'||(format.value==='short'?r.format==='short':r.format!=='short'&&r.seconds>=1200);const length=duration.value==='all'||(duration.value==='short'?minutes<20:duration.value==='medium'?minutes>=20&&minutes<=120:minutes>120);r.card.hidden=!(type&&length&&(sound.value==='all'||sound.value===r.sound)&&terms.every(t=>r.text.includes(t)));}
    document.querySelectorAll('.video-group').forEach(group=>{group.hidden=![...group.querySelectorAll('.video-card')].some(c=>!c.hidden);});
    const total=visible().length;document.querySelector('#chill-count').textContent=total+' of '+records.length+' videos';document.querySelector('#chill-empty').hidden=total!==0;shuffleFiltered.disabled=total===0;
  }
  function play(queue,shuffled=false){
    if(!queue.length)return;
    const token=++generation;if(player){player.destroy();player=null;}
    const manual=queue.some(r=>r.format==='short');
    previousButton.hidden=nextButton.hidden=!manual||queue.length<2;
    previousButton.disabled=nextButton.disabled=true;
    const first=queue[0],id=first.id,name=first.name;
    const iframe=document.createElement('iframe');
    iframe.id='chill-youtube-frame';
    iframe.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&playsinline=1&rel=0'+(manual?'&enablejsapi=1&origin='+encodeURIComponent(location.origin):'&loop=1&playlist='+queue.map(r=>r.id).join(','));
    iframe.title='Relaxation Station playlist, starting with '+name;iframe.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';
    frame.replaceChildren(iframe);heading.textContent=shuffled?'Shuffle listening':'Continuous listening';external.href='https://www.youtube.com/watch?v='+id;
    status.textContent=(shuffled?'Shuffled order. ':'')+'Starting with '+name+'. '+queue.length+' videos queued. The next plays automatically and the queue repeats. Changing filters only changes your next selection.';stop.hidden=false;
    links.forEach(link=>{if(link.dataset.video===id)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
    cards.forEach(card=>card.classList.toggle('is-selected',card.querySelector('.chill-play').dataset.video===id));
    if(manual)youtubeAPI().then(YT=>{
      if(token!==generation)return;
      let index=0,failures=0;
      const advance=step=>{if(token!==generation||!player)return;index=(index+step+queue.length)%queue.length;const next=queue[index];status.textContent='Now playing '+next.name+'. '+queue.length+' videos in this repeating queue.';iframe.title='Relaxation Station: '+next.name;player.loadVideoById(next.id);};
      player=new YT.Player(iframe,{events:{onReady:event=>{if(token!==generation)return;previousButton.disabled=nextButton.disabled=false;previousButton.onclick=()=>advance(-1);nextButton.onclick=()=>advance(1);event.target.playVideo();},onStateChange:event=>{if(token!==generation)return;if(event.data===1)failures=0;if(event.data===0)advance(1);},onError:()=>{if(token!==generation)return;if(++failures<queue.length)advance(1);else status.textContent='These videos could not be played. Try another video or open it on YouTube.';}}});
    }).catch(()=>{if(token===generation)status.textContent='The video can play, but the automatic queue could not connect. Try another selection or open it on YouTube.';});
    document.dispatchEvent(new CustomEvent('opp:video-select',{detail:{id}}));
    panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});heading.focus({preventScroll:true});
  }
  function select(id){
    const selected=records.find(r=>r.id===id);if(!selected)return;
    let queue=visible().filter(r=>selected.format==='short'?r.format==='short':selected.seconds>=1200?r.format!=='short'&&r.seconds>=1200:r.id===id);
    if(!queue.some(r=>r.id===id))queue=[selected];
    const index=queue.findIndex(r=>r.id===id);play(queue.slice(index).concat(queue.slice(0,index)));
  }
  function shuffle(queue){queue=[...queue];for(let i=queue.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[queue[i],queue[j]]=[queue[j],queue[i]];}play(queue,true);}
  links.forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;event.preventDefault();select(link.dataset.video);}));
  start.addEventListener('click',()=>select(start.dataset.video));
  stop.addEventListener('click',()=>{++generation;if(player){player.destroy();player=null;}previousButton.hidden=nextButton.hidden=true;frame.replaceChildren(start);heading.textContent='Pick a soundscape and settle in.';status.textContent='Video stopped. Choose a video whenever you are ready.';stop.hidden=true;links.forEach(link=>link.removeAttribute('aria-current'));cards.forEach(card=>card.classList.remove('is-selected'));start.focus();});
  document.querySelector('#chill-player-shuffle').addEventListener('click',()=>shuffle(records.filter(r=>r.format!=='short'&&r.seconds>=1200)));
  document.querySelector('#chill-shuffle-shorts').addEventListener('click',()=>shuffle(records.filter(r=>r.format==='short')));
  shuffleFiltered.addEventListener('click',()=>shuffle(visible()));
  form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('change',update);query.addEventListener('input',update);
  form.addEventListener('reset',()=>{query.value='';format.value='all';duration.value='all';sound.value='all';update();});
  const choices=document.querySelector('.chill-choices');if(choices)choices.hidden=true;
  form.hidden=false;panel.hidden=false;update();
})();
