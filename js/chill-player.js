(()=>{
  const panel=document.querySelector('#chill-player');if(!panel)return;
  const frame=document.querySelector('#chill-player-frame'),heading=document.querySelector('#chill-player-title'),status=document.querySelector('#chill-player-status'),stop=document.querySelector('#chill-player-stop'),start=document.querySelector('#chill-player-start'),external=document.querySelector('#chill-player-external');
  const links=[...document.querySelectorAll('.chill-play')],cards=[...document.querySelectorAll('.video-card')];
  let listening=false;
  const allowed=new Set(links.map(link=>link.dataset.video));
  function select(id,name,shuffledQueue){
    if(!allowed.has(id)||!/^[A-Za-z0-9_-]{11}$/.test(id))return;
    const order=[...allowed],index=order.indexOf(id);
    const queue=shuffledQueue||order.slice(index).concat(order.slice(0,index));
    const iframe=document.createElement('iframe');
    iframe.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&playsinline=1&rel=0&loop=1&playlist='+queue.join(',');
    iframe.title='Relaxation Station continuous playlist, starting with '+name;iframe.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';
    listening=true;frame.replaceChildren(iframe);heading.textContent=shuffledQueue?'Shuffle listening':'Continuous listening';external.href='https://www.youtube.com/watch?v='+id;
    status.textContent=(shuffledQueue?'Shuffled order. Starting with ':'Starting with ')+name+'. The next video plays automatically, and the collection repeats. Use the player controls to pause or skip. Site navigation opens below while your video keeps playing.';stop.hidden=false;
    links.forEach(link=>{if(link.dataset.video===id)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
    cards.forEach(card=>card.classList.toggle('is-selected',card.querySelector('.chill-play').dataset.video===id));
    panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});heading.focus({preventScroll:true});
  }
  links.forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;event.preventDefault();select(link.dataset.video,link.dataset.name);}));
  start.addEventListener('click',()=>select(start.dataset.video,start.dataset.name));
  stop.addEventListener('click',()=>{listening=false;frame.replaceChildren(start);heading.textContent='Pick a soundscape and settle in.';status.textContent='Video stopped. Choose a video whenever you are ready.';stop.hidden=true;links.forEach(link=>link.removeAttribute('aria-current'));cards.forEach(card=>card.classList.remove('is-selected'));start.focus();});
  document.querySelector('#chill-player-shuffle').addEventListener('click',()=>{
    const queue=[...allowed];
    for(let i=queue.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[queue[i],queue[j]]=[queue[j],queue[i]];}
    const first=links.find(link=>link.dataset.video===queue[0]);
    if(first)select(first.dataset.video,first.dataset.name,queue);
  });
  const browse=document.createElement('section');browse.className='chill-browse';browse.hidden=true;
  browse.innerHTML='<div class="chill-browse-bar"><p>Browse Origami Penguin while your soundscape keeps playing above.</p><button type="button">Back to Chill Corner</button></div><iframe title="Browse Origami Penguin" referrerpolicy="strict-origin-when-cross-origin"></iframe>';
  panel.after(browse);
  const siteFrame=browse.querySelector('iframe'),back=browse.querySelector('button');
  function returnToChill(){browse.hidden=true;document.body.classList.remove('chill-browsing');panel.scrollIntoView({block:'start'});back.blur();heading.focus({preventScroll:true});}
  back.addEventListener('click',returnToChill);
  function route(event){
    const link=event.target.closest('a[href]');
    if(!listening||!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||link.hasAttribute('download')||link.target&&link.target!=='_self')return;
    const destination=new URL(link.href,location.href);
    if(destination.origin!==location.origin||!/^https?:$/.test(destination.protocol))return;
    if(destination.pathname===location.pathname&&destination.hash)return;
    if(/^\/chill-corner(?:\.html)?\/?$/.test(destination.pathname)){if(!browse.hidden){event.preventDefault();returnToChill();}return;}
    event.preventDefault();siteFrame.src=destination.href;browse.hidden=false;document.body.classList.add('chill-browsing');panel.scrollIntoView({block:'start'});
  }
  document.addEventListener('click',route);
  siteFrame.addEventListener('load',()=>{
    try{siteFrame.contentDocument.addEventListener('click',event=>{
      const link=event.target.closest('a[href]');if(!link||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
      const destination=new URL(link.href);if(destination.origin===location.origin&&/^\/chill-corner(?:\.html)?\/?$/.test(destination.pathname)){event.preventDefault();returnToChill();}
    });}catch(error){/* External destinations keep their normal browser behavior. */}
  });
  panel.hidden=false;
})();
