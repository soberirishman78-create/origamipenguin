import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def models(file):
    return json.loads((ROOT / 'content' / file).read_text(encoding='utf-8'))

def finished_layers(model):
    step = model['steps'][-1]
    if 'result' in step:
        return [(layer['fill'], [(v['x'], v['y']) for v in layer['vertices']]) for layer in step['result']['layers']]
    image = step['image']
    layers = []
    for polygon in ET.parse(ROOT / image['src']).iter('{http://www.w3.org/2000/svg}polygon'):
        points = [tuple(map(float, pair.split(','))) for pair in polygon.attrib['points'].split()]
        if min(x for x, _ in points) > image['width'] / 2:
            layers.append((polygon.attrib['fill'], points))
    return layers

def symbol(model):
    layers = finished_layers(model)
    xs, ys = zip(*(point for _, points in layers for point in points))
    left, top, right, bottom = min(xs), min(ys), max(xs), max(ys)
    scale = 76 / max(right - left, bottom - top)
    def vertices(points):
        return ' '.join(f'{50+(x-(left+right)/2)*scale:.2f},{50+(y-(top+bottom)/2)*scale:.2f}' for x, y in points)
    name = model['name'].lower().replace(' ', '-')
    faces = ''.join(f'<polygon fill="{fill}" points="{vertices(points)}"/>' for fill, points in layers)
    return f'<symbol id="{name}" viewBox="0 0 100 100"><g stroke="#27394a" stroke-width="1.3" stroke-linejoin="round">{faces}</g></symbol>'

catalog = models('interactive-folds.json') + models('fold-quest.json')
sprite = '<svg xmlns="http://www.w3.org/2000/svg">\n' + '\n'.join(map(symbol, catalog)) + '\n</svg>\n'
(ROOT / 'images' / 'finished-origami.svg').write_text(sprite, encoding='utf-8')
