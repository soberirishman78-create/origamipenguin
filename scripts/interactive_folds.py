import json
from pathlib import Path

square = [(200,70),(330,200),(200,330),(70,200)]
front, back = '#fffdf6', '#f2a676'

def clip(poly, normal, mid, sign):
    def signed(p):
        return sign * sum((p[i]-mid[i])*normal[i] for i in range(2))
    out = []
    for a,b in zip(poly, poly[1:]+poly[:1]):
        da, db = signed(a), signed(b)
        if da >= 0:
            out.append(a)
        if (da > 0 > db) or (db > 0 > da):
            out.append(tuple(a[i]+(b[i]-a[i])*da/(da-db) for i in range(2)))
    return out

def tip_layer(layers, start):
    return max(i for i,(poly,_) in enumerate(layers) if start in poly)

def fold(layers, start, end, top_only=False):
    mid = tuple((a+b)/2 for a,b in zip(start,end))
    normal = tuple(b-a for a,b in zip(start,end))
    norm = sum(n*n for n in normal)
    fixed, flipped = [], []
    selected = tip_layer(layers, start) if top_only else None
    for index,(poly,color) in enumerate(layers):
        if top_only and index != selected:
            fixed.append((poly,color))
            continue
        rest = clip(poly,normal,mid,1)
        flap = clip(poly,normal,mid,-1)
        if len(rest)>2:
            fixed.append((rest,color))
        if len(flap)>2:
            reflected = [tuple(p[i]-2*sum((p[j]-mid[j])*normal[j] for j in range(2))*normal[i]/norm for i in range(2)) for p in flap]
            flipped.insert(0,(reflected,back if color==front else front))
    return fixed+flipped

def scene(layers, actions=()):
    def pt(p):
        return dict(x=round(p[0],2), y=round(p[1],2))
    return dict(layers=[dict(fill=color,vertices=[pt(p) for p in poly]) for poly,color in layers],
                actions=[{'from':pt(a),'to':pt(b)} for a,b in actions])

def model(name, intro, moves):
    layers=[(square,front)]
    steps=[dict(title='Set out your paper',text=intro,scene=scene(layers))]
    for title, text, start, end, *flags in moves:
        old=layers
        if start is None:
            layers=[([(400-x,y) for x,y in poly], back if color==front else front) for poly,color in reversed(layers)]
        else:
            layers=fold(layers,start,end,bool(flags))
        before = scene(old,[(start,end)] if start else [])
        if flags:
            before["actions"][0]["layer"] = tip_layer(old, start)
        steps.append(dict(title=title,text=text,scene=before,result=scene(layers)))
    return dict(name=name,steps=steps)

down=('Make a triangle','Bring the top point to the bottom point. Press along the horizontal fold.',(200,70),(200,330))
up=('Make a triangle','Bring the bottom point to the top point. Press along the horizontal fold.',(200,330),(200,70))
turn=('Turn the model over','Flip the paper left to right, keeping the top edge at the top.',None,None)
diamond='Put a square of paper down like a diamond, with a point at the top. The lighter side starts up.'
models=[
model('Kite',diamond,[
 ('Fold the left lower edge inward','Bring the left corner onto the centre line. The fold starts at the bottom point.',(70,200),(200,254)),
 ('Fold the right lower edge inward','Mirror the first fold so the two folded edges meet along the centre line.',(330,200),(200,254)),
]),
model('Cat Face',diamond,[
 down,
 ('Raise the left ear','Bring the left corner diagonally up and slightly inward. Leave a pointed ear above the straight edge.',(70,200),(100,155)),
 ('Raise the right ear','Match the angle and height of the left ear.',(330,200),(300,155)),
 ('Soften the chin','Fold a small bit of the bottom point up. Keep the fold shallow.',(200,330),(200,304)),
 turn,
]),
model('Dog Face',diamond,[
 down,
 ('Fold the left ear down','Pull the left corner diagonally down to make a floppy ear.',(70,200),(112,277)),
 ('Fold the right ear down','Repeat on the right so the ears hang at the same height.',(330,200),(288,277)),
 ('Fold up the muzzle','Turn up a small triangle at the bottom. You can draw a nose on this flap.',(200,330),(200,282)),
]),
model('Fox Face',diamond,[
 down,
 ('Raise the left point','Fold the left point sharply upward to make a tall ear.',(70,200),(131,113)),
 ('Raise the right point','Mirror the left ear, leaving a space between the tips.',(330,200),(269,113)),
 turn,
]),
model('Envelope',diamond,[
 ('Bring the left point to the centre','Fold the left point to the middle of the square.',(70,200),(200,200)),
 ('Bring the right point to the centre','Bring the right point in to meet the first point.',(330,200),(200,200)),
 ('Raise the bottom flap','Bring the bottom point slightly above the middle, overlapping the side flaps.',(200,330),(200,177)),
 ('Close the top flap','Fold the top point down over the other folds. A sticker can hold the paper envelope closed.',(200,70),(200,230)),
]),
model('Paper Cup',diamond,[
 up,
 ('Cross the left point','Bring the left corner to the opposite sloping edge, about a third of the way up from the base.',(70,200),(287,157)),
 ('Cross the right point','Repeat in the other direction. Line up the two crossing folds.',(330,200),(113,157)),
 ('Lower the front rim','Fold only the front tip down over the crossed flaps. Leave the back tip standing.',(200,70),(200,190),True),
 turn,
 ('Lower the back rim','Fold the remaining tip down on this side. Gently separate the two sides at the top to open your cup.',(200,70),(200,190),True),
]),
model('Sailboat',diamond,[
 up,
 ('Fold a strip for the hull','Bring the middle of the bottom edge up toward the tip, leaving most of the triangle visible as the sail.',(200,200),(200,154)),
 ('Turn the boat over','Flip the shape to see the broad face of the sail and the folded hull on the reverse.',None,None),
])]
p = Path(__file__).resolve().parents[1] / 'content/interactive-folds.json'
p.write_text('[\n'+',\n'.join(json.dumps(m,ensure_ascii=False,separators=(',',':')) for m in models)+'\n]\n',encoding='utf-8')
