"""Build a share-card SVG from the current tutorial's original vector layers.

Rasterize at its native 1200 x 630 size for social platforms.
This is a diagram preview, not a photograph or physical-fold validation.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'
source = ET.parse(ROOT / 'images/penguin/step-14.svg').getroot()
# The right-hand panel is the current step-14 checkpoint. Preserve layer order.
polygons = [p for p in source.findall(NS + 'polygon')
            if min(float(v.split(',')[0]) for v in p.attrib['points'].split()) > 320]
assert polygons
layers = ''.join(ET.tostring(p, encoding='unicode').replace('ns0:', '').replace(':ns0', '') for p in polygons)
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">Origami Penguin: 14 illustrated steps</title>
<desc id="desc">Diagram preview from the current penguin tutorial, with a matching diagram for every step.</desc>
<rect width="1200" height="630" fill="#f3f7fa"/>
<rect x="0" y="0" width="18" height="630" fill="#2466a0"/>
<g font-family="Arial, sans-serif" fill="#172c42">
<text x="68" y="104" font-size="24" letter-spacing="3">ORIGAMI PENGUIN</text>
<text x="64" y="234" font-size="66" font-weight="700">Fold a penguin</text>
<text x="68" y="316" font-size="38" fill="#2466a0">14 illustrated steps</text>
<text x="68" y="384" font-size="25">Follow each fold and orientation change.</text>
<text x="68" y="548" font-size="26">origamipenguin.com</text>
<rect x="756" y="96" width="384" height="440" rx="24" fill="white"/>
<text x="948" y="498" text-anchor="middle" font-size="20">Tutorial diagram preview</text>
</g>
<g transform="translate(252,10) scale(1.45)">''' + layers + '</g></svg>\n'
(ROOT / 'images/penguin-social-14-steps.svg').write_text(svg, encoding='utf-8', newline='\n')

if __name__ == '__main__':
    # Optional authoring dependency only; the normal site build uses the saved PNG.
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGB', (2400, 1260), '#f3f7fa')
    draw = ImageDraw.Draw(im)
    for el in ET.fromstring(svg).iter():
        a = el.attrib
        tag = el.tag.split('}')[-1]
        if tag == 'rect':
            x, y = float(a.get('x', 0)), float(a.get('y', 0))
            draw.rounded_rectangle([x*2, y*2, (x+float(a['width']))*2, (y+float(a['height']))*2],
                                   radius=float(a.get('rx', 0))*2, fill=a['fill'])
        elif tag == 'text':
            font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if a.get('font-weight') == '700'
                                     else 'C:/Windows/Fonts/arial.ttf', int(a['font-size'])*2)
            draw.text((float(a['x'])*2, float(a['y'])*2), el.text, font=font,
                      fill=a.get('fill', '#172c42'), anchor='ms' if a.get('text-anchor') == 'middle' else 'ls')
        elif tag == 'polygon':
            pts = [((float(v.split(',')[0])*1.45+252)*2, (float(v.split(',')[1])*1.45+10)*2)
                   for v in a['points'].split()]
            draw.polygon(pts, fill=a['fill'])
            draw.line(pts+[pts[0]], fill=a['stroke'], width=6, joint='curve')
    im.resize((1200, 630), Image.Resampling.LANCZOS).save(ROOT / 'images/penguin-social-14-steps.png')
