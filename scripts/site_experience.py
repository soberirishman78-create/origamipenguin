"""Progressive discovery features layered onto the static site."""
from html import escape as e
import json,re

TOPICS={
 'numbers-0-20':('number-sense','Number sense'),'place-value':('number-sense','Number sense'),
 'addition-subtraction':('addition','Addition & subtraction'),
 'multiplication-chart':('multiplication','Multiplication & division'),'division-steps':('multiplication','Multiplication & division'),
 'fraction-decimal-percent':('fractions','Fractions & decimals'),'fraction-steps':('fractions','Fractions & decimals'),'decimals-operations':('fractions','Fractions & decimals'),
 'measurement-conversions':('measurement','Measurement, time & money'),'time-and-money':('measurement','Measurement, time & money'),
 'shapes-area-perimeter':('geometry','Shapes & geometry'),'word-problem-steps':('problem-solving','Problem solving'),
 'nouns':('grammar','Grammar'),'verbs':('grammar','Grammar'),'adjectives-adverbs':('grammar','Grammar'),'pronouns':('grammar','Grammar'),'sentences-punctuation':('grammar','Grammar'),
 'writing-checklist':('writing','Writing'),'connecting-ideas':('writing','Writing')}

CSS='''
.explore-hero{padding:36px 0}.explore-kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;font-weight:700;color:#456a62}.explore-hero h1{font:600 clamp(2.2rem,5vw,3.3rem)/1.08 Georgia,serif;max-width:850px;color:#18394a;margin:12px 0 20px}.explore-hero>p{font-size:1.1rem;max-width:700px}.explore-actions{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:24px 0}.explore-paths{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin:12px 0 40px}.explore-paths>a{background:#fff;border:1px solid #c9d8d3;border-radius:12px;padding:22px 16px;text-decoration:none;color:#18394a}.explore-paths strong{font:600 1.6rem Georgia,serif;display:block;margin-bottom:12px}.explore-paths span{font-size:.9rem;line-height:1.6;display:block}.explore-feature{padding:30px;background:#edf3ef;border-radius:12px;margin:24px 0}.explore-feature h2{margin-top:0}.explore-pair{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:25px 0}.explore-pair>section{background:white;border:1px solid #d3dfdb;border-radius:12px;padding:24px}.related-experience{margin:28px 0;padding:22px;background:#edf3ef;border-radius:10px}.related-experience h2{font:600 1.3rem Georgia,serif;margin:0 0 12px}.related-experience ul{padding-left:20px}.resource-related{font-size:.88rem;border-top:1px solid #dbe3df;padding-top:12px}.starter-packs{margin:22px 0;background:#edf3ef;border-radius:10px;padding:20px}.starter-packs summary{font-size:1.2rem;font-weight:700;cursor:pointer}.pack-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}.pack-grid a{display:block;padding:16px;background:white;border:1px solid #b8cbc3;border-radius:8px}.pack-grid small{display:block;margin-top:7px;color:#415e55}.resource-filters input,.chill-filters input,.chill-filters select{width:100%;min-height:46px;padding:10px 12px;font:inherit;border:1px solid #758d85;border-radius:6px;background:white;color:#18394a}.resource-filters .resource-search-field{flex-basis:100%}.chill-filters{padding:20px;border:1px solid #ccd8d6;background:#fff;border-radius:10px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px;margin:24px 0}.chill-filters[hidden],.video-card[hidden],.video-group[hidden]{display:none!important}.chill-filters label{display:block;font-weight:700;margin-bottom:7px}.chill-filters .chill-search,.chill-filters p{grid-column:1/-1;margin:0}.chill-filters button{padding:10px 16px;background:#edf3ef;border:1px solid #35645f;border-radius:6px;cursor:pointer;font:inherit;min-height:44px}.chill-player-buttons{flex-wrap:wrap}.chill-player-actions{align-items:flex-start;flex-wrap:wrap}.chill-player-actions>p{flex-basis:100%}.chill-player-buttons button[disabled]{opacity:.55;cursor:not-allowed}.games-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.games-grid article{padding:24px;border:1px solid #ccd8d6;background:white;border-radius:12px}.newsletter-invite{padding:24px;border:1px solid #ccd8d6;border-radius:12px;background:#f8f4ed;margin:30px 0}.newsletter-invite h2{margin-top:0}@media(max-width:900px){.explore-paths{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:600px){.explore-paths{grid-template-columns:repeat(2,minmax(0,1fr))}.explore-pair,.games-grid{grid-template-columns:1fr}.explore-feature{padding:22px}.chill-filters{grid-template-columns:1fr}.chill-filters>*{grid-column:1}.explore-hero{padding:15px 0}}
'''

