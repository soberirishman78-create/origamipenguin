"""Original flat-fold construction and SVG diagrams; no third-party assets.

Coordinates are in half-diagonals of the starting square, with y downward.
Layers are ordered bottom to top. This is ideal zero-thickness geometry,
not a physical folding simulation or evidence of beginner usability.
"""
from pathlib import Path
from html import escape
import copy
import sys

ROOT = Path(__file__).resolve().parents[1]
EPS = 1e-9
DIAMOND = [(0,-1),(1,0),(0,1),(-1,0)]

def area(poly):
    return abs(sum(x*v-u*y for (x,y),(u,v) in zip(poly,poly[1:]+poly[:1])))/2

def clip(poly,a,b,c,positive):
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        dp=a*p[0]+b*p[1]-c; dq=a*q[0]+b*q[1]-c
        pin=dp>=-EPS if positive else dp<=EPS
        qin=dq>=-EPS if positive else dq<=EPS
        if pin: out.append(p)
        if pin != qin:
            t=dp/(dp-dq); out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return out if len(out)>=3 and area(out)>EPS else []

def reflect(p,a,b,c):
    d=(a*p[0]+b*p[1]-c)/(a*a+b*b)
    return p[0]-2*a*d,p[1]-2*b*d

def fold(layers,a,b,c,positive=True):
    fixed=[];moving=[]
    for poly,front in layers:
        stay=clip(poly,a,b,c,not positive); move=clip(poly,a,b,c,positive)
        if stay:fixed.append((stay,front))
        if move:moving.append(([reflect(p,a,b,c) for p in move],not front))
    return fixed+list(reversed(moving))

def flip(layers):
    return [([(-x,y) for x,y in poly],not front) for poly,front in reversed(layers)]

def construction():
    layers=[(DIAMOND,False)]; states=[copy.deepcopy(layers)]
    # First two instructions crease and reopen the square.
    states.extend([copy.deepcopy(layers),copy.deepcopy(layers)])
    for args in [(0,1,-.5,False),(0,1,.25,True),(1,1,.25,True),(-1,1,.25,True)]:
        layers=fold(layers,*args);states.append(layers)
    layers=flip(layers);states.append(layers)
    layers=fold(layers,1,0,.5);layers=fold(layers,1,0,-.5,False);states.append(layers)
    layers=fold(layers,0,1,-.625,False);states.append(layers)
    layers=flip(layers);states.append(layers)
    return states

LABELS=['Set the starting orientation','Make the vertical centre crease','Make the horizontal centre crease','Bring the top tip to the centre','Bring the bottom tip to the new top edge','Lift the right half','Lift the left half','Turn the model over','Fold the side tips inward','Fold both top tips down','Turn to the front']
LINES={2:[((0,-1),(0,1))],3:[((-1,0),(1,0))],4:[((-.5,-.5),(.5,-.5))],5:[((-.75,.25),(.75,.25))],6:[((0,.25),(.625,-.375))],7:[((0,.25),(-.625,-.375))],9:[((-.5,-.5),(-.5,-.25)),((.5,-.5),(.5,-.25))],10:[((-.375,-.625),(-.125,-.625)),((.125,-.625),(.375,-.625))]}
ARROWS={2:[((-1,0),(1,0))],3:[((0,1),(0,-1))],4:[((0,-1),(0,0))],5:[((0,1),(0,-.5))],6:[((.75,.25),(0,-.5))],7:[((-.75,.25),(0,-.5))],9:[((-.625,-.375),(-.375,-.375)),((.625,-.375),(.375,-.375))],10:[((-.25,-.75),(-.25,-.5)),((.25,-.75),(.25,-.5))]}

def diagram(n,states):
    before=states[max(0,n-2)]; after=states[n-1]
    def pt(p,cx):return f'{cx+110*p[0]:.3f},{190+110*p[1]:.3f}'
    title=f'Heart step {n}: {LABELS[n-1]}'
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Original mathematical diagram. Left: before; right: after. Pink is the coloured face, white the reverse. Blue dashed lines are folds; arrows show moving corners. Paper thickness is omitted.</desc>', '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#164e8a"/></marker></defs><rect width="640" height="360" fill="white"/>']
    for cx,state,label in [(160,before,'Before'),(480,after,'After')]:
        out.append(f'<text x="{cx}" y="35" text-anchor="middle" font-family="sans-serif" font-size="25" fill="#18283b">{label}</text>')
        for poly,front in state:
            out.append(f'<polygon points="{" ".join(pt(p,cx) for p in poly)}" fill="{"#e898b1" if front else "#fff"}" stroke="#263244" stroke-width="1.6" stroke-linejoin="round"/>')
    references={3:[((0,-1),(0,1))],4:[((0,-1),(0,1)),((-1,0),(1,0))],5:[((0,-.5),(0,1))],6:[((0,-.5),(0,.25))],7:[((0,-.5),(0,.25))]}
    for p,q in references.get(n,[]):
        out.append(f'<path d="M{pt(p,160)} L{pt(q,160)}" fill="none" stroke="#5c6776" stroke-width="1.8" stroke-dasharray="3 4"/>')
    for p,q in LINES.get(n,[]):out.append(f'<path d="M{pt(p,160)} L{pt(q,160)}" fill="none" stroke="#164e8a" stroke-width="2.4" stroke-dasharray="7 5"/>')
    for p,q in ARROWS.get(n,[]):out.append(f'<path d="M{pt(p,160)} Q{pt(((p[0]+q[0])/2+.15,(p[1]+q[1])/2-.12),160)} {pt(q,160)}" fill="none" stroke="#164e8a" stroke-width="2.6" marker-end="url(#arrow)"/>')
    if n in [2,3]:
        p,q=LINES[n][0];out.append(f'<path d="M{pt(p,480)} L{pt(q,480)}" stroke="#5c6776" stroke-width="1.8" stroke-dasharray="3 4"/>')
    if n==3:out.append(f'<path d="M{pt((0,-1),480)} L{pt((0,1),480)}" stroke="#5c6776" stroke-width="1.8" stroke-dasharray="3 4"/>')
    if n in [4,5]:out.append(f'<path d="M{pt((0,-.5),480)} L{pt((0,.25 if n==5 else 1),480)}" stroke="#5c6776" stroke-width="1.8" stroke-dasharray="3 4"/>')
    bottom='Turn over left to right; keep bottom tip down' if n in [8,11] else 'Fold, then reopen completely' if n in [2,3] else 'Keep the page orientation; do not rotate the paper'
    out.append(f'<text x="320" y="337" text-anchor="middle" font-family="sans-serif" font-size="19" fill="#18283b">{bottom}</text></svg>')
    return ''.join(out)

def main():
    target=ROOT/'images/heart';states=construction();changed=[]
    if '--check' not in sys.argv:target.mkdir(exist_ok=True)
    for n in range(1,12):
        p=target/f'step-{n:02d}.svg';content=diagram(n,states)
        if not p.exists() or p.read_text(encoding='utf-8')!=content:
            changed.append(p.name)
            if '--check' not in sys.argv:p.write_text(content,encoding='utf-8',newline='\n')
    if '--check' in sys.argv and changed:raise SystemExit('Stale heart diagrams: '+', '.join(changed))
    print('Verified' if '--check' in sys.argv else 'Generated',11,'heart diagrams')

if __name__=='__main__':main()
