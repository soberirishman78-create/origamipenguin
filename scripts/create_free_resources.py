"""Rebuild the original printable library. Requires reportlab, pypdf and Poppler.
Normal site builds use the checked-in PDFs and page data; no PDF dependency in CI.
"""
from pathlib import Path
import json, subprocess
from html import escape as e
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resources';OUT.mkdir(exist_ok=True)
PREVIEW=ROOT/'images/resources';PREVIEW.mkdir(exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleOPP',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=colors.HexColor('#18394a'),spaceAfter=8))
styles.add(ParagraphStyle(name='SubOPP',fontSize=11,leading=15,textColor=colors.HexColor('#4b585c'),spaceAfter=17))
styles.add(ParagraphStyle(name='HeadOPP',fontName='Helvetica-Bold',fontSize=14,leading=18,spaceBefore=12,spaceAfter=7,textColor=colors.HexColor('#18394a')))
styles.add(ParagraphStyle(name='TextOPP',fontName='Helvetica',fontSize=12.5,leading=18,spaceAfter=8))
styles.add(ParagraphStyle(name='CellOPP',fontName='Helvetica',fontSize=11,leading=15))
styles.add(ParagraphStyle(name='SmallOPP',fontSize=10.5,leading=14,spaceAfter=8))

S=[]
def sheet(slug,title,grades,subject,intro,blocks):
    S.append(dict(slug=slug,title=title,grades=grades,subject=subject,intro=intro,blocks=blocks))
def text(heading,*lines):return {'heading':heading,'lines':list(lines)}
def table(heading,rows,widths=None):return {'heading':heading,'rows':rows,'widths':widths}

sheet('numbers-0-20','Numbers 0-20','K-1','Math','Say it. Find it. Count one object for each number.',[
 table('Number names',[['0 zero','1 one','2 two'],['3 three','4 four','5 five'],['6 six','7 seven','8 eight'],['9 nine','10 ten','11 eleven'],['12 twelve','13 thirteen','14 fourteen'],['15 fifteen','16 sixteen','17 seventeen'],['18 eighteen','19 nineteen','20 twenty']]),
 text('Count in order','0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10','11, 12, 13, 14, 15, 16, 17, 18, 19, 20'),
 text('One more / one less','One more than 8 is 9. One less than 8 is 7.'),
 text('Compare two groups','More means a larger amount. Fewer means a smaller amount.','The same number means equal. Match objects one to one to compare.')])
sheet('place-value','Place value','1-4','Math','A digit gets its value from its place in a number.',[
 table('Read 4,582',[['Thousands','Hundreds','Tens','Ones'],['4','5','8','2'],['4,000','500','80','2']]),
 text('Three ways to write it','Standard: 4,582','Expanded: 4,000 + 500 + 80 + 2','Word form: four thousand five hundred eighty-two'),
 text('Trade without changing the value','10 ones = 1 ten. 10 tens = 1 hundred.','10 hundreds = 1 thousand.'),
 text('Compare whole numbers','Start at the left. Compare the first place with different digits.','4,582 &gt; 4,528 because 8 tens is more than 2 tens.'),
 text('Round a whole number','Find the place. Look one place to its right.','0-4: keep the digit. 5-9: add 1 to the digit.','Change all digits to the right to zero. Example: 4,582 to the nearest hundred is 4,600.')])
sheet('addition-subtraction','Addition & subtraction','K-2','Math','Addition joins amounts. Subtraction takes away or finds the difference.',[
 text('Count on to add','Start with 7. Add 3: say 8, 9, 10. So 7 + 3 = 10.'),
 text('Make a ten','8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.'),
 text('Use a double','6 + 6 = 12, so 6 + 7 is one more: 13.'),
 text('Think addition to subtract','For 13 - 8, ask: 8 plus what makes 13?','8 + 5 = 13, so 13 - 8 = 5.'),
 table('A fact family uses the same three numbers',[['Addition','Subtraction'],['4 + 6 = 10','10 - 4 = 6'],['6 + 4 = 10','10 - 6 = 4']]),
 text('Check your answer','Use objects, draw dots, or use the opposite operation.','For 9 - 4 = 5, check that 5 + 4 = 9.')])
sheet('multiplication-chart','Multiplication chart 0-12','2-6','Math','Find one factor on the left and the other across the top. Meet at the product.',[
 table('',[['x']+list(range(13))]+[[a]+[a*b for b in range(13)] for a in range(13)]),
 text('Ways to remember','Any number x 0 = 0. Any number x 1 = itself.','3 x 4 = 4 x 3. Turn an array to see the same total.','6 x 7 = (5 x 7) + (1 x 7) = 35 + 7 = 42.'),
 text('Connect multiplication and division','4 x 6 = 24, so 24 divided by 6 = 4 and 24 divided by 4 = 6.')])
sheet('division-steps','Division reminders','3-6','Math','Division makes equal groups or finds the size of each group.',[
 text('Think of a related multiplication fact','42 divided by 6 = ? Think: 6 x ? = 42. Answer: 7.'),
 text('Divide 156 by 3, one place at a time','1. 1 hundred cannot make 3 whole hundreds in each group. Use 15 tens.','2. 15 tens divided by 3 = 5 tens. Write 5 in the tens place.','3. Bring down the 6 ones. 6 divided by 3 = 2 ones.','4. Answer: 52. Check: 52 x 3 = 156.'),
 text('A remainder is an amount left over','17 divided by 5 = 3 remainder 2, because 5 x 3 + 2 = 17.','The remainder must be smaller than the divisor.'),
 text('What does the problem ask?','17 people, 5 seats per car: need 4 cars, because everyone needs a seat.','17 stickers shared by 5 students: 3 each, with 2 left over.'),
 text('Remember','You cannot divide by zero. 0 divided by a nonzero number is 0.')])
sheet('fraction-decimal-percent','Fractions, decimals & percents','4-6','Math','These are different ways to name the same part of a whole.',[
 table('Common equivalents',[['Fraction','Decimal','Percent'],['1/10','0.1','10%'],['1/8','0.125','12.5%'],['1/5','0.2','20%'],['1/4','0.25','25%'],['1/3','0.333...','33 1/3%'],['1/2','0.5','50%'],['2/3','0.666...','66 2/3%'],['3/4','0.75','75%'],['1 whole','1.0','100%']]),
 text('Fraction to decimal','Divide the numerator by the denominator. 3/4 = 3 divided by 4 = 0.75.'),
 text('Decimal to percent','Multiply by 100. 0.75 x 100 = 75, so 0.75 = 75%.'),
 text('Percent to decimal','Divide by 100. 25% = 25/100 = 0.25.'),
 text('Watch the repeating decimals','The dots in 0.333... mean the 3 repeats forever. 0.33 is only an approximation of 1/3.')])
sheet('fraction-steps','Working with fractions','3-6','Math','Use equal-sized parts. The denominator tells the size of the parts.',[
 text('Name the parts','In 3/4, the numerator 3 counts the parts.','The denominator 4 means the whole is split into 4 equal parts.'),
 text('Make an equivalent fraction','Multiply or divide the top and bottom by the same nonzero number.','1/2 = 2/4 = 3/6. Divide 6/8 by 2 on top and bottom to get 3/4.'),
 text('Add or subtract: use a common denominator','1/2 + 1/3 = 3/6 + 2/6 = 5/6.','3/4 - 1/2 = 3/4 - 2/4 = 1/4.','Add or subtract the numerators. Keep the common denominator.'),
 text('Multiply across','2/3 x 3/4 = (2 x 3)/(3 x 4) = 6/12 = 1/2.'),
 text('Divide: multiply by the reciprocal','3/4 divided by 1/2 = 3/4 x 2/1 = 6/4 = 1 1/2.','Do not divide by zero.'),
 text('Check the whole','Compare fractions of the same-sized whole. Draw fraction bars if you need a picture.')])
sheet('measurement-conversions','Measurement conversions','3-6','Math','Use matching units. These customary measures use U.S. units.',[
 table('Length',[['U.S. customary','Metric'],['12 inches = 1 foot','10 millimeters = 1 centimeter'],['3 feet = 1 yard','100 centimeters = 1 meter'],['5,280 feet = 1 mile','1,000 meters = 1 kilometer']],[264,264]),
 table('Capacity and mass / weight',[['U.S. liquid capacity','Metric capacity'],['8 fluid ounces = 1 cup','1,000 milliliters = 1 liter'],['2 cups = 1 pint','Metric mass'],['2 pints = 1 quart','1,000 milligrams = 1 gram'],['4 quarts = 1 gallon','1,000 grams = 1 kilogram']],[264,264]),
 text('U.S. customary weight','16 ounces = 1 pound. 2,000 pounds = 1 short ton.'),
 text('Choose multiply or divide','Larger unit to smaller unit: multiply. 3 feet x 12 = 36 inches.','Smaller unit to larger unit: divide. 200 centimeters divided by 100 = 2 meters.'),
 text('Check the label','A fluid ounce measures volume. An ounce of weight measures weight. They are not the same kind of measurement.')])
sheet('shapes-area-perimeter','Shapes, area & perimeter','2-6','Math','Perimeter is distance around. Area measures a surface.',[
 table('Shape facts',[['Shape','Remember'],['Triangle','3 sides; angles total 180 degrees'],['Quadrilateral','4 sides; angles total 360 degrees'],['Rectangle','4 right angles; opposite sides equal'],['Square','4 equal sides and 4 right angles'],['Circle','Radius: center to edge. Diameter = 2 x radius.']],[130,398]),
 text('Rectangle','Perimeter = 2 x (length + width). Area = length x width.','Example: length 5 cm, width 3 cm. Perimeter = 16 cm. Area = 15 square cm.'),
 text('Triangle','Area = (base x perpendicular height) divided by 2.','Example: base 8 cm, height 3 cm. Area = 12 square cm.'),
 text('Rectangular prism','Volume = length x width x height. Use cubic units.','Example: 4 cm x 3 cm x 2 cm = 24 cubic cm.'),
 text('Label your answer','Length: cm. Area: square cm. Volume: cubic cm.')])
sheet('decimals-operations','Decimals & operation order','4-6','Math','Read places carefully and estimate before calculating.',[
 table('Read 3.456',[['Ones','Tenths','Hundredths','Thousandths'],['3','4','5','6']]),
 text('Add and subtract','Line up decimal points. Add zeros to show equal places.','2.40 + 0.35 = 2.75. 5.00 - 1.28 = 3.72.'),
 text('Multiply decimals','Multiply as whole numbers. Count decimal places in BOTH factors.','1.2 x 0.3: 12 x 3 = 36. Two decimal places total gives 0.36.'),
 text('Divide by a decimal','Multiply BOTH numbers by the same power of 10 to make the divisor whole.','4.8 divided by 0.6 = 48 divided by 6 = 8.'),
 text('Order of operations','1. Grouping symbols, such as parentheses. 2. Exponents.','3. Multiply and divide from left to right.','4. Add and subtract from left to right.','Example: 18 - 6 divided by 3 x 2 = 18 - 2 x 2 = 18 - 4 = 14.')])
sheet('time-and-money','Time & money','1-3','Math','Take one step at a time. Label minutes, hours, cents, or dollars.',[
 table('U.S. coins',[['Penny','Nickel','Dime','Quarter'],['1 cent','5 cents','10 cents','25 cents']]),
 text('Count money','Start with the largest coin value and count on.','1 quarter + 2 dimes + 1 nickel = 25 + 10 + 10 + 5 = 50 cents.','100 cents = $1.00. $2.35 means 2 dollars and 35 cents.'),
 text('Read an analog clock','The short hand tells the hour. The long hand tells minutes.','Each number marks 5 minutes: 1 = 5, 2 = 10, 3 = 15 ... 12 = 0.','At 3:30, the minute hand points to 6; the hour hand is halfway from 3 to 4.'),
 text('Time facts','60 seconds = 1 minute. 60 minutes = 1 hour. 24 hours = 1 day.','A quarter hour is 15 minutes. A half hour is 30 minutes.'),
 text('Find elapsed time','From 2:45 to 3:20: 15 minutes to 3:00, then 20 minutes more.','15 + 20 = 35 minutes. Use a timeline to track the jumps.')])
sheet('word-problem-steps','Word problems: a calm plan','1-6','Math','You do not have to solve it all at once. Start with what you know.',[
 text('1. Read and tell the story','Read once. Say what is happening in your own words.','Circle the question. What are you trying to find?'),
 text('2. Find the useful information','Label each amount. Cross out information you do not need.','Draw objects, a bar model, a table, or a number line.'),
 text('3. Choose a plan','Are amounts joining, separating, being compared, or forming equal groups?','Write an equation. Do not choose an operation from one keyword alone.'),
 text('4. Solve one step at a time','Show your work. Use a chart or a familiar fact if you need one.'),
 text('5. Check and label','Does your answer fit the story? Check with a drawing or another method.','Write a sentence with the correct unit.'),
 text('Example','Mia has 3 bags with 4 shells in each. She gives away 2 shells.','3 x 4 = 12 shells. 12 - 2 = 10 shells. Mia has 10 shells left.')])
sheet('nouns','Nouns: name it','K-3','English','A noun names a person, place, thing, or idea.',[
 table('Find the noun',[['Person','Place','Thing','Idea'],['teacher','school','pencil','kindness'],['friend','park','dog','courage']]),
 text('Common or proper?','A common noun names a general person, place, thing, or idea: city, student.','A proper noun names a specific one: Chicago, Maya. Use a capital letter.'),
 text('One or more than one','Singular: one cat. Plural: two cats.','Usually add -s: book/books. Often add -es: box/boxes.','Consonant + y: baby/babies. Some change: child/children, mouse/mice.'),
 text('Show ownership','One dog: the dog\'s bowl. More than one dog: the dogs\' bowls.','Irregular plural: the children\'s books.'),
 text('Try it','The teacher carries a book to school.','Nouns: teacher (person), book (thing), school (place).')])
sheet('verbs','Verbs: action & being','1-4','English','A verb tells what happens or connects the subject to information about it.',[
 text('Action verbs','A penguin waddles. The class reads. We built a tower.','Waddles, reads, and built tell what someone or something does.'),
 text('Linking verbs','The soup is warm. The flowers smell sweet.','Is and smell connect the subject to a description.'),
 text('Helping verbs','She is reading. They have finished. We will go.','Is, have, and will help the main verb.'),
 table('Past, present, future',[['Past','Present','Future'],['Yesterday I walked.','Today I walk.','Tomorrow I will walk.'],['Yesterday I went.','Today I go.','Tomorrow I will go.']],[176,176,176]),
 text('Match subject and verb','One bird sings. Two birds sing.','I am. You are. He/she/it is. We are. They are.'),
 text('Try it','Lena has packed her bag. Helping verb: has. Main verb: packed.')])
sheet('adjectives-adverbs','Adjectives & adverbs','2-5','English','Use describing words to make a sentence more precise.',[
 text('Adjectives describe nouns or pronouns','Ask: What kind? Which one? How many?','The small penguin found three smooth stones.','Small describes penguin. Three and smooth describe stones.'),
 text('Adverbs describe verbs, adjectives, or other adverbs','Ask: How? When? Where? To what extent?','The penguin waddles slowly. Slowly tells how it waddles.','The water is very cold. Very describes the adjective cold.'),
 table('Compare carefully',[['One','Compare two','Compare three or more'],['small','smaller','smallest'],['careful','more careful','most careful'],['good','better','best']],[176,176,176]),
 text('Do not rely only on -ly','Quickly is an adverb, but friendly is usually an adjective.','Fast can be either: a fast runner (adjective); runs fast (adverb).'),
 text('Quick check','Ask which word is being described. Then choose the word that fits.')])
sheet('pronouns','Pronouns & clear sentences','1-4','English','A pronoun can take the place of a noun. Make it clear who or what it means.',[
 table('Choose a pronoun',[['Subject: does the action','Object: receives the action'],['I, you, he, she, it, we, they','me, you, him, her, it, us, them']],[264,264]),
 text('Subject or object?','Maya and I read. I is part of the subject.','The teacher helped Maya and me. Me is part of the object.','Check by removing the other name: I read. The teacher helped me.'),
 text('Possessive words show belonging','My/your/his/her/its/our/their come before nouns: our books.','Mine/yours/his/hers/ours/theirs can stand alone: The books are ours.'),
 text('Its or it\'s?','Its shows belonging: The bird spread its wings.','It\'s means it is or it has: It\'s raining.'),
 text('Make the meaning clear','Unclear: Sam told Lee that he won. Which person won?','Clear: Sam told Lee, "You won." Or: Sam told Lee, "I won."')])
sheet('sentences-punctuation','Sentences & punctuation','K-3','English','A complete sentence shares a complete thought.',[
 text('Build a sentence','Tell who or what (subject). Tell what happens or what is true (predicate).','The little dog / sleeps on the rug.','Begin with a capital letter. End with a punctuation mark.'),
 table('Choose an ending',[['Type','Example'],['Statement: tells something','The dog is asleep.'],['Question: asks something','Where is the dog?'],['Exclamation: strong feeling','What a surprise!'],['Command: tells someone to act','Please close the door.']],[250,278]),
 text('Commas can separate a list','I packed a book, a snack, and a pencil.'),
 text('Apostrophes have jobs','Contraction: do not becomes don\'t.','Ownership: the cat\'s toy. Do not add an apostrophe just to make a plural.'),
 text('Read it aloud','Does it make sense? Is the thought finished? Check the first and last marks.')])
sheet('writing-checklist','My writing check','2-6','English','Read your writing one small part at a time.',[
 text('1. Meaning','What is my main idea? Did I answer the question?','Add a detail or example to help the reader understand.'),
 text('2. Order','Does my beginning introduce the idea?','Do my details follow an order? Does my ending finish the thought?'),
 text('3. Sentences','Read each sentence aloud or ask someone to read it to you.','Does each sentence make sense? Join or separate thoughts where needed.'),
 text('4. Capitals and punctuation','Check the first letter, names, and the word I.','Check sentence endings, commas, and apostrophes.'),
 text('5. Spelling and word choice','Mark words you are unsure about. Use a word bank or dictionary.','Check words that sound alike: their/there/they\'re and to/too/two.'),
 text('6. One final look','Check spaces, readable handwriting or text, and your name if needed.','Choose one improvement. A small change can make your message clearer.')])
sheet('connecting-ideas','Connecting ideas','4-6','English','Use connecting words to show how ideas belong together.',[
 text('Coordinating conjunctions','For, and, nor, but, or, yet, so can join words, phrases, or clauses.','I wanted to play, but it was raining.','Use a comma before the conjunction when it joins two complete sentences.'),
 text('Subordinating conjunctions','Because, although, if, when, and while begin dependent clauses.','Because it was raining, we played inside.','We played inside because it was raining.','A dependent clause does not usually stand alone as a complete sentence.'),
 text('Prepositions show relationships','In, on, under, beside, before, after, and with can begin prepositional phrases.','The book is under the desk. We walked after lunch.'),
 text('Transitions guide the reader','Order: first, next, finally. Example: for instance.','Contrast: however. Cause/result: therefore. Add information: also.'),
 text('Check the connection','Choose a connector that matches your meaning. Read the sentence to check that the ideas still fit.')])

def watermark(c,doc):
    c.saveState();c.setFillColor(colors.HexColor('#eeeeee'));c.translate(306,382);c.rotate(32);c.setFont('Helvetica-Bold',114);c.drawCentredString(0,0,'OPP');c.restoreState()
    c.setStrokeColor(colors.HexColor('#b9c6c7'));c.line(42,43,570,43)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#47565d'))
    c.drawString(42,29,'OPP | Origami Penguin Publishing | Free for home and classroom use')
    c.drawRightString(570,29,'origamipenguin.com/free-resources')

def make_pdf(s):
    path=OUT/(s['slug']+'.pdf')
    doc=SimpleDocTemplate(str(path),pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=56,title=s['title']+' | OPP',author='Origami Penguin Publishing',pageCompression=1)
    story=[Paragraph(s['title'],styles['TitleOPP']),Paragraph('QUICK REFERENCE | Suggested grades '+s['grades']+' | '+s['subject'],styles['SubOPP']),Paragraph(s['intro'],styles['TextOPP'])]
    for b in s['blocks']:
        pieces=[]
        if b['heading']:pieces.append(Paragraph(b['heading'],styles['HeadOPP']))
        if 'lines' in b:pieces.extend(Paragraph(line,styles['TextOPP']) for line in b['lines'])
        else:
            data=[[Paragraph(str(cell),styles['CellOPP']) for cell in row] for row in b['rows']]
            if s['slug']=='multiplication-chart':
                data=[[str(cell) for cell in row] for row in b['rows']]
            t=Table(data,colWidths=b.get('widths') or [528/len(data[0])]*len(data[0]),hAlign='LEFT')
            commands=[('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eeee')),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#142b35')),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#aebbbf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]
            if s['slug']=='multiplication-chart':commands.extend([('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),11),('ALIGN',(0,0),(-1,-1),'CENTER'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#e7eeee')),('LEFTPADDING',(0,0),(-1,-1),1),('RIGHTPADDING',(0,0),(-1,-1),1),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])
            t.setStyle(TableStyle(commands));pieces+=[t,Spacer(1,6)]
        story.append(KeepTogether(pieces))
    doc.build(story,onFirstPage=watermark,onLaterPages=watermark)
    assert len(PdfReader(path).pages)==1,s['slug']+' overflowed'
    subprocess.run(['pdftoppm','-singlefile','-scale-to','850','-jpeg','-jpegopt','quality=82',str(path),str(PREVIEW/s['slug'])],check=True,capture_output=True)
    return path