def home():
 return '''<section class="explore-hero"><p class="explore-kicker">Origami Penguin · Stories, learning &amp; creative breaks</p><h1>A curious mind has more than one way to play.</h1><p>Find a story to get lost in, a helpful page for learning, a fold to try, or a quieter place to spend a little time. Welcome to everything we’re making at Origami Penguin.</p><div class="explore-actions"><a class="btn" href="/free-resources">Start with something free</a><a href="/books">Find your next read →</a></div></section>
<nav class="explore-paths" aria-label="Choose your path"><a href="/books"><strong>Read</strong><span>Mysteries, adventures, and notes from the creative life.</span></a><a href="/free-resources"><strong>Learn</strong><span>Free K-6 references, grade packs, and educational books.</span></a><a href="/tutorials"><strong>Create</strong><span>Make your next fold with illustrated origami tutorials.</span></a><a href="/chill-corner"><strong>Relax</strong><span>Rain, forests, music, and a soundscape for your day.</span></a><a href="/games"><strong>Play</strong><span>Meet zombies, defend a couch, or take a dog for a run.</span></a></nav>
<section class="explore-feature"><p class="explore-kicker">For parents, teachers &amp; growing minds</p><h2>A little reminder can make the next step easier.</h2><p>Explore 19 free one-page reference sheets, with grade, subject, and topic filters. Or grab a grade-level pack with a simple parent and teacher guide.</p><div class="explore-actions"><a class="btn" href="/free-resources">Find a reference sheet</a><a href="/free-resources#starter-packs">Choose a grade pack</a></div><p><a href="/textbooks">Explore the educational bookshelf →</a></p></section>
<div class="explore-pair"><section><h2>Stories with a little mystery.</h2><p>Follow the Kelly Brothers Mysteries, discover the Skybridge Trilogy, and explore more fiction by Jeremy Kelly.</p><p><a class="btn" href="/books">Browse the fiction collection</a></p><p><a href="/coloring-puzzles">Coloring &amp; puzzles</a> · <a href="/journals">Journals &amp; logbooks</a> · <a href="/nonfiction">Practical nonfiction</a></p></section><section><h2>The Creative Notebook</h2><p>52 notes from writing books, making educational resources, publishing, and building this creative home. Start anywhere that sounds familiar.</p><a class="btn" href="/blog">Read a note</a></section></div>
<section class="explore-feature"><h2>Still here for the folds.</h2><p>Origami remains part of our story. Start with paper and a few careful creases, then make a heart, crane, or penguin.</p><div class="explore-actions"><a href="/guide" class="btn">Start with the basics</a><a href="/tutorials">All illustrated tutorials</a><a href="/origami-for-teachers">Fold in the classroom</a></div><p><a href="/heart-tutorial">Fold a heart</a> · <a href="/crane-tutorial">Fold a crane</a> · <a href="/penguin-tutorial">Fold a penguin</a></p><p><a href="/supplies">Paper, books, and supplies</a> · <a href="/origami-paper-for-classrooms">Plan a classroom set</a></p></section>
<div class="explore-pair"><section><h2>Your quieter corner.</h2><p>Choose a long listening session, try a short pause, or shuffle a collection of rain, forest, music, and space videos.</p><a class="btn" href="/chill-corner">Visit Chill Corner</a></section><section><h2>A small adventure between projects.</h2><p>Play our browser games, including Deadwood, Cats vs. Dogs, Dog Runner, and Shardkeeper.</p><a class="btn" href="/games">Explore the games</a></section></div>'''

