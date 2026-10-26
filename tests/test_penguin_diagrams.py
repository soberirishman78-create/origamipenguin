import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from penguin_diagrams import construction,HEAD
from heart_geometry import area,reflect

class PenguinDiagramTests(unittest.TestCase):
    def test_flat_landmarks(self):
        pairs=[(reflect((1,0),1,-.5,.5),(.2,.4)),
               (reflect((-1,0),-1,-.5,.5),(-.2,.4)),
               (reflect((2/3,1/3),1,0,.4),(2/15,1/3)),
               (reflect((0,1),0,1,.6),(0,.2)),
               (reflect((0,-1),1,1,HEAD),(.35,HEAD))]
        for actual,expected in pairs:
            for a,b in zip(actual,expected):self.assertAlmostEqual(a,b)

    def test_paper_area_and_profile_orientation(self):
        states=construction()
        for state in states:self.assertAlmostEqual(sum(area(p) for p,_ in state),2)
        for state in states[9:]:
            for poly,_ in state:
                for x,y in poly:self.assertGreaterEqual(x,-1e-9)
        # This is planar accounting; no assertion of physical outside-wrap validity.

    def test_diagrams_current_and_unverified(self):
        d=json.loads((ROOT/'content/tutorials/penguin.json').read_text(encoding='utf-8'))
        self.assertEqual(d['review']['status'],'needs-review')
        self.assertEqual(len(d['steps']),14)
        self.assertIsNone(d['diagram'])
        for n,s in enumerate(d['steps'],1):
            self.assertEqual(s['image']['src'],f'images/penguin/step-{n:02d}.svg')
            self.assertTrue((ROOT/s['image']['src']).is_file())
        subprocess.run([sys.executable,str(ROOT/'scripts/penguin_diagrams.py'),'--check'],check=True)

if __name__=='__main__':unittest.main()
