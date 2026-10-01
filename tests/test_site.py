"""Fast, dependency-free regression checks for the deployed static site."""
import collections
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import unittest
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://origamipenguin.com'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=[]; self.links=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a)
    def find(self,tag,**attrs):return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files={p.name:p.read_text(encoding='utf-8') for p in ROOT.glob('*.html') if not p.name.startswith('google')}
        cls.pages={n:Page(s) for n,s in cls.files.items()}
    def test_generated_pages_current(self):
        subprocess.run(['python','scripts/build.py','--check'],cwd=ROOT,check=True)
    def test_accessible_page_shell(self):
        for name,p in self.pages.items():
            with self.subTest(page=name):
                self.assertEqual(len(p.find('h1')),1)
                self.assertEqual(len(p.find('main',id='main')),1)
                self.assertTrue(p.find('a',href='#main'))
                self.assertTrue(p.find('nav',**{'aria-label':'Main navigation'}))
                self.assertEqual(len(p.ids),len(set(p.ids)))
                for image in p.find('img'):
                    for attr in ['alt','width','height']:self.assertIn(attr,image)
    def test_internal_links_and_fragments(self):
        for name,p in self.pages.items():
            for a in p.links:
                href=a['href']; u=urlsplit(href)
                if u.netloc and u.netloc!='origamipenguin.com':continue
                if u.scheme and u.scheme not in ['http','https']:continue
                path=u.path
                target=name if not path else 'index.html' if path=='/' else unquote(path.lstrip('/'))
                f=ROOT/target
                if not f.exists() and not Path(target).suffix:target+='.html';f=ROOT/target
                with self.subTest(page=name,link=href):
                    self.assertTrue(f.is_file(),href)
                    if u.fragment and target in self.pages:self.assertIn(u.fragment,self.pages[target].ids)
    def test_metadata_and_sitemap(self):
        sitemap=ET.fromstring((ROOT/'sitemap.xml').read_text(encoding='utf-8'))
        urls={node.text for node in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
        expected=set();titles=[];descriptions=[]
        for name,p in self.pages.items():
            if name=='404.html':self.assertTrue(p.find('meta',name='robots'));continue
            canonical=ORIGIN+('/' if name=='index.html' else '/'+name.removesuffix('.html'))
            self.assertEqual(p.find('link',rel='canonical')[0]['href'],canonical)
            desc=p.find('meta',name='description')[0]['content'];self.assertTrue(desc);descriptions.append(desc)
            self.assertEqual(p.find('meta',property='og:url')[0]['content'],canonical)
            self.assertTrue(p.find('meta',property='og:image'))
            titles.append(re.search(r'<title>(.*?)</title>',self.files[name]).group(1))
            if not any('noindex' in a.get('content','') for a in p.find('meta',name='robots')):expected.add(canonical)
        self.assertEqual(urls,expected)
        self.assertEqual(len(titles),len(set(titles)))
        self.assertEqual(len(descriptions),len(set(descriptions)))
    def test_structured_data_and_tutorials(self):
        for name,text in self.files.items():
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
                data=json.loads(raw);self.assertEqual(data['@context'],'https://schema.org')
                if data['@type']=='HowTo':
                    for n,step in enumerate(data['step'],1):
                        self.assertIn('step-'+str(n),self.pages[name].ids)
                        self.assertEqual(step['url'],ORIGIN+'/'+name.removesuffix('.html')+'#step-'+str(n))
    def test_unverified_penguin_has_visible_review_notice(self):
        text=self.files['penguin-tutorial.html']
        self.assertTrue(self.pages['penguin-tutorial.html'].find('h2',id='review-heading'))
        self.assertIn('We have not yet verified a corrected sequence by folding it.',text)
        schemas=[json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)]
        self.assertFalse(any(item['@type']=='HowTo' for item in schemas))
    def test_affiliate_tracking_preserved(self):
        # Baseline public URLs captured before any edits. No tag rewriting.
        expected=json.loads((ROOT/'tests/affiliate-baseline.json').read_text(encoding='utf-8'))
        current={}
        for name,p in self.pages.items():
            urls=[]
            for a in p.links:
                if urlsplit(a['href']).netloc in ['www.amazon.com','amazon.com','amzn.to']:
                    urls.append(a['href'])
                    if 'tag=' in a['href']:
                        self.assertIn('sponsored',a.get('rel','').split())
                        self.assertIn('nofollow',a.get('rel','').split())
                    if a.get('target')=='_blank':self.assertIn('noopener',a.get('rel','').split())
            if urls:current[name]=dict(collections.Counter(urls))
        self.assertEqual(current,expected)
    def test_assets_and_no_tracking_additions(self):
        for name,p in self.pages.items():
            for tag in ['script','img','link']:
                for a in p.find(tag):
                    v=a.get('src') if tag!='link' else a.get('href') if a.get('rel') in ['stylesheet','icon'] else None
                    if v and v.startswith('/'):self.assertTrue((ROOT/urlsplit(v).path.lstrip('/')).is_file())
        self.assertNotIn('@import',(ROOT/'style.css').read_text(encoding='utf-8'))
        headers=(ROOT/'_headers').read_text(encoding='utf-8')
        for directory in ['content','templates','scripts','tests','docs']:
            self.assertIn('/'+directory+'/*\n  X-Robots-Tag: noindex',headers)
        self.assertIn("var CLICK_ENDPOINT = '';",(ROOT/'js/outbound.js').read_text(encoding='utf-8'))
        self.assertEqual(json.loads((ROOT/'content/products.json').read_text(encoding='utf-8'))['pressBooks'],[])
        self.assertEqual(json.loads((ROOT/'content/products.json').read_text(encoding='utf-8'))['teacherResources'],[])

if __name__=='__main__':unittest.main()
