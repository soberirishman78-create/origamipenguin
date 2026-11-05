(()=>{
  if(location.hostname!=='origamipenguin.com'||navigator.doNotTrack==='1'||navigator.globalPrivacyControl===true)return;
  function record(event,target){
    fetch('/api/events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({event,target}),keepalive:true,credentials:'omit'}).catch(()=>{});
  }
  record('page_view',location.pathname.replace(/\.html$/,'').replace(/\/$/,'')||'/');
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');if(!link)return;
    const url=new URL(link.href,location.href);
    if(url.origin===location.origin&&url.pathname.startsWith('/resources/')&&url.pathname.endsWith('.pdf'))record(link.hasAttribute('download')?'resource_download':'resource_preview',url.pathname);
    else if(link.closest('.book-card')&&/(^|\.)amazon\.com$/.test(url.hostname)){const asin=url.pathname.match(/\/dp\/([A-Z0-9]{10})(?:\/|$)/);if(asin)record('book_click',asin[1]);}
  });
  document.addEventListener('opp:video-select',event=>{if(typeof event.detail?.id==='string')record('video_select',event.detail.id);});
})();
