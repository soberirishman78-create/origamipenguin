"""Combine existing one-page references with a new parent/teacher guide."""
from pathlib import Path
import json,subprocess
from pypdf import PdfReader,PdfWriter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'resources/packs';out.mkdir(exist_ok=True)
items=json.loads((ROOT/'content/free-resources.json').read_text())
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='PackTitle',fontName='Helvetica-Bold',fontSize=25,leading=30,spaceAfter=15,textColor=colors.HexColor('#18394a')))
styles.add(ParagraphStyle(name='PackText',fontSize=13,leading=20,spaceAfter=15))
def footer(c,d):
    c.saveState();c.setFillColor(colors.HexColor('#eeeeee'));c.translate(306,380);c.rotate(32);c.setFont('Helvetica-Bold',110);c.drawCentredString(0,0,'OPP');c.restoreState()
    c.setFont('Helvetica',9);c.drawString(42,30,'OPP | Origami Penguin Publishing | origamipenguin.com/free-resources')
guide=out/'start-here-guide.pdf'
story=[Paragraph('A small guide to a helpful reminder',styles['PackTitle']),Paragraph('FOR PARENTS AND TEACHERS | K-6 REFERENCE PACKS',styles['PackText'])]
for title,body in [('Choose one useful sheet','Start with the idea the student is working on today. Grade bands are suggestions, not limits. A familiar reference from an earlier grade can still help.'),('Look at an example together','Point to one heading and read its worked example. Ask the student to explain the first step in their own words. You can model a step before asking them to try.'),('Try one similar question','Use a small amount of practice. Let the student look back at the sheet instead of trying to remember everything at once. A drawing, objects, or a number line can help too.'),('Check, then choose the next step','Compare the work with the reminder. Talk about which step helped. Keep the sheet nearby, or revisit it another day. Follow the teacher\'s directions about references during assessments.'),('Print only what you need','The first page of each pack is this guide. The remaining pages are one-page references selected for that grade. Use the PDF print dialog to choose individual pages. Print at 100% on US Letter, or Fit on A4.')]:
    story.extend([Paragraph(title,styles['Heading2']),Paragraph(body,styles['PackText'])])
SimpleDocTemplate(str(guide),pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=56,title='OPP Parent and Teacher Reference Guide',author='Origami Penguin Publishing').build(story,onFirstPage=footer,onLaterPages=footer)
assert len(PdfReader(guide).pages)==1
manifest=[]
for grade in range(7):
    label='Kindergarten' if grade==0 else 'Grade '+str(grade)
    selected=[]
    for item in items:
        lo,hi=map(int,item['grades'].replace('K','0').split('-'))
        if lo<=grade<=hi:selected.append(item)
    path=out/('kindergarten' if grade==0 else 'grade-'+str(grade))
    writer=PdfWriter();writer.append(guide)
    for item in selected:writer.append(ROOT/'resources'/(item['slug']+'.pdf'))
    writer.add_metadata({'/Title':'OPP '+label+' Reference Starter Pack','/Author':'Origami Penguin Publishing'})
    with path.with_suffix('.pdf').open('wb') as f:writer.write(f)
    assert len(PdfReader(path.with_suffix('.pdf')).pages)==len(selected)+1
    manifest.append({'grade':grade,'title':label+' starter pack','url':'/resources/packs/'+path.name+'.pdf','sheets':[i['slug'] for i in selected],'pages':len(selected)+1})
(ROOT/'content/resource-packs.json').write_text(json.dumps(manifest,indent=2)+'\n')
subprocess.run(['pdftoppm','-singlefile','-scale-to','1100','-png',str(guide),str(ROOT.parent.parent/'outputs/resource-pack-guide')],check=True,capture_output=True)
print('Created 7 grade packs plus the one-page guide')
