"""Original penguin flat-state geometry and labelled outside-reverse schematic.

The final cap projection gives landmarks, not a certified 3D wrap/layer model.
"""
from pathlib import Path
from html import escape
import json,sys,copy
from heart_geometry import DIAMOND,fold,flip,clip,reflect
ROOT=Path(__file__).resolve().parents[1]
HEAD=-.65

def mountain(layers,a,b,c,positive=True):
    fixed=[];moving=[]
    for poly,face in layers:
        p=clip(poly,a,b,c,not positive);q=clip(poly,a,b,c,positive)
        if p:fixed.append((p,face))
        if q:moving.append(([reflect(v,a,b,c) for v in q],not face))
    return list(reversed(moving))+fixed

def construction():
    p=[(DIAMOND,True)];states=[copy.deepcopy(p),copy.deepcopy(p)]
    p=flip(p);states.append(p)
    p=fold(p,1,-.5,.5);states.append(p)
    p=fold(p,-1,-.5,.5);states.append(p)
    p=flip(p);states.append(p)
    p=fold(p,1,0,.4);states.append(p)
    p=fold(p,1,0,-.4,False);states.append(p)
    p=fold(p,0,1,.6);states.append(p)
    p=mountain(p,1,0,0,False);states.append(p)
    states.extend([p,p]) # precrease/reopen and schematic neck opening
    # Project the closed outside-reversed cap. Hidden wrap ordering is omitted.
    p=fold(p,1,1,HEAD,False);states.append(p);states.append(p)
    return states

def diagram(n,step,states):
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420" role="img" aria-labelledby="title desc"><title id="title">Penguin step {n}: {escape(step["title"])}</title><desc id="desc">Original vector diagram. {escape(step["diagramNote"])} Dark is the coloured face and white the reverse. Outside-reverse opening is schematic.</desc><rect width="640" height="420" fill="white"/><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#2466a0" stroke="white" stroke-width=".7"/></marker></defs>']
    def point(p,cx,profile=False):
        return f'{cx+(170 if profile else 120)*(p[0]-(.2 if profile else 0)):.3f},{215+(170 if profile else 120)*p[1]:.3f}'
    def label(s,x,y,size=21):out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="#263244">{escape(s)}</text>')
    def polygon(p,cx,face,profile=False):out.append(f'<polygon points="{" ".join(point(v,cx,profile) for v in p)}" fill="{"#42566a" if face else "#ffffff"}" stroke="#172c42" stroke-width="1.6" stroke-linejoin="round"/>')
    def line(p,q,cx,dash='',profile=False,colour='#2466a0'):
        out.append(f'<path d="M{point(p,cx,profile)} L{point(q,cx,profile)}" fill="none" stroke="white" stroke-width="4.8" stroke-dasharray="{dash}"/>')
        out.append(f'<path d="M{point(p,cx,profile)} L{point(q,cx,profile)}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-dasharray="{dash}"/>')
    def arrow(p,q,cx,profile=False):
        mid=((p[0]+q[0])/2+.12,(p[1]+q[1])/2-.1)
        out.append(f'<path d="M{point(p,cx,profile)} Q{point(mid,cx,profile)} {point(q,cx,profile)}" fill="none" stroke="white" stroke-width="5.2"/>')
        out.append(f'<path d="M{point(p,cx,profile)} Q{point(mid,cx,profile)} {point(q,cx,profile)}" fill="none" stroke="#2466a0" stroke-width="2.6" marker-end="url(#arrow)"/>')
    label('Before',160,32,25);label('After / checkpoint',480,32,25)
    for cx,index in [(160,max(0,n-2)),(480,n-1)]:
        profile=index>=9
        for poly,face in states[index]:polygon(poly,cx,face,profile)
        if 1<=index<=8:line((0,-1),(0,.6 if index==8 else 1),cx,'3 4',colour='#778899')
    if n==2:
        line((0,-1),(0,1),160,'7 5');arrow((-1,0),(1,0),160)
    if n==4:
        line((0,-1),(2/3,1/3),160,'7 5');arrow((1,0),(.2,.4),160)
    if n==5:
        line((0,-1),(-2/3,1/3),160,'7 5');arrow((-1,0),(-.2,.4),160)
    if n in [7,8]:
        sign=1 if n==7 else -1
        line((sign*.4,-.2),(sign*.4,.6),160,'7 5')
        arrow((sign*2/3,1/3),(sign*2/15,1/3),160)
    if n==9:
        line((-.4,.6),(.4,.6),160,'7 5');arrow((0,1),(0,.2),160)
    if n==10:
        line((0,-1),(0,.6),160,'9 4 2 4');arrow((-.35,.35),(.35,.35),160)
        label('LEFT HALF GOES BEHIND',160,365,15)
    hinge=[(0,HEAD),(7/60,-23/30)]
    if n in [11,12,13]:line(*hinge,160,'7 5' if n==11 else '3 4',True)
    if n==11:
        arrow((0,-1),(.35,HEAD),160,True)
        line(*hinge,480,'3 4',True)
    if n in [12,13]:
        # Separated paired neck walls in a local opening view, deliberately not to scale.
        # The outer cap crosses OVER the two walls rather than entering between them.
        polygon([(-.36,.2),(0,-.6),(.06,.25)],320,True)
        polygon([(.06,.25),(.4,-.35),(.38,.35)],320,False)
        arrow((-.08,-.53),(-.46,-.05),320)
        arrow((.1,-.52),(.48,-.03),320)
        label('OPEN NECK',320,115,14);label('WRAP OVER OUTSIDE',320,300,14)
    label(step['diagramNote'],320,387,16)
    label('Physical folding and standing are unverified',320,411,15)
    out.append('</svg>');return ''.join(out)

def main():
    d=json.loads((ROOT/'content/tutorials/penguin.json').read_text(encoding='utf-8'))
    states=construction();target=ROOT/'images/penguin';target.mkdir(exist_ok=True);stale=[]
    for n,s in enumerate(d['steps'],1):
        p=target/f'step-{n:02d}.svg';content=diagram(n,s,states)
        if not p.exists() or p.read_text(encoding='utf-8')!=content:
            stale.append(p.name)
            if '--check' not in sys.argv:p.write_text(content,encoding='utf-8',newline='\n')
    if '--check' in sys.argv and stale:raise SystemExit('Stale penguin diagrams: '+', '.join(stale))
    print('Verified' if '--check' in sys.argv else 'Generated',len(d['steps']),'penguin diagrams')
if __name__=='__main__':main()
