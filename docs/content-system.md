# Content system and quality gates

## Tutorials

The renderer reads `content/tutorials/*.json` for the three existing URLs. A tutorial supports heading/introduction, difficulty, duration and estimate note, recommended paper, materials, finished image, diagram, step text and optional step image, helpful tips, common mistakes, related projects, supply recommendations, educational connections, printable URL and video URL. Images require `src`, `alt`, `width`, `height`; step images load lazily. Optional media/commerce sections appear only when real values are supplied. Existing pages use a browser print layout with no signup barrier.

For a new tutorial, add its metadata to `content/site.json` and its structured record under `content/tutorials/`. Maintain a stable `.html` filename; public canonical links are extensionless. Use an accurate topic title and unique description. Do not fabricate a finished image, video, product, review, rating or availability claim. Duration is an estimate and appears as such.

Before publishing a new fold: make it from the exact instructions, have a second beginner follow it, reconcile every image with the text, confirm image/design rights, record the review in the tutorial JSON, then run the build and tests. `legacy-migrated` means the existing wording was retained, not physically tested. Do not treat a passing software test as a fold-quality review.

Known inherited content issue: penguin step 6 has an “up” heading but describes a downward fold. Its diagram and text need a hands-on orientation review; steps 2/3 also repeat unfolding. Crane and heart instructions are compressed and need matching step photos before promotion at scale. No new folding sequence was invented to conceal these limitations. Existing URLs and instructions remain available.

## Articles and education

New article records in `content/pages/` contain `slug`, `title`, `description`, `heading`, `nav`, `breadcrumbs`, `kind` and trusted editorial `body` HTML. The two first examples are a complete classroom lesson with printable student task and a classroom paper selection guide. They do not require an account or purchase to be useful.

Do not create thin taxonomy pages before there is enough material to browse. Future beginner, easy animal and seasonal clusters can start as sections in the existing tutorial directory. Separate hubs become appropriate as several verified tutorials exist in each cluster.

## Original products

`content/products.json` starts empty. Follow `classroom-editorial.md` when actual Origami Penguin Press titles or TPT resources are provided. Verify seller/store identity and destination before publishing. Suggested book titles are planning ideas, not available inventory. Do not display buy buttons for them.

## Affiliate links

Existing public Amazon URLs, including `origamipeng-20`, remain unchanged. Regression tests compare each original URL and occurrence count, and require sponsored/nofollow/noopener for tagged links. The Amazon privacy-policy URL is not an affiliate link. Do not visit affiliate links as synthetic conversion tests. Confirm tracking/reporting in the owner's account when supported access is available.

## Analytics and email

`js/outbound.js` remains unchanged: the empty endpoint makes it inert. There is no new data collection. No analytics collector was visible in the audited source; Cloudflare account-level analytics and historical reporting could not be confirmed. Preserve existing Search Console verification.

Do not add a signup form until the owner chooses or confirms an existing email provider and approves its account, privacy, consent and costs. A useful first free download is the classroom lesson/student task already available in the print layout. Next, prepare a small fold-tested beginner project collection. Require accessible signup, explicit consent, unsubscribe, a tested delivery email and a privacy-policy update before launch. Do not collect addresses into a nonfunctional form or silently enroll visitors.

A future outbound analytics implementation should measure only the needed event category, page path and product ID, avoid full URLs/identifiers, respect privacy choices, never delay navigation, and be verified against its real collection endpoint. Do not activate the old scaffold until the backend and privacy behavior are confirmed.
