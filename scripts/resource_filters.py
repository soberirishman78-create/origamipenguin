"""Add progressive grade/subject controls without rebuilding printable PDFs."""
import json,re
from pathlib import Path

def enhance_resources(page,items):
    if 'id="resource-filters"' in page['body']:return page
    ordered=[s for subject in ['Math','English'] for s in items if s['subject']==subject]
    iterator=iter(ordered)
    def card(match):
        item=next(iterator)
        low,high=item['grades'].replace('K','0').split('-')
        grades=' '.join(str(n) for n in range(int(low),int(high)+1))
        return '<article class="resource-card" data-grades="'+grades+'" data-subject="'+item['subject'].lower()+'">'
    body=re.sub(r'<article class="resource-card">',card,page['body'])
    controls='<form class="resource-filters" id="resource-filters" hidden aria-label="Filter printable resources"><div><label for="resource-grade">Grade level</label><select id="resource-grade" name="grade"><option value="all">All grades</option><option value="0">Kindergarten</option>'+''.join('<option value="'+str(n)+'">Grade '+str(n)+'</option>' for n in range(1,7))+'</select></div><div><label for="resource-subject">Subject</label><select id="resource-subject" name="subject"><option value="all">All subjects</option><option value="math">Math</option><option value="english">English &amp; writing</option></select></div><button type="reset">Reset filters</button><p id="resource-filter-count" role="status" aria-live="polite">19 of 19 sheets</p><p class="resource-filter-help">Choose both filters to narrow the list. Grade matches include every grade in a sheet\'s suggested range.</p></form><p id="resource-filter-empty" hidden>No sheets match these filters. Try another grade or subject, or reset the filters.</p>'
    body=body.replace('<nav class="resource-jumps"',controls+'<nav class="resource-jumps"')
    body=body.replace('<section id="math">','<section class="resource-subject" id="math">').replace('<section id="english">','<section class="resource-subject" id="english">')
    page['body']=body
    page['scripts']=['js/resource-filters.js?v=1']
    page['styles']+=' .resource-filters[hidden],.resource-card[hidden],.resource-subject[hidden],.resource-jumps[hidden]{display:none}.resource-filters{display:flex;flex-wrap:wrap;gap:16px;align-items:end;padding:22px;background:#fff;border:1px solid #ccd8d6;border-radius:10px;margin:24px 0}.resource-filters>div{flex:1;min-width:180px}.resource-filters label{display:block;font-weight:700;margin-bottom:7px;color:#18394a}.resource-filters select{width:100%;padding:11px 12px;border:1px solid #6f8581;border-radius:6px;background:white;font:inherit;color:#18394a;min-height:46px}.resource-filters button{min-height:46px;border:1px solid #35645f;border-radius:6px;background:#edf3ef;padding:10px 16px;font:600 1rem system-ui;color:#18394a;cursor:pointer}.resource-filters p{flex-basis:100%;margin:0}.resource-filter-help{font-size:.85rem;color:#52615e}.resource-filters :focus-visible{outline:3px solid #a55936;outline-offset:3px}@media(max-width:540px){.resource-filters>div{flex-basis:100%;min-width:0}}'
    return page

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    path=root/'content/pages/free-resources.json'
    page=enhance_resources(json.loads(path.read_text(encoding='utf-8')),json.loads((root/'content/free-resources.json').read_text()))
    path.write_text(json.dumps(page,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
