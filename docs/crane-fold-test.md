# Crane schematic fold-test draft

2026-10-25. Draft following heart commit 49826d0c5de04f06b406b418113a480ea1692913. Independent second review passed for release as a clearly labelled schematic, physically untested draft.

26 original step texts and deterministic schematic SVGs now exist. The text restores opposite precrease polarity, closed-top/open-bottom square-base orientation, complete front/back petal precrease-and-unfold cycles, bird-base flap identification, narrowing both faces, separate inside reverse folds for both neck/tail points, beak reversal and broad wing opening.

Independent mechanics review chose the conventional inside-reverse method from Web Japan/NIPPONIA, whose diagram consultant is ORIGAMI HOUSE. Origami.me currently uses an alternate book-fold/swivel setup; that method was not mixed into this draft. Publisher art was not traced or copied.

Exact base landmarks: with diamond top (0,-1), right (1,0), bottom (0,1), left (-1,0), k=sqrt(2)-1 and a=2-sqrt(2). Side precreases x=+/-k(1-y) meet upper edges at (+/-a,-k). Top cross-crease y=-k. Raised petal point is (0,1-2sqrt(2)). These flat landmarks were independently derived. Whole-stack reflection does NOT model the pocket opening or establish all hidden-layer ordering.

Second review identified and corrected four actual defects: reversed edge-fold arrow, unchanged rear apex during the stack precrease, obsolete rear-square corners on the second face, and missing neck/tail reversal hinges. Step14 now uses the existing cross-crease rather than folding the completed long petal. A later small diagram improvement adds corner-convergence arrows to the initial collapse.

Validation: 15 unittest tests pass, including 3 crane tests for base/petal/reverse landmarks, selected-face area conservation and all26 diagrams matching their generator. All26 browser images loaded; desktop central pocket view and mobile375px inspected with no horizontal overflow. Individual vector zoom links are available because small mobile diagrams need enlargement. The 28-page vector PDF was rendered with Poppler; every page inspected in contact sheets, with enlarged collapse, petal, reversal, head and wing views. Exact instruction text was checked from the generated PDF. Browser print pagination itself is not verified; the separate PDF has been rendered and checked.

Reviewer verdict: PASS as a schematic crane fold-test draft. This is NOT complete physical or beginner verification. Initial collapse has movement arrows but no full intermediate 3D mesh; pocket/reversal insets omit hidden layers, and final wing pose is illustrative. Physical tests must focus on one-flap selection, reversing pocket creases without tearing, separate lower legs, points remaining between wings, beak reversal and wing opening. Status remains needs-review; no HowTo schema is emitted.

At this crane-only checkpoint, the earlier heart-only payload excluded crane and penguin. Penguin was rebuilt subsequently; see penguin-fold-test.md and reviewed-tutorial-release.md for the combined release.
