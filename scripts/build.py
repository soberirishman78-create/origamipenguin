#!/usr/bin/env python3
"""Build checked-in static pages. Python standard library only; no runtime build needed."""
from pathlib import Path
from html import escape
from string import Template
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://origamipenguin.com'
NAV = [('home', '/', 'Home'), ('tutorials', '/tutorials.html', 'Tutorials'), ('guide', '/guide.html', "Beginner’s Guide"), ('teachers', '/origami-for-teachers.html', 'For Teachers'), ('supplies', '/supplies.html', 'Supplies'), ('blog', '/blog.html', 'Articles'), ('about', '/about.html', 'About')]

def canonicalize(text):
    # Cloudflare Pages serves extensionless pages and redirects .html requests.
    text=text.replace(ORIGIN + '/index.html', ORIGIN + '/')
    return re.sub(r'(https://origamipenguin\.com/[a-z0-9-]+)\.html', r'\1', text)

def esc(value):
    return escape(str(value), quote=True)

def url(slug):
    return ORIGIN + ('/' if slug == 'index.html' else '/' + slug.removesuffix('.html'))

def ld(value):
    return '<script type="application/ld+json">' + canonicalize(json.dumps(value, ensure_ascii=False)).replace('<', '\\u003c') + '</script>'

def links(items):
    return '<ul>' + ''.join(f'<li><a href="{esc(i["url"])}">{esc(i["title"])}</a></li>' for i in items) + '</ul>'

def crumbs(items):
    return '<p class="breadcrumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">›</span> '.join(f'<a href="{esc(i["url"])}">{esc(i["name"])}</a>' if i.get('url') else esc(i['name']) for i in items) + '</p>'

def tutorial_body(t):
    body = crumbs([{'name':'Home','url':'/'},{'name':'Tutorials','url':'/tutorials.html'},{'name':t['heading']}])
    body += f'<h1>{esc(t["heading"])}</h1><p class="intro">{esc(t["introduction"])}</p>'
    body += f'<dl class="project-facts"><div><dt>Difficulty</dt><dd>{esc(t["difficulty"])}</dd></div><div><dt>Allow about</dt><dd>{t["durationMinutes"]} minutes</dd></div><div><dt>Recommended paper</dt><dd>{esc(t["paper"])}</dd></div></dl><p class="small">{esc(t["durationNote"])}</p>'
    body += '<div class="tutorial-actions"><a class="btn" href="#instructions">Jump to instructions</a><a href="#print-guide">Print / save as PDF</a></div>'
    body += '<h2>Materials</h2><ul>' + ''.join(f'<li>{esc(i)}</li>' for i in t['materials']) + '</ul><p>No scissors or glue needed. New to folding? <a href="/guide.html">Read the beginner’s guide</a>.</p>'
    for key in ['finishedImage','diagram']:
        image=t.get(key)
        if image:
            body += f'<figure class="diagram-section"><img src="/{esc(image["src"])}" alt="{esc(image["alt"])}" width="{int(image["width"])}" height="{int(image["height"])}" decoding="async"><figcaption>{esc(image["alt"])}</figcaption></figure>'
    body += '<h2 id="instructions">Step-by-step instructions</h2><ol class="steps">'
    for n, step in enumerate(t['steps'],1):
        body += f'<li class="step" id="step-{n}"><h3>{esc(step["title"])}</h3><p>{esc(step["text"])}</p>'
        if step.get('image'):
            image=step['image']; body += f'<img src="/{esc(image["src"])}" alt="{esc(image["alt"])}" width="{int(image["width"])}" height="{int(image["height"])}" loading="lazy" decoding="async">'
        body += '</li>'
    body += '</ol>'
    for heading,key in [('Helpful folding tips','tips'),('If a fold goes wrong','commonMistakes')]:
        body += f'<h2>{heading}</h2><ul>'+''.join(f'<li>{esc(i)}</li>' for i in t.get(key,[]))+'</ul>'
    body += '<aside class="print-guide" id="print-guide"><h2>Print these instructions</h2><p>Use your browser’s Print command (Ctrl+P on Windows, Command+P on Mac), then choose a printer or “Save as PDF.” Navigation and shopping suggestions are hidden in the printed version. No signup required.</p></aside>'
    if t.get('printableUrl'): body += f'<p><a href="{esc(t["printableUrl"])}">Download printable instructions</a></p>'
    if t.get('videoUrl'): body += f'<p><a href="{esc(t["videoUrl"])}">Watch the folding video</a></p>'
    body += '<section class="related"><h2>What to fold next</h2>'+links(t.get('relatedProjects',[]))+'<h2>Paper for this project</h2>'+links(t.get('supplyRecommendations',[]))+'<h2>For the classroom</h2>'+links(t.get('educationalConnections',[]))+'</section>'
    return body