def resources(body,root):
 items=json.loads((root/'content/free-resources.json').read_text(encoding='utf-8'))
 ordered=[i for sub in ['Math','English'] for i in items if i['subject']==sub]
 it=iter(ordered)
 def card(m):
  item=next(it);topic,label=TOPICS[item['slug']]
  return m.group(0)[:-1]+' data-topic="'+topic+'" data-search="'+e(item['title']+' '+item['intro']+' '+label+' '+('times tables multiply multiplication' if topic=='multiplication' else ''))+'">'
 body=re.sub(r'<article class="resource-card"[^>]*>',card,body)
 fields='<div class="resource-search-field"><label for="resource-query">Search reference sheets</label><input id="resource-query" name="q" type="search" placeholder="Try fractions, nouns, money…" autocomplete="off"></div>'
 body=body.replace('<div><label for="resource-grade">',fields+'<div><label for="resource-grade">',1)
 topics=dict(TOPICS.values())
 topicselect='<div><label for="resource-topic">Topic</label><select id="resource-topic"><option value="all">All topics</option>'+''.join('<option value="'+k+'">'+e(v)+'</option>' for k,v in topics.items())+'</select></div>'
 body=body.replace('<button type="reset">Reset filters',topicselect+'<button type="reset">Reset filters')
 body=body.replace('Choose both filters to narrow the list.', 'Search and combine grade, subject, and topic filters.')
 packs=json.loads((root/'content/resource-packs.json').read_text(encoding='utf-8'))
 block='<details class="starter-packs" id="starter-packs"><summary>Grade-level starter packs</summary><p>Each pack starts with a one-page parent and teacher guide, followed by the references whose suggested grade ranges include that grade. Print only the pages you need.</p><div class="pack-grid">'+''.join('<a href="'+p['url']+'" download>'+e(p['title'])+'<small>'+str(len(p['sheets']))+' reference sheets + guide · '+str(p['pages'])+' pages</small></a>' for p in packs)+'</div><p><a href="/resources/packs/start-here-guide.pdf" target="_blank" rel="noopener">Preview the parent and teacher guide</a></p></details>'
 body=body.replace('<nav class="resource-jumps"',block+'<nav class="resource-jumps"',1)
 # Place context links inside each card, beside the existing printable actions.
 matches=list(re.finditer(r'(<article class="resource-card".*?</article>)',body))
 for m,item in reversed(list(zip(matches,ordered))):
  if item['subject']=='Math':links='<a href="/textbooks?search=math">Explore math learning books</a> · <a href="/origami-for-teachers">Try a folding activity</a>'
  else:links='<a href="/textbooks?search=language">Explore language learning books</a> · <a href="/books">Find a story to read</a>'
  extra='<p class="resource-related">'+links+'</p>'
  old=m.group(0);new=old.replace('</div></article>',extra+'</div></article>')
  body=body[:m.start()]+new+body[m.end():]
 return body

def duration(value):
 m=re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',value)
 if not m:return 0
 h,mi,s=[int(x or 0) for x in m.groups()];return h*3600+mi*60+s

def chill(body,root):
 videos={v['id']:v for v in json.loads((root/'content/relaxation-videos.json').read_text(encoding='utf-8'))}
 def card(m):
  raw=m.group(0);vid=re.search(r'data-video="([\w-]+)"',raw)[1];v=videos[vid];title=v['title'].lower()
  fmt='short' if v.get('format')=='short' else 'video'
  music=any(w in title for w in ['piano','harp','music','drums','schubert','tones','drone','fractal','aurora','northern lights','528 hz','space']) and 'no music' not in title
  sound='music' if music else 'nature'
  if 'welcome to' in title:sound='intro'
  return raw.replace('class="video-card"','class="video-card" data-seconds="'+str(duration(v['duration']))+'" data-format="'+fmt+'" data-sound="'+sound+'"',1)
 body=re.sub(r'<article class="video-card">.*?</article>',card,body)
 filters='''<form class="chill-filters" id="chill-filters" hidden aria-label="Find a video"><div class="chill-search"><label for="chill-query">Find your soundscape</label><input type="search" id="chill-query" placeholder="Try rain, piano, forest…"></div><div><label for="chill-format">Video type</label><select id="chill-format"><option value="all">All videos</option><option value="long">Long sessions (20+ min)</option><option value="short">Shorts</option></select></div><div><label for="chill-duration">Duration</label><select id="chill-duration"><option value="all">Any duration</option><option value="short">Under 20 minutes</option><option value="medium">20 minutes–2 hours</option><option value="long">Over 2 hours</option></select></div><div><label for="chill-sound">Sound</label><select id="chill-sound"><option value="all">All sounds</option><option value="nature">Nature sounds &amp; noise</option><option value="music">Music &amp; ambient tones</option></select></div><button type="reset">Reset video filters</button><p id="chill-count" role="status" aria-live="polite">83 videos</p><p>Filters choose the next queue; they do not interrupt a video already playing. Mixed soundscapes appear with music when they include instruments or tones.</p></form><p id="chill-empty" hidden>No matching videos. Try another filter or reset the list.</p>'''
 body=body.replace('<div class="chill-choices"',filters+'<div class="chill-choices"',1)
 body=body.replace('id="chill-player-shuffle">Shuffle &amp; play','id="chill-player-shuffle">Shuffle long sessions')
 body=body.replace('<button type="button" id="chill-player-stop"','<button type="button" id="chill-shuffle-shorts">Shuffle Shorts</button><button type="button" id="chill-shuffle-filtered">Shuffle filtered videos</button><button type="button" id="chill-player-stop"')
 body=body.replace('<button type="button" id="chill-player-stop"','<button type="button" id="chill-previous" hidden>Previous in queue</button><button type="button" id="chill-next" hidden>Next in queue</button><button type="button" id="chill-player-stop"')
 return body

