# Penguin tutorial quality review - 1 October 2026

## Decision

Hold corrected folding instructions and replacement diagrams until a physical test establishes a complete sequence. This was a source, diagram-pixel and reference review, not a physical fold test. Changing only "up" to "down" would conceal unresolved problems.

The safe public change is a visible review notice, including in print, and removal of this page's HowTo structured data while it is under review. Existing step text and image pixels are preserved. Metadata now describes the review status instead of promising a reliable beginner result. Homepage and tutorial-directory penguin promotions disclose the review, and the homepage's first action leads to the beginner's guide. No model designer or rights holder is guessed.

## Evidence from the existing image and text

Inspected both the original 1408 x 768 JPEG and the displayed WebP. The illustration contains ten panels in two rows. It has no visible designer credit or rights statement. Repository review also found no model-specific attribution; absence of a credit does not establish ownership or a traditional design.

| Location | Observed problem | Required check |
| --- | --- | --- |
| Steps 2-3 | Text unfolds twice. Panel 2 marks a diagonal, but panel 3 depicts horizontal/vertical lines without explaining a rotation or extra fold. | Choose a fixed starting orientation; photograph the actual crease after unfolding. |
| Step 4 | Text says edges meet at the centre; the image leaves a broad central region and gives several arrows without a clear before/after state. | Identify the exact edges and whether they meet or leave a gap. |
| Steps 5-6 | Step 5 folds a bottom point up. Step 6 heading says up, body says down, and image presents a side-like shape without explaining its relationship to the previous front view. | Establish which layer/point moves, its direction, crease landmarks and any turn-over. |
| Steps 7-8 | Step 7 closes the model; step 8 says inside reverse fold, while heading and body also disagree about back/forward. | Physically establish inside versus outside reverse fold and show the opening/closing operation. |
| Steps 9-10 | Panel 9 returns to a front-like view. Final picture has feet/tail details not clearly created by the described wing fold. | Demonstrate all shape changes and a real finished model; do not use the illustration as proof of the result. |

## References checked

These are comparison sources, not permission to copy diagrams and not evidence that our illustration depicts their models.

- [WWF's own Penguin PDF](https://www.worldwildlife.org/documents/1196/2ct7k7pm83_WWF_Together_PenguinOrigami.pdf), linked from its [origami activity page](https://www.worldwildlife.org/resources/activities/origami-patterns/): identifies a traditional design and credits WWF, copyright 2013. Its sequence explicitly includes turn-overs, a head pre-crease, an outside reverse fold, a bottom reverse fold and a beak crimp. Those operations are not equivalent to our ten captions. PDF text was inspected; local PDF retrieval returned 403, so no claim of visual verification of every WWF panel is made.
- [Origami.me's traditional penguin](https://origami.me/penguin/): Peter Saydak's tutorial credits diagrammer Kelly Tan. It specifies a gap between folded edges, a turn-over and an outside reverse fold for the head. It is a useful candidate reference for a simpler replacement after physical testing, not a verified match for our illustration.
- [Jo Nakashima's own penguin page](https://jonakashima.com.br/2015/07/13/origami-penguin/): explicitly credits his April 2011 design and describes it as low intermediate; his revised 2023 diagrams add reference points. This is a separate authored model, not a basis for silently attributing or repairing ours.

No external diagram, screenshot or tutorial text was added to site assets. No AI replacement image was generated: plausible-looking geometry would not verify folding correctness. Existing copyright/footer and affiliate identities remain intact.

## Draft correction brief and hands-on questions

1. Confirm the intended model and the original illustration's creator/source and permitted use. If unavailable, choose a documented traditional model and make original photographs and original wording from a real fold.
2. Use a 15 cm two-colour square. Record the starting colour facing up and the corner pointing upward. Photograph every before/after state with consistent orientation.
3. Resolve steps 2-4 first: is the centre crease vertical in the working view, which edges move, and do they meet or leave a gap?
4. At steps 5-6, identify the moving tip/layer and crease endpoints. Does it move up or down? Is a turn-over or rotation missing? Do not approve the heading change in isolation.
5. At steps 7-10, verify the reverse-fold type and show how the beak, flippers, feet and any tail actually form. Replace the finished illustration with an owned photo of that exact model.
6. Have a beginner follow only the proposed words and pictures. Record stalls and corrections, then rerun the full sequence with the revised instructions. Record reviewer/date, paper and outcome in the tutorial record before setting `fold-tested`.

Parent/owner handoff: please arrange this hands-on fold and provide the intended model/source plus photos of the ambiguous transitions. Until then, publish no corrected sequence or replacement diagram. The public review notice may remain in place.

## Phone and print checks

Headless desktop Chrome rendered all 18 HTML content/error pages at 320, 375, 414 and 499 CSS pixels (72 combinations): no horizontal document overflow, off-screen non-positioned elements or broken images. Screenshots cover home, penguin, supplies and teacher activity at 320/375. This is viewport emulation, not real phone hardware, Safari, touch or screen-reader testing.

Actual Chromium PDF rendering used A4 and US Letter with 12 mm margins, browser headers/footers off and background graphics off. Baseline outputs: penguin 3 pages, heart 2, crane 2 and teacher activity 4, in each size. Navigation/shopping tutorial sections were hidden; inspected penguin pages retained intact step cards. The teacher student task starts on its own page. The all-in-one penguin image is visually too dense for a narrow screen; because its sequence is unverified, it was not promoted or redrawn as a fix. Future owned step photos should be individually readable.

Build/test portability: explicit UTF-8 reads/writes fix the Windows default-codepage failure. Site generation remains dependency-free; optional browser/PDF QA dependencies stay outside the repository.

## Recovery

The starting upstream commit was freshly confirmed as `c5e4bfcd2f090edcb003bac795158abc8f2aaffe`. Remote branch `backup/pre-penguin-quality-20261001` preserves it. A source archive and untouched extracted baseline are preserved in the task workspace; isolated edits live in `work/`. The local snapshot commit is not upstream Git history. Revert this phase's actual upstream commit through the existing Git deployment workflow to undo it; never force-push or change Cloudflare settings. See [existing rollback guidance](rollback.md).
