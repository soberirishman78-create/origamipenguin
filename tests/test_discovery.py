from pathlib import Path
import json,subprocess,unittest
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]

class DiscoveryTests(unittest.TestCase):
    def test_counter_contract(self):
        subprocess.run(['node','--experimental-default-type=module','tests/metrics.test.mjs'],cwd=ROOT,check=True,capture_output=True)

    def test_resource_topics_and_packs(self):
        text=(ROOT/'free-resources.html').read_text(encoding='utf-8')
        self.assertIn('id="resource-query"',text);self.assertIn('id="resource-topic"',text)
        self.assertEqual(text.count('data-search='),19)
        packs=json.loads((ROOT/'content/resource-packs.json').read_text())
        self.assertEqual([p['grade'] for p in packs],list(range(7)))
        for p in packs:
            self.assertTrue((ROOT/p['url'].lstrip('/')).is_file())
            self.assertEqual(p['pages'],len(p['sheets'])+1)
            self.assertIn(p['url'],text)

    def test_discovery_and_private_counters(self):
        home=(ROOT/'index.html').read_text(encoding='utf-8')
        for label in ['Read','Learn','Create','Relax','Play']:self.assertIn('<strong>'+label+'</strong>',home)
        chill=(ROOT/'chill-corner.html').read_text(encoding='utf-8')
        self.assertEqual(chill.count('data-format="short"'),37)
        self.assertEqual(chill.count('data-seconds='),83)
        for key in ['chill-format','chill-duration','chill-sound','chill-shuffle-shorts','chill-shuffle-filtered']:self.assertIn('id="'+key+'"',chill)
        routes=json.loads((ROOT/'_routes.json').read_text());self.assertEqual(routes['include'],['/api/events'])
        self.assertIsNone(json.loads((ROOT/'content/newsletter.json').read_text())['signupUrl'])
