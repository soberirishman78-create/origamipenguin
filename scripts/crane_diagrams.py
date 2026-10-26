"""Original schematic crane diagrams; exact base landmarks, not a 3D simulator.

Pocket-opening panels communicate layer selection. They are deliberately
labelled schematic, and cannot certify self-intersection or physical access.
"""
from pathlib import Path
from html import escape
from math import sqrt,tan,pi
import json,sys
from heart_geometry import fold,reflect,clip
ROOT=Path(__file__).resolve().parents[1]
K=sqrt(2)-1; A=2-sqrt(2); H=(0,-K); U=(0,1-2*sqrt(2)); B=(0,1)
BASE=[(0,-1),(1,0),B,(-1,0)]
BIRD=[U,(A,-K),B,(-A,-K)]
NARROW=tan(pi/16)

def narrowed():
    return fold(fold([(BIRD,True)],1,NARROW,NARROW),-1,NARROW,NARROW)

def svg(n,t):
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="480" viewBox="0 0 720 480" role="img" aria-labelledby="title desc"><title id="title">Crane step {n}: {escape(t["title"])}</title><desc id="desc">Original diagram. {escape(t["diagramNote"])} Grey shows paper; blue marks the selected flap, not paper colour. Hidden layers are omitted.</desc><rect width="720" height="480" fill="white"/><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#1d5788"/></marker></defs>']
    def point(p,cx):return f'{cx+83*p[0]:.3f},{240+83*p[1]:.3f}'
    def polygon(poly,cx,fill='#e8edf1'):
        out.append(f'<polygon points="{" ".join(point(p,cx) for p in poly)}" fill="{fill}" stroke="#253343" stroke-width="1.7" stroke-linejoin="round"/>')
    def line(p,q,cx,dash='',colour='#253343'):
        out.append(f'<path d="M{point(p,cx)} L{point(q,cx)}" fill="none" stroke="{colour}" stroke-width="2" stroke-dasharray="{dash}"/>')
    def arrow(p,q,cx):
        middle=((p[0]+q[0])/2+.2,(p[1]+q[1])/2)
        out.append(f'<path d="M{point(p,cx)} Q{point(middle,cx)} {point(q,cx)}" fill="none" stroke="#1d5788" stroke-width="2.5" marker-end="url(#arrow)"/>')
    def label(s,x,y,size=21):out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="#253343">{escape(s)}</text>')
    def state(kind,cx):
        if kind.startswith('sheet'):
            polygon(BASE,cx,'#f6f7f9');label('COLOUR UP' if kind in ['sheet','sheet-v','sheet-cross'] else 'WHITE UP',cx,355,16)
            if kind!='sheet':line((0,-1),B,cx,'3 5','#667787')
            if kind not in ['sheet','sheet-v']:line((-1,0),(1,0),cx,'3 5','#667787')
            if kind=='sheet-all':
                line((-.5,-.5),(.5,.5),cx,'9 4 2 4','#667787');line((.5,-.5),(-.5,.5),cx,'9 4 2 4','#667787')
        elif kind in ['base','precreases','kite','cap']:
            if kind=='cap':
                for p,_ in fold([(BASE,True)],0,1,-K,False):polygon(p,cx)
            else:polygon(BASE,cx)
            line(H if kind=='cap' else (0,-1),B,cx,'3 4','#788899')
            if kind in ['kite','cap']:
                layers=fold(fold([(BASE,True)],1,K,K),-1,K,K)
                if kind=='cap':layers=fold(layers,0,1,-K,False)
                for p,_ in layers:polygon(p,cx,'#a9cfed')
            if kind=='precreases':
                line(B,(A,-K),cx,'3 4','#667787');line(B,(-A,-K),cx,'3 4','#667787');line((-A,-K),(A,-K),cx,'3 4','#667787')
            if kind!='cap':label('CLOSED',cx,130,15)
            label('LOOSE CORNERS',cx,355,15)
        elif kind=='pocket':
            polygon(BASE,cx)
            polygon([(-A,-K),(.0,-1.65),(A,-K),(.0,.35)],cx,'#a9cfed')
            line((-A,-K),(A,-K),cx,'7 5','#1d5788')
            arrow((0,.35),U,cx);arrow((-.62,-.1),(-.2,-.4),cx);arrow((.62,-.1),(.2,-.4),cx)
            label('ONE FLAP OPEN',cx,365,16)
        elif kind in ['one-petal','back-base','back-kite','back-precreases','bird','front-narrow','narrow','left-pre','left-up','both-up','beak','wings']:
            if kind in ['one-petal','back-base','back-kite','back-precreases']:
                if kind=='one-petal':polygon(BASE,cx);polygon(BIRD,cx,'#a9cfed')
                else:
                    polygon(BIRD,cx)
                    if kind=='back-kite':
                        for p,_ in fold(fold([(BASE,True)],1,K,K),-1,K,K):polygon(p,cx,'#a9cfed')
                    else:state({'back-base':'base','back-precreases':'precreases'}[kind],cx)
            elif kind=='bird':
                polygon(BIRD,cx,'#a9cfed');line(H,B,cx)
                label('2 BROAD WINGS ABOVE',cx,50,15);label('2 SEPARATE LEGS BELOW',cx,365,15)
            else:
                layers=narrowed()
                if kind=='front-narrow':polygon(BIRD,cx)
                if kind in ['left-up','both-up','beak','wings']:
                    for sign in [-1,1]:
                        for poly,_ in layers:
                            lower=clip(clip(poly,0,1,-K,True),1,0,0,sign>0)
                            if not lower:continue
                            if sign<0 or kind!='left-up':
                                parts=fold([(lower,True)],-sign,1+sqrt(2),-1)
                                if sign<0 and kind in ['beak','wings']:
                                    parts=fold(parts,0,1,-1.16,False)
                                for p,_ in parts:polygon(p,cx,'#a9cfed')
                            else:polygon(lower,cx,'#a9cfed')
                    # Broad wing sheets cover the roots of the reversed legs.
                    if kind=='wings':
                        polygon([H,(-1.5,-.75),(-.18,.05)],cx,'#e8edf1')
                        polygon([H,(1.5,-.75),(.18,.05)],cx,'#a9cfed')
                        polygon([H,(-.18,.05),(0,.2),(.18,.05)],cx)
                        label('POSE SCHEMATIC',cx,365,15)
                    else:
                        for poly,_ in layers:
                            upper=clip(poly,0,1,-K,False)
                            if upper:polygon(upper,cx)
                else:
                    for p,_ in layers:polygon(p,cx,'#a9cfed')
                    line(H,B,cx)
        else:raise ValueError(kind)
    before=t['before'];after=t['after'];state(before,180);state(after,540)
    label('Before',180,27,25);label('After / checkpoint',540,27,25)
    if n==2:line((0,-1),B,180,'7 5','#1d5788');arrow((-1,0),(1,0),180)
    if n==3:line((-1,0),(1,0),180,'7 5','#1d5788');arrow(B,(0,-1),180)
    if n==5:
        line((-.5,-.5),(.5,.5),180,'7 5','#1d5788');line((.5,-.5),(-.5,.5),180,'7 5','#1d5788')
        arrow((0,1),(-1,0),180);arrow((0,1),(1,0),180)
    if n==6:
        arrow((-1,0),B,180);arrow((1,0),B,180)
        arrow((0,-1),(.08,.92),180)
        label('CORNERS COME TOGETHER',180,390,14)
    if n in [7,13]:
        line(B,(A,-K),180,'7 5','#1d5788');line(B,(-A,-K),180,'7 5','#1d5788');arrow((1,0),H,180);arrow((-1,0),H,180)
    if n==8:line((-A,-K),(A,-K),180,'7 5','#1d5788');arrow((0,-1),(0,1-2*K),180)
    if n in [10,15]:arrow(B,U,180)
    if n in [17,19]:
        qx=NARROW*(1-U[1])/(1+NARROW*(1+sqrt(2)));qy=(1+sqrt(2))*qx+U[1]
        line(B,(qx,qy),180,'7 5','#1d5788');line(B,(-qx,qy),180,'7 5','#1d5788')
        arrow((A,-K),(0,1-sqrt(A*A+(1+K)**2)),180);arrow((-A,-K),(0,1-sqrt(A*A+(1+K)**2)),180)
    if n in [20,21]:arrow((-.09,.65),(-1,-1-K),180)
    if n in [22,23]:arrow((.09,.65),(1,-1-K),180)
    def reverse_crease(sign,cx,dash):
        # Intersection with narrowed lower edge x=sign*t*(1-y).
        y=(-1+NARROW)/(1+sqrt(2)+NARROW)
        q=(sign*NARROW*(1-y),y)
        line(H,q,cx,dash,'#1d5788' if dash=='7 5' else '#667787')
    if n==20:reverse_crease(-1,180,'7 5');reverse_crease(-1,540,'3 4')
    if n==21:reverse_crease(-1,180,'3 4')
    if n==22:reverse_crease(1,180,'7 5');reverse_crease(1,540,'3 4')
    if n==23:reverse_crease(1,180,'3 4')
    if n in [21,23]:
        # Magnified open side pocket: the selected point travels between two walls.
        # Offset walls show separation, not an exact perspective mesh.
        polygon([(-.38,.25),(0,-.75),(.08,.25)],360,'#e8edf1')
        polygon([(.08,.25),(.45,-.55),(.38,.45)],360,'#e8edf1')
        polygon([(-.07,.25),(.13,-.35),(.17,.25)],360,'#a9cfed')
        arrow((.08,.2),(.08,-.52),360)
        label('OPEN SIDE',360,130,14);label('DETAIL ONLY',360,325,14)
    if n in [24,25]:
        # Separate magnified tip detail; opening is schematic, not a surface mesh.
        polygon([(-.35,0),(0,-.65),(.16,0)],360,'#a9cfed')
        line((-.18,-.32),(.08,-.32),360,'7 5','#1d5788');arrow((0,-.65),(0,.01),360)
        label('TIP DETAIL',360,285,14)
    if n==26:arrow((-.08,-1.55),(-.95,-.6),180);arrow((.08,-1.55),(.95,-.6),180)
    note=t['diagramNote']
    # Keep readable labels short; full operational detail is adjacent prose.
    label(note,360,435,17)
    label('SCHEMATIC: hidden layers omitted',360,466,16)
    out.append('</svg>');return ''.join(out)

def main():
    data=json.loads((ROOT/'content/tutorials/crane.json').read_text(encoding='utf-8'))
    target=ROOT/'images/crane';target.mkdir(exist_ok=True);stale=[]
    for n,step in enumerate(data['steps'],1):
        p=target/f'step-{n:02d}.svg';content=svg(n,step)
        if not p.exists() or p.read_text(encoding='utf-8')!=content:
            stale.append(p.name)
            if '--check' not in sys.argv:p.write_text(content,encoding='utf-8',newline='\n')
    if '--check' in sys.argv and stale:raise SystemExit('Stale crane diagrams: '+', '.join(stale))
    print('Verified' if '--check' in sys.argv else 'Generated',len(data['steps']),'crane diagrams')
if __name__=='__main__':main()
