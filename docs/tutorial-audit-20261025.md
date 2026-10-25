# Tutorial pathway audit — 25 October 2026

## Verified starting state

Current origin/main: `1b2d71799f7876a3d8e9b69a4a239edc8a1c191b`. Fresh isolated clone on DESKTOP-NN0GELM; the October 1 working checkout was clean and left untouched. No repository AGENTS.md or .agents skills were present; the parent Codex AGENTS.md was read.

The earlier supplies referral fix is already present in source and in a direct HTTP 200 response from https://origamipenguin.com/supplies. It no longer recommends the penguin as a first project. The live HTML differs by an existing injected Cloudflare Insights beacon; this change neither adds nor modifies that service. Source-only absence of a collector must not be read as proof that production has no analytics.

The current commit has successful Cloudflare Pages, GitHub Pages build/deploy and validation checks. Root static HTML deployment and existing integrations are retained; no settings, credentials, DNS or production content were changed by this audit.

## Findings and proposed fixes

- Penguin: re-inspected the existing WebP against all ten captions. The prior review remains valid: diagonal versus orthogonal crease disagreement, duplicate unfolding, unexplained orientation changes, up/down and back/forward contradictions, and final details not demonstrated by the sequence. Do not patch a direction in isolation.
- Heart: step 2 forms a pointed top while step 3 refers to an unexplained bottom point. Later lobe/tuck transitions lack landmarks. There are no step images. The public page previously called this a quick, easy completed project despite the internal legacy-migrated review status.
- Crane: base collapse does not state orientation or opposing crease directions; petal folds are compressed; neck/tail raising is absent before shaping the head. No step images resolve these gaps. Comparing the independently authored illustrated crane resource confirms that a fuller sequence is needed, not that its design can silently replace ours.
- All three now show review status in headings/metadata, a visible explanation before the steps, and a link to illustrated alternatives. Existing instructions, image pixels, URLs and anchors are preserved. Unverified tutorials no longer emit HowTo schema or difficulty/time promises. Only a recorded fold-tested status enables those claims in the renderer.
- Homepage and directory describe heart/crane review status; supplies directs readers to the same useful starting point. The guide corrects the mountain-fold ridge explanation, distinguishes the moving paper from the crease profile, and offers illustrated resources instead of leaving beginners at a warning.

## References checked

Read on 25 October 2026: https://origami.me/beginners-guide/, https://origami.me/heart/, https://origami.me/crane/. These have on-page illustrated steps; the heart page also exposes a video link. The heart page was additionally opened in Chrome to inspect its step and image links. External PDFs or other features may require signup/payment, so only the on-page instructions are described as readable without signup. Links point to the original publisher; no diagrams, text sequences or media were copied. This is a desk review, not physical verification or an accessibility certification.

## Validation

- All 9 Python unittest checks pass, including generated-output freshness, internal links/fragments, metadata, schemas, asset references and exact original Amazon URL occurrence counts.
- Added regression coverage for visible review notices before steps, useful exit links, absent unverified HowTo/difficulty claims, directory/supplies routing and the three external reference links.
- Chrome local preview: home, guide, directory, supplies, all three tutorials and teacher activity at 320, 375 and 1280 CSS pixels (24 page/viewport combinations). No horizontal document overflow or broken images. Inspected mobile heart notice and guide resource section visually; clicked the tutorial resource link and verified the correct fragment destination.
- Computer/browser access worked; the previously reported quota block did not recur. Real phone hardware, Safari, screen readers, physical folding and a fresh print/PDF run were not tested. Existing print styles are unchanged and the review notice remains ordinary printable content.
- Unrelated Matrix and Deadwood files, affiliate URLs/disclosures, analytics scaffold, hosting configuration and assets are unchanged.

## Rollback and publication handoff

Local branch `backup/pre-tutorial-audit-20261025` preserves the starting commit. A full-history bundle at `../pre-tutorial-audit.bundle` passed `git bundle verify`. Changes are isolated on `fix/tutorial-review-pathways`.

No merge or production deployment is authorized yet. After approval, review this branch against current main, rerun `python -m unittest discover -s tests -v`, and merge through the existing GitHub workflow. Updating main triggers the existing hosting integrations; do not add a new build command or manually deploy with Wrangler. Wait for the exact resulting commit's Cloudflare check, then check the custom-domain home, guide resource anchor, all tutorial notices, supplies referral, affiliate links and missing-page behavior. Roll back only this change with a normal revert commit, preserving later unrelated work; never force-push main.

Before claiming a corrected model, physically fold the complete proposed sequence, resolve model attribution/rights, photograph each transition, and have a beginner follow only the revised instructions. Record reviewer, date, paper and outcome before marking fold-tested. The penguin-specific questions remain in `penguin-quality-review.md`.
