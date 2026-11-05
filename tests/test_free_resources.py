import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class FreeResourceTests(unittest.TestCase):
    def test_complete_printable_library(self):
        items=json.loads((ROOT/'content/free-resources.json').read_text())
        self.assertEqual(len(items),19)
        self.assertEqual(len({i['slug'] for i in items}),19)
        page=(ROOT/'free-resources.html').read_text(encoding='utf-8')
        self.assertEqual(page.count('class="resource-card"'),19)
        for item in items:
            pdf=ROOT/'resources'/(item['slug']+'.pdf')
            self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'))
            self.assertTrue((ROOT/'images/resources'/(item['slug']+'.jpg')).is_file())
            self.assertIn('/resources/'+pdf.name,page)
        self.assertIn('/resources/opp-reference-sheets-complete.pdf',page)
        self.assertTrue((ROOT/'resources/opp-reference-sheets-complete.pdf').is_file())

    def test_navigation_and_homepage_discovery(self):
        for page in ROOT.glob('*.html'):
            if page.name in {'deadwood.html','matrix.html','cats.html','dogs.html','math.html'} or page.name.startswith('google'):continue
            self.assertIn('href="/free-resources"',page.read_text(encoding='utf-8'),page.name)
        self.assertIn('Start with something free',(ROOT/'index.html').read_text(encoding='utf-8'))