def normalize_body(body):
    # Root-relative links also work when a missing URL is several levels deep.
    body=re.sub(r'(href|src)="(?!https?:|mailto:|#|/)([^"]+)"',r'\1="/\2"',body)
    body=body.replace('href="/index.html"','href="/"')
    body=re.sub(r'(<a[^>]+class="btn"[^>]*?) style="[^"]*"',r'\1',body)
    return re.sub(r'(href="/[a-z0-9-]+)\.html(?=["#])',r'\1',body)

def build():
    pages=json.loads((ROOT/'content/site.json').read_text())
    for f in sorted((ROOT/'content/pages').glob('*.json')):
        pages.append(json.loads(f.read_text()))
    template=Template((ROOT/'templates/page.html').read_text())
    outputs={}
    for p in pages:
        schemas=p.get('schema',[])
        name=p['slug']
        source=ROOT/'content/tutorials'/name.replace('-tutorial.html','.json')
        if name.endswith('-tutorial.html') and source.exists():
            t=json.loads(source.read_text())
            legacy={'penguin-tutorial.html','heart-tutorial.html','crane-tutorial.html'}
            if name not in legacy and t.get('review',{}).get('status')!='fold-tested':
                raise ValueError('New tutorials require a recorded fold-tested review: '+name)
            body=tutorial_body(t)
            # Keep schema aligned with visible instructions; do not invent ratings/results.
            howto={'@context':'https://schema.org','@type':'HowTo','name':t['heading'],'description':p['description'],'totalTime':f'PT{t["durationMinutes"]}M','supply':[{'@type':'HowToSupply','name':t['paper']}],'step':[{'@type':'HowToStep','name':i['title'],'text':i['text'],'url':url(name)+f'#step-{n}'} for n,i in enumerate(t['steps'],1)]}
            if t.get('finishedImage'):howto['image']=ORIGIN+'/'+t['finishedImage']['src']
            schemas=[s for s in schemas if s.get('@type')!='HowTo']+[howto]
        elif 'body' in p:
            body=crumbs(p.get('breadcrumbs',[]))+f'<h1>{esc(p["heading"])}</h1>'+p['body']
            schemas=[{'@context':'https://schema.org','@type':'Article','headline':p['heading'],'description':p['description'],'mainEntityOfPage':url(name),'author':{'@type':'Organization','name':'Origami Penguin','url':ORIGIN+'/'}}]
            if p.get('breadcrumbs'):
                schemas.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':n,'name':i['name'],**({'item':ORIGIN+'/'+i['url'].lstrip('/')} if i.get('url') else {})} for n,i in enumerate(p['breadcrumbs'],1)]})
        else: body=(ROOT/'content/legacy'/name).read_text()
        nav=''.join(f'<a href="{href}"'+(' aria-current="page"' if (name=='index.html' and key=='home') or '/'+name==href else '')+(' class="nav-section"' if p.get('nav')==key else '')+f'>{label}</a>' for key,href,label in NAV)
        output=template.substitute(title=esc(p['title']),description=esc(p['description']),robots='<meta name="robots" content="noindex, follow">' if p.get('noindex') else '',canonical=f'<link rel="canonical" href="{url(name)}">' if name!='404.html' else '',url=url(name),image=esc(p.get('image',ORIGIN+'/images/og-default.png')),og_type='website' if name in ['index.html','tutorials.html','supplies.html','blog.html'] else 'article',styles='<style>'+p['styles']+'</style>' if p.get('styles') else '',schema='\n'.join(ld(s) for s in schemas),navigation=nav,body=normalize_body(body),scripts='\n'.join('<script src="/'+esc(s)+'" defer></script>' for s in p.get('scripts',[])))
        outputs[name]=re.sub(r'(href="/[a-z0-9-]+)\.html(?=["#])',r'\1',output)
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+esc(url(p['slug']))+'</loc></url>\n' for p in pages if not p.get('noindex'))+'</urlset>\n'
    outputs['sitemap.xml']=sitemap
    changed=[]
    for name,content in outputs.items():
        path=ROOT/name
        if not path.exists() or path.read_text()!=content:
            changed.append(name)
            if '--check' not in sys.argv:path.write_text(content)
    if '--check' in sys.argv and changed:
        print('Generated files need updating: '+', '.join(changed)); return 1
    print(('Verified' if '--check' in sys.argv else 'Built')+f' {len(pages)} pages and sitemap')
    return 0

if __name__=='__main__':sys.exit(build())