def main():
    for s in S:make_pdf(s)
    writer=PdfWriter()
    for s in S:writer.append(str(OUT/(s['slug']+'.pdf')))
    writer.add_metadata({'/Title':'OPP Free Reference Sheets - Complete Collection','/Author':'Origami Penguin Publishing'})
    with (OUT/'opp-reference-sheets-complete.pdf').open('wb') as f:writer.write(f)
    manifest=[{k:v for k,v in s.items() if k!='blocks'} for s in S]
    (ROOT/'content/free-resources.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    body='<section class="resource-intro"><p class="eyebrow">A little reminder goes a long way</p><h2>Keep a helpful page close by.</h2><p>Free, one-page reference sheets for K-6 learners. Use them beside homework, in a binder, or at a classroom station. Clear steps and worked examples help students return to an idea when they need a reminder.</p><p>Grade ranges are suggestions, not limits. Choose the sheet that fits the learner. Each PDF is US Letter size with a light OPP watermark, and works in black and white. No email or signup needed.</p><p><a class="btn" href="/resources/opp-reference-sheets-complete.pdf" download>Download all 19 sheets (PDF)</a></p><p class="resource-note">Open any PDF to preview or print. Choose Actual size / 100% on US Letter, or Fit for A4. Each individual PDF is one page. Free for personal, home, and classroom use; please keep the OPP credit and do not resell these sheets.</p></section><nav class="resource-jumps" aria-label="Resource subjects"><a href="#math">Math reminders</a><a href="#english">English &amp; writing</a></nav>'
    for subject in ['Math','English']:
        body+='<section id="'+subject.lower()+'"><h2>'+('Math reminders' if subject=='Math' else 'English &amp; writing')+'</h2><div class="resource-grid">'
        for s in S:
            if s['subject']!=subject:continue
            base='/resources/'+s['slug']+'.pdf'
            body+='<article class="resource-card"><a href="'+base+'" target="_blank" rel="noopener" aria-label="Preview '+e(s['title'])+' PDF"><img src="/images/resources/'+s['slug']+'.jpg" alt="Preview of the '+e(s['title'])+' reference sheet" width="657" height="850" loading="lazy" decoding="async"></a><div><p class="resource-grade">'+e(subject)+' · Suggested grades '+e(s['grades'])+'</p><h3>'+e(s['title'])+'</h3><p>'+e(s['intro'])+'</p><p class="resource-links"><a href="'+base+'" target="_blank" rel="noopener">Preview / print PDF</a><a href="'+base+'" download>Download</a></p></div></article>'
        body+='</div></section>'
    body+='<aside class="resource-note"><h2>Use a sheet in small steps.</h2><p>Start with one heading. Read the example together, try a similar question, then point back to the reminder when needed. Students can keep using a reference while they build confidence and fluency.</p><p>For more learning materials, explore our <a href="/textbooks">textbooks and educational books</a> or <a href="/origami-for-teachers">origami ideas for teachers</a>.</p></aside>'
    css='.resource-intro{background:#edf3ef;padding:28px;border-radius:12px;margin:20px 0 26px}.resource-intro h2{font:500 clamp(1.7rem,4vw,2.4rem)/1.25 Georgia,serif;color:#18394a}.resource-note{font-size:.94rem;line-height:1.7;padding:18px 0}.resource-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin:20px 0 40px}.resource-card{border:1px solid #ccd8d6;border-radius:10px;overflow:hidden;background:#fff}.resource-card>a{display:block;background:#edf1f0;padding:16px}.resource-card img{display:block;width:100%;height:auto;border:1px solid #ced5d3;box-shadow:0 3px 9px #18394a18}.resource-card>div{padding:18px}.resource-card h3{font:600 1.2rem/1.3 Georgia,serif;margin:8px 0 12px;color:#18394a}.resource-grade{font-size:.78rem;color:#47625e;font-weight:700}.resource-links{display:flex;flex-wrap:wrap;gap:12px;font-size:.9rem}.resource-jumps{display:flex;gap:20px;margin:20px 0}.resource-card p{line-height:1.6}@media(max-width:850px){.resource-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:540px){.resource-grid{grid-template-columns:1fr}.resource-intro{padding:20px}}'
    page=dict(slug='free-resources.html',title='Free K-6 Printable Reference Sheets | Origami Penguin',description='Free one-page K-6 printable math and English reference sheets: multiplication, fractions, conversions, grammar and step-by-step reminders. No signup required.',heading='Free Resources',nav='resources',breadcrumbs=[dict(name='Home',url='/'),dict(name='Free Resources')],body=body,styles=css)
    from resource_filters import enhance_resources
    page=enhance_resources(page,S)
    assert len(S)==19
    (ROOT/'content/pages/free-resources.json').write_text(json.dumps(page,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Created',len(S),'one-page sheets, complete pack, and resource page data.')

if __name__=='__main__':main()
