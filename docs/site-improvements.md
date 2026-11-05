# Visitor discovery and aggregate usage

The homepage now leads to Read, Learn, Create, Relax and Play. Games are linked through /games; their existing game files and logic are unchanged. The site-experience module adds related links to resource cards, book hubs, selected teaching pages and all 52 journal articles.

## Resources and packs

Search, grade, subject and topic filters combine; the query string can preserve/share a selection. Search text is never sent to the counter endpoint. Grade packs reuse the exact original sheets, with one new parent/teacher guide as the first page. Regenerate packs using scripts/create_resource_packs.py with the bundled PDF environment; normal builds use checked-in files. All seven packs have been checked for the right sheet order and page count.

## Chill Corner

Video type, duration, sound and search filters combine. The default selection of a long session queues long sessions only; selecting a Short queues Shorts. The two dedicated shuffle buttons use all long sessions or all Shorts respectively; Shuffle filtered videos deliberately uses the exact visible set, which can mix types when All videos is selected. Changing filters does not replace the existing iframe. Sound labels are descriptions inferred from the verified titles; mixed instrumental/nature scenes are placed with music/tones. Not a guarantee of any therapeutic effect.

## Usage counts

Cloudflare Pages Function /api/events accepts only known page, PDF, ASIN and video identifiers generated in lib/metric-targets.js. It stores daily aggregate counts in the D1 database origamipenguin-usage (binding USAGE_DB). No visitor IDs, cookies, full URLs, search terms, IP addresses or emails are stored by the counter. DNT and GPC signals skip collection. Hosting logs are separate. These are action counts, not unique visitors, completed downloads, purchases or watch-time measurements; repeat clicks, bots and blockers affect totals.

The API has no public read endpoint. The owner can view the D1 database in Cloudflare or request a report in this chat. Useful query:

```sql
SELECT event,target,SUM(total) AS actions FROM daily_counts
WHERE day >= date('now','-30 days') GROUP BY event,target
ORDER BY event,actions DESC;
```

No credentials are in the repository. Previews and localhost skip sending usage events. Pages routes limit Function execution to /api/events; normal pages/assets remain static. The current production database ID is 631204a9-ce3d-46ff-af52-4ed007f0c852. No email addresses belong in this database.

## Monthly email: prepared, not collecting

The user does not have a mailing service yet. content/newsletter.json has a null signupUrl, so no fake signup or disabled form appears on the public site. docs/newsletter-preview.html shows the prepared design. Setting a valid public HTTPS hosted signup URL in the config will add the optional invitation on the homepage, resource hub and article hub. Before enabling it, update privacy.html with the actual provider and use a confirmed/double-opt-in signup with an adult audience, a verified sender, and an unsubscribe link in every email.

Suggested setup: create a Brevo account, make an Origami Penguin Monthly Updates list, then create a hosted signup form. Use the preview's title and copy, collect email only, select double opt-in, and supply the sender/organization details requested by the provider. Return the hosted form URL for connection. No campaign is scheduled or sent by this website update.

Shorts/mixed queues use the YouTube IFrame API after user selection to advance on the ended event, with explicit previous/next buttons. Long-only queues use the built-in playlist. Stopping invalidates pending API loads so old sessions cannot restart. Counters use UTC day buckets; initial counts include the deployment verification session.
