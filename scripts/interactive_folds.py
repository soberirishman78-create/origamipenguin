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

def tip_layer(layers, start, end):
    candidates = [(i, poly) for i, (poly, _) in enumerate(layers) if start in poly]
    if start == (200, 200):
        dx, dy = end[0] - start[0], end[1] - start[1]
        return max(candidates, key=lambda item: (sum((x-start[0])*dx+(y-start[1])*dy for x,y in item[1])/len(item[1]), item[0]))[0]
    return candidates[-1][0]

def fold(layers, start, end, top_only=False):
    mid = tuple((a+b)/2 for a,b in zip(start,end))
    normal = tuple(b-a for a,b in zip(start,end))
    norm = sum(n*n for n in normal)
    fixed, flipped = [], []
    selected = tip_layer(layers, start, end) if top_only else None
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

def model(name, intro, moves, sheet=square, material="paper"):
    layers=[(sheet,front)]
    steps=[dict(title='Set out your paper',text=intro,scene=scene(layers))]
    for title, text, start, end, *flags in moves:
        old=layers
        if start is None:
            layers=[([(400-x,y) for x,y in poly], back if color==front else front) for poly,color in reversed(layers)]
        else:
            layers=fold(layers,start,end,bool(flags))
        before = scene(old,[(start,end)] if start else [])
        if flags:
            before["actions"][0]["layer"] = tip_layer(old, start, end)
        steps.append(dict(title=title,text=text,scene=before,result=scene(layers)))
    return dict(name=name,material=material,steps=steps)

down=('Make a triangle','Bring the top point to the bottom point. Press along the horizontal fold.',(200,70),(200,330))
up=('Make a triangle','Bring the bottom point to the top point. Press along the horizontal fold.',(200,330),(200,70))
turn=('Turn the model over','Flip the paper left to right, keeping the top edge at the top.',None,None)
diamond='Put a square of paper down like a diamond, with a point at the top. The lighter side starts up.'
models=[
model('Kite',diamond,[
 ('Fold the left lower edge inward','Bring the left corner to the centre line, a little below the middle of the sheet. Match the lower-left edge to the centre line.',(70,200),(200,254)),
 ('Fold the right lower edge inward','Bring the right corner to the same spot on the centre line. The two lower edges should now meet along that line.',(330,200),(200,254)),
]),
model('Cat Face',diamond,[
 down,
 ('Raise the left ear','Bring the left corner diagonally up and slightly inward. Leave a pointed ear above the straight edge.',(70,200),(100,155)),
 ('Raise the right ear','Pull the right corner diagonally up and slightly inward, matching the height of the left ear.',(330,200),(300,155)),
 ('Soften the chin','Fold a small bit of the bottom point up. Keep the fold shallow.',(200,330),(200,304)),
 turn,
]),
model('Dog Face',diamond,[
 down,
 ('Fold the left ear down','Pull the left corner diagonally down to make a floppy ear.',(70,200),(112,277)),
 ('Fold the right ear down','Pull the right corner diagonally down and inward. Match the height of the left ear.',(330,200),(288,277)),
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
 ('Turn the boat over','Flip the boat left to right, keeping the sail pointing up. The narrow hull sits along the bottom.',None,None),
])]
flat_square = [(75,75),(325,75),(325,325),(75,325)]
bill = [(50,136),(350,136),(350,264),(50,264)]
flat_setup = 'Set a square of paper in front of you with a straight edge at the top.'
bill_setup = 'Lay one U.S. dollar bill flat with the long edges running left to right. You can also practise with a rectangle about 2.34 times as wide as it is tall.'
models += [
model('Paper House',flat_setup,[
 ('Shape the left side of the roof','Bring the upper-left corner diagonally down and inward. The crease becomes the left slope of the roof.',(75,75),(200,200)),
 ('Shape the right side of the roof','Bring the upper-right corner to the same spot. The two roof slopes meet at the top.',(325,75),(200,200)),
 ('Show the front','Turn the paper over left to right. Add a door or windows to the flat front if you like.',None,None),
],flat_square),
model('Paper Picture Frame',diamond,[
 ('Fold the left corner in','Bring the left point to the centre.',(70,200),(200,200)),
 ('Fold the right corner in','Bring the right point to the centre.',(330,200),(200,200)),
 ('Fold the bottom corner in','Bring the bottom point to the centre.',(200,330),(200,200)),
 ('Fold the top corner in','Bring the top point to the centre.',(200,70),(200,200)),
 ('Turn back the left tip','Pull the centre tip of the left flap toward the left, stopping short of the outer edge.',(200,200),(151,200),True),
 ('Turn back the right tip','Pull the centre tip of the right flap toward the right.',(200,200),(249,200),True),
 ('Turn back the lower tip','Pull the centre tip of the lower flap toward the bottom.',(200,200),(200,249),True),
 ('Turn back the upper tip','Pull the last tip toward the top. Slide the corners of a small paper picture beneath the four turned-back tips.',(200,200),(200,151),True),
]),
model('Paper Crown',diamond,[
 up,
 ('Raise the left point','Fold the left corner up and inward to form one of the crown points.',(70,200),(128,102)),
 ('Raise the right point','Match the fold on the right. Keep the tall centre point visible.',(330,200),(272,102)),
 ('Fold up the band','Lift the middle of the bottom edge a little to give the crown a straight band.',(200,200),(200,170)),
]),
model('Dollar Bill Arrow',bill_setup,[
 ('Fold in the upper corner','Bring the top-right corner diagonally down and left to the centre line. Keep the midpoint of the right edge fixed.',(350,136),(286,200)),
 ('Fold in the lower corner','Bring the bottom-right corner to the same spot to make the arrow point.',(350,264),(286,200)),
 ('Narrow the top of the shaft','At the left edge, bring the top corner down to the centre line.',(50,136),(50,200)),
 ('Narrow the bottom of the shaft','Bring the bottom-left corner up to the centre line to match.',(50,264),(50,200)),
],bill,'bill'),
model('Dollar Bill Packet',bill_setup,[
 ('Lift the bottom edge','Bring the lower edge straight up to make a narrow band.',(200,264),(200,210)),
 ('Fold the left end in','Fold the left end toward the middle. Keep the vertical crease straight.',(50,200),(170,200)),
 ('Fold the right end in','Repeat on the right so the folded ends sit beside each other.',(350,200),(230,200)),
 ('Close the packet','Fold the upper edge down over the folded ends.',(200,136),(200,239)),
],bill,'bill'),
model('Dollar Bill Pennant',bill_setup,[
 ('Fold the upper-right corner inward','Bring the upper-right corner down to the midpoint of the bill’s height, forming the upper slope of the flag.',(350,136),(286,200)),
 ('Fold the lower-right corner inward','Bring the lower-right corner up to meet the first corner. The right end now makes a point.',(350,264),(286,200)),
 ('Shorten the flat end','Bring the left edge partway toward the point. Keep its crease vertical.',(50,200),(246,200)),
 ('Show the front','Flip the folded pennant left to right to see the smooth side.',None,None),
],bill,'bill'),
]
p = Path(__file__).resolve().parents[1] / 'content/interactive-folds.json'
p.write_text('[\n'+',\n'.join(json.dumps(m,ensure_ascii=False,separators=(',',':')) for m in models)+'\n]\n',encoding='utf-8')
