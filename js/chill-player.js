(()=>{
  const panel=document.querySelector('#chill-player');if(!panel)return;
  const frame=document.querySelector('#chill-player-frame'),heading=document.querySelector('#chill-player-title'),status=document.querySelector('#chill-player-status'),stop=document.querySelector('#chill-player-stop'),start=document.querySelector('#chill-player-start'),external=document.querySelector('#chill-player-external');
  const links=[...document.querySelectorAll('.chill-play')],cards=[...document.querySelectorAll('.video-card')];
  const allowed=new Set(links.map(link=>link.dataset.video));
  function select(id,name){
    if(!allowed.has(id)||!/^[A-Za-z0-9_-]{11}$/.test(id))return;
    const order=[...allowed],index=order.indexOf(id);
    const queue=order.slice(index).concat(order.slice(0,index));
    const iframe=document.createElement('iframe');
    iframe.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&playsinline=1&rel=0&loop=1&playlist='+queue.join(',');
    iframe.title='Relaxation Station continuous playlist, starting with '+name;iframe.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';
    frame.replaceChildren(iframe);heading.textContent='Continuous listening';external.href='https://www.youtube.com/watch?v='+id;
    status.textContent='Starting with '+name+'. The next video plays automatically, and the collection repeats. Use the player controls to pause or skip.';stop.hidden=false;
    links.forEach(link=>{if(link.dataset.video===id)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
    cards.forEach(card=>card.classList.toggle('is-selected',card.querySelector('.chill-play').dataset.video===id));
    panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});heading.focus({preventScroll:true});
  }
  links.forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;event.preventDefault();select(link.dataset.video,link.dataset.name);}));
  start.addEventListener('click',()=>select(start.dataset.video,start.dataset.name));
  stop.addEventListener('click',()=>{frame.replaceChildren(start);heading.textContent='Pick a soundscape and settle in.';status.textContent='Video stopped. Choose a video whenever you are ready.';stop.hidden=true;links.forEach(link=>link.removeAttribute('aria-current'));cards.forEach(card=>card.classList.remove('is-selected'));start.focus();});
  panel.hidden=false;
})();
