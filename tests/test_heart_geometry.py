import sys,json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from heart_geometry import construction,reflect,area

class HeartGeometryTests(unittest.TestCase):
    def test_landmark_reflections(self):
        for point,line,target in [((0,-1),(0,1,-.5),(0,0)),((0,1),(0,1,.25),(0,-.5)),((.75,.25),(1,1,.25),(0,-.5)),((1,0),(1,1,.25),(.25,-.75)),((-.75,.25),(-1,1,.25),(0,-.5)),((.625,-.375),(1,0,.5),(.375,-.375)),((.25,-.75),(0,1,-.625),(.25,-.5))]:
            self.assertEqual(reflect(point,*line),target)
    def test_no_paper_lost_and_final_bounds(self):
        states=construction()
        self.assertEqual(len(states),11)
        for state in states:self.assertAlmostEqual(sum(area(p) for p,_ in state),2)
        for p,_ in states[-1]:
            for x,y in p:
                self.assertLessEqual(abs(x),.5+1e-9)
                self.assertGreaterEqual(y,-.625-1e-9)
                self.assertLessEqual(y,.25+1e-9)
    def test_images_match_steps_and_generator(self):
        t=json.loads((ROOT/'content/tutorials/heart.json').read_text(encoding='utf-8'))
        self.assertEqual(t['review']['status'],'needs-review')
        self.assertEqual(len(t['steps']),11)
        for n,step in enumerate(t['steps'],1):
            self.assertEqual(step['image']['src'],f'images/heart/step-{n:02d}.svg')
            self.assertTrue((ROOT/step['image']['src']).is_file())
        subprocess.run([sys.executable,'scripts/heart_geometry.py','--check'],cwd=ROOT,check=True)