def related(name,body,p):
 if p.get('kind')=='journal':
  category=p.get('body','')
  if any(t in name for t in ['translation','answer','lesson','resource','page-needs','instructions','bundles']):links=[('/free-resources','Find a free classroom reference'),('/textbooks','Explore educational books')]
  elif any(t in name for t in ['sound','loop','thumbnail','quiet']):links=[('/chill-corner','Choose a background soundscape'),('/blog','Explore more creative notes')]
  else:links=[('/books','Explore the fiction collection'),('/free-resources?topic=writing','Try a writing checklist')]
 elif name=='origami-for-teachers.html':links=[('/free-resources?topic=fractions','Free fraction reference sheets'),('/free-resources?topic=geometry','Free shape and area reminders')]
 elif name=='textbooks.html':links=[('/free-resources','Try a free printable reference'),('/free-resources#starter-packs','Choose a grade starter pack')]
 elif name=='books.html':links=[('/free-resources?topic=writing','Print a writing reminder'),('/chill-corner','Pick a reading soundscape')]
 else:return body
 return body+'<aside class="related-experience"><h2>Keep exploring</h2><ul>'+''.join('<li><a href="'+url+'">'+text+'</a></li>' for url,text in links)+'</ul></aside>'

def enhance(name,body,p,root):
 if name=='index.html':
  body=home()+'<section class="explore-feature"><h2>What’s new</h2><ul><li><a href="/fractions-with-paper">New lesson: Fractions with Paper Folding</a></li><li><a href="/practice">New five-minute math practice</a></li><li><a href="/kelly-brothers-reading-order">New Kelly Brothers reading guide</a></li><li><a href="/free-resources#starter-packs">Printable grade packs</a></li><li><a href="/chill-corner#rain">Featured listening: Distant Forest Drums &amp; Gentle Rain</a></li></ul></section>'
 if name=='books.html':
  body='<aside class="related-experience"><h2>Start a series</h2><p><a href="/kelly-brothers-reading-order">Kelly Brothers reading order</a> · <a href="/skybridge-reading-order">Skybridge reading order</a></p></aside>'+body
 if name=='origami-for-teachers.html':
  body+='<aside class="related-experience"><h2>Ready-to-teach fraction lesson</h2><a href="/fractions-with-paper">Fractions with Paper Folding</a></aside>'
 if name=='free-resources.html':
  body='<aside class="related-experience"><h2>Try five-minute practice</h2><p><a href="/practice?topic=fractions">Practice equivalent fractions</a> · <a href="/practice?topic=multiplication">Practice multiplication</a> · <a href="/fractions-with-paper">Paper-folding lesson</a></p></aside>'+body
 if name=='free-resources.html':body=resources(body,root)
 if name=='chill-corner.html':body=chill(body,root)
 body=related(name,body,p)
 newsletter=json.loads((root/'content/newsletter.json').read_text(encoding='utf-8'))
 if newsletter.get('signupUrl') and not newsletter['signupUrl'].startswith('https://'):raise ValueError('Newsletter signup URL must be public HTTPS')
 if newsletter.get('signupUrl') and name in ['index.html','free-resources.html','blog.html']:
  body+='<section class="newsletter-invite"><h2>A little good news, once a month.</h2><p>New free sheets, book news, and a quiet corner to explore. Optional updates for adults, with an unsubscribe link in every email. Downloads remain free without subscribing.</p><a class="btn" href="'+e(newsletter['signupUrl'])+'" target="_blank" rel="noopener">Get monthly updates</a><p><a href="/privacy">How we handle your information</a></p></section>'
 return body
