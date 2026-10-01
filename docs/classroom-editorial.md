# Classroom content and product publishing

## Current content

The two original classroom articles are stored in `content/pages/` and rendered by the shared site template:

- `origami-for-teachers.json`: an approximately 18-minute, two-square symmetry and fractions lesson, adaptations, assessment prompts and a browser-printable student task
- `origami-paper-for-classrooms.json`: a task-based paper selection guide with sheet-count and usable-cost examples

Each page uses this shape:

- `slug`: unique public filename ending in `.html`
- `title`: browser/search title; the renderer can add the site name
- `description`: accurate plain-text summary
- `heading`: one visible page heading
- `nav`: active navigation category, `teachers` or `supplies`
- `breadcrumbs`: ordered objects with `name` and local `url`
- `body`: trusted, editorially reviewed HTML fragment beginning with an introductory paragraph; section headings begin at h2, with no additional h1
- `kind`: `article`

The activity is original educational content, not a tested intervention or a claim of standards alignment. It deliberately separates mathematical understanding from fine-motor precision. Timing is a classroom planning estimate. Paper quantities and dollar figures are explicitly worked examples, not live product offers. Print guidance uses the browser; no downloadable worksheet or scripting is claimed.

## Product catalog status

`content/products.json` deliberately contains only two empty arrays:

```json
{
  "pressBooks": [],
  "teacherResources": []
}
```

There are no verified origami titles or resource listings ready to publish. Ownership of a publishing imprint or teacher marketplace account does not establish a product's existence, availability or URL. Do not display empty product cards, invented book covers, fabricated reviews, sample purchase links, fake free downloads, or “coming soon” promises based on these arrays.

## Proposed future item schema

This is a documented proposal for adding verified items, not a promise that the current renderer supports product cards. Implement and validate rendering before filling the arrays.

Common fields for each future item:

| Field | Type | Publication rule |
| --- | --- | --- |
| `id` | string | Stable, unique local identifier |
| `title` | string | Exact title verified against the actual listing |
| `description` | string | Original, factual summary of the actual contents |
| `url` | string | Verified HTTPS product or resource-detail URL; never a guessed store slug |
| `format` | string | Actual offered format, such as paperback or printable PDF |
| `verifiedAt` | string | ISO date of the last listing and destination check |
| `image` | string, optional | Existing local image path with documented permission to use the cover or preview |
| `imageAlt` | string, required with image | Useful accessible description |
| `audience` | string, optional | Verified intended audience; do not invent age, grade or curricular alignment |

Additional `pressBooks` fields may include `author`, `publisher`, and `isbn`, when the exact edition has been verified. Additional `teacherResources` fields may include `platform`, `includedFiles`, and `pageCount`, when visible in or confirmed for the actual resource. Omit unknown fields rather than inventing a value. Do not populate prices or “free” labels without a specific plan for keeping them accurate.

## Checks before publishing any catalog item

1. Confirm that the actual item exists and that the owner has authorized it to be featured
2. Open the exact destination and confirm the title, creator/imprint, format, availability and intended audience
3. Confirm that preview images are authorized and that the delivered file or product matches the description
4. Check all item links and local image paths; do not invent merchant IDs, ISBNs or marketplace storefront URLs
5. Use the site's appropriate commercial disclosure; mark affiliate links as sponsored and preserve referral parameters intentionally
6. Do not claim reviews, credentials, endorsements, standards alignment or learning outcomes without adequate evidence
7. Test the new item on desktop, mobile and keyboard navigation; check image alternatives and purchase-link wording
8. Add Product or Offer structured data only when the visible, verified content and applicable required fields support it
9. Record the verification date and provide a way to remove or update stale listings

## Ongoing classroom editorial checks

- Physically test fold instructions before describing a model as classroom-ready; the current two-square activity can be checked by matching edges and corners
- Distinguish an equal-area partition from a line of reflection symmetry
- Keep the original whole explicit when comparing fractions; A and B must start the same size
- Recheck arithmetic and give sheet-count assumptions next to each example
- Keep new classroom pages substantive and distinct instead of generating keyword variations
- Preview browser printing after template changes, including the entire student task and answer prompts
- Review linked legacy product recommendations separately; these new pages do not verify or endorse any particular listing
