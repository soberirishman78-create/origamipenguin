from pathlib import Path
import json,re,unittest
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]

class JournalTests(unittest.TestCase):
    def test_complete_substantive_series(self):
        posts=json.loads((ROOT/'content/journal.json').read_text(encoding='utf-8'))
        self.assertEqual([p['number'] for p in posts],list(range(1,53)))
        self.assertEqual(len({p['slug'] for p in posts}),52)
        self.assertEqual(len({p['description'] for p in posts}),52)
        all_paragraphs=[]
        for p in posts:
            self.assertGreaterEqual(len(' '.join(p['paragraphs']).split()),200)
            self.assertGreaterEqual(len(p['paragraphs']),5)
            all_paragraphs+=p['paragraphs']
            text=(ROOT/(p['slug']+'.html')).read_text(encoding='utf-8')
            self.assertIn('"@type": "BlogPosting"',text)
            self.assertIn('"datePublished": "2026-11-04"',text)
            self.assertIn('Read one each week or explore the collection at your own pace.',text)
            self.assertIn(p['title'].replace('&','&amp;'),text)
        self.assertEqual(max(Counter(all_paragraphs).values()),1)

    def test_hub_and_reading_sequence(self):
        posts=json.loads((ROOT/'content/journal.json').read_text(encoding='utf-8'))
        hub=(ROOT/'blog.html').read_text(encoding='utf-8')
        self.assertEqual(hub.count('class="journal-card"'),52)
        for i,p in enumerate(posts):
            text=(ROOT/(p['slug']+'.html')).read_text(encoding='utf-8')
            self.assertIn('href="/'+p['slug']+'"',hub)
            if i:self.assertIn('href="/'+posts[i-1]['slug']+'"',text)
            if i<51:self.assertIn('href="/'+posts[i+1]['slug']+'"',text)
        for original in ['blog-folding-tips','blog-history','blog-best-paper','tutorials']:
            self.assertIn('href="/'+original+'"',hub)

    def test_chill_links_are_verified_channel_videos(self):
        videos=json.loads((ROOT/'content/relaxation-videos.json').read_text(encoding='utf-8'))
        self.assertEqual(len(videos),83)
        self.assertEqual(len({v['id'] for v in videos}),83)
        text=(ROOT/'chill-corner.html').read_text(encoding='utf-8')
        self.assertEqual(text.count('class="video-card"'),83)
        self.assertNotIn('<iframe',text)
        self.assertIn('id="chill-player"',text)
        self.assertEqual(text.count('class="chill-play"'),166)
        self.assertIn('/js/chill-player.js',text)
        self.assertNotIn('<video',text)
        for v in videos:
            self.assertEqual(v['channelId'],'UCnt0WRg-Cv8RdcRQ011L1DA')
            self.assertRegex(v['id'],r'^[A-Za-z0-9_-]{11}$')
            self.assertIn(v['url'],text)
        self.assertIn('@relaxationstationloops',text)
