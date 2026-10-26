import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from crane_diagrams import K,A,B,H,U,NARROW,narrowed
from heart_geometry import reflect,area

class CraneDiagramTests(unittest.TestCase):
    def test_precrease_and_reverse_landmarks(self):
        for actual,expected in [(reflect((1,0),1,K,K),H),
                                (reflect((-1,0),-1,K,K),H),
                                (reflect(B,0,1,-K),U),
                                (reflect(B,1,1+2**.5,-1),(-1,-1-K)),
                                (reflect(B,-1,1+2**.5,-1),(1,-1-K))]:
            for a,b in zip(actual,expected):self.assertAlmostEqual(a,b)
        self.assertAlmostEqual(A+(-K),1-2*K)

    def test_narrowing_conserves_selected_face_area(self):
        # This checks only the selected planar face, not a complete 3D bird base.
        from crane_diagrams import BIRD
        self.assertAlmostEqual(sum(area(p) for p,_ in narrowed()),area(BIRD))

    def test_draft_diagrams_current_and_review_gate_retained(self):
        data=json.loads((ROOT/'content/tutorials/crane.json').read_text(encoding='utf-8'))
        self.assertEqual(data['review']['status'],'needs-review')
        self.assertEqual(len(data['steps']),26)
        for n,s in enumerate(data['steps'],1):
            self.assertEqual(s['image']['src'],f'images/crane/step-{n:02d}.svg')
            self.assertTrue((ROOT/s['image']['src']).is_file())
        subprocess.run([sys.executable,str(ROOT/'scripts/crane_diagrams.py'),'--check'],check=True)

if __name__=='__main__':unittest.main()
