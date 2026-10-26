# Heart replacement: fold-test draft, 2026-10-25

Base: e4202e9ea0ba82848db40349694c85124cc2e772. Local rollback branch: backup/pre-illustrated-tutorials-20261025.

## Scope

Replaces the incomplete heart with 11 original instructions and 11 deterministic SVG before/after diagrams. Starting orientation, both centre precreases, the NEW top edge target, lower-edge alignment, layer selection, turnovers and shaping folds are explicit. The page includes a diagram legend, individual vector zoom links, source notes and a printable physical-test record. Status remains needs-review; no HowTo structured data, speed or difficulty endorsement is emitted. At this heart-only checkpoint, crane and penguin were unchanged; see their later fold-test audits and reviewed-tutorial-release.md for the combined release.

## Geometry evidence

Starting diamond coordinates are top (0,-1), right (1,0), bottom (0,1), left (-1,0), with y downward. Top crease y=-0.5 maps top tip to centre. Bottom crease y=0.25 maps bottom tip to (0,-0.5), the midpoint of the NEW top edge. Right lift x+y=0.25 and left lift -x+y=0.25 align the lower half-edges on x=0. Right crease meets the upper-right slope at (0.625,-0.375). Side shaping creases x=+/-0.5; top caps y=-0.625. The final bounds are x=[-0.5,0.5], y=[-0.625,0.25].

scripts/heart_geometry.py clips and reflects each paper polygon, reverses moved-layer order and swaps face colours. Turnovers reverse all layers and reflect x. Total paper-layer area remains 2 through every state. This model ignores thickness, stiffness, friction and hand access; area conservation alone does not prove foldability.

Independent reviewer heart_review checked actual code and prose: state indices, crease endpoints, arrows, reflected landmarks, layer ordering, final silhouette and sampled face visibility. It found missing reference creases and ambiguous whole-half/paper-size wording. Those were corrected. Final front is coloured; reverse is mixed, not uniformly white.

## Provenance

This is a widely taught flat-heart construction; original designer has not been confirmed. Do not claim invention or established traditional provenance. Text and vector geometry are independently authored; no publisher art was copied or traced. Publisher references retain their copyright:

- Japan Society educational PDF: https://www.japansociety.org.uk/usercontent/04782371b403dc3881a69411a8d673e6/OrigamiHeart.pdf
- Childhood Magic original tutorial: https://childhoodmagic.com/origami-heart/
- Parent reviewer independently consulted Stanford DREME: https://familymath.stanford.edu/app/uploads/2023/12/DREME-Origami.pdf

## Software and browser validation

12 unittest tests pass: 9 existing site checks plus landmark reflection, area/bounds, and diagram-generation/step correspondence. Existing checks cover internal links/fragments, generated-page freshness, affiliate tracking and absence of new tracking. All 11 SVGs load in Chrome local preview. Desktop viewport 1175px and mobile 375px have no horizontal overflow. Desktop central fold and final front/back views and mobile step 6 inspected. Small mobile diagrams have explicit links to open the vector for zooming. All draft diagrams load eagerly so print does not depend on scroll-triggered image loads.

Print CSS preserves the warning, uses break-inside avoidance for steps and starts the test record on a new page; zoom links are hidden in print. Actual paginated print preview remains NOT VERIFIED: supported browser Control+P input returned without showing print UI. No PDF export or paper print has been checked. No physical fold or beginner test has occurred. No publication performed.

## Required physical test

Print the heart tutorial with its warning and record sheet. Record tester/date, paper size along each side and paper type. Use a thin two-colour 15x15cm square; photograph each numbered state. Check step4 centre contact; step5 contact at NEW top-edge midpoint; steps6-7 all required layers move and lower half-edges meet on centreline; step8 is a turnover keeping bottom down; steps9-11 shaping flaps remain behind, notch stays open and heart lies flat without glue. Record the FIRST mismatch in wording, arrows, colour, layer order or orientation. Ask a second beginner to follow only this page. After any corrections repeat the entire sequence before marking fold-tested. Physical evidence is required to lift the review gate.
