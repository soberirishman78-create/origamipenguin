# Creative Notebook and Chill Corner

The 52 original short articles in `content/journal.json` reflect on the ongoing work of building Origami Penguin, including fiction, narration, publishing, resource development, catalog organization, games and ambience videos. They were prepared from the owner's project conversations and records at the owner's request. They do not claim a year of historical weekly publication, invented personal feelings, classroom trials, human-only authorship, or business results. Private account information and financial figures are omitted.

All new articles are dated November 4, 2026. The numbered order is a suggested weekly reading sequence, explicitly distinguished from publication history. Existing origami article URLs and tutorials remain available and are linked from the new Articles hub.

`scripts/journal_pages.py` generates the hub, 52 article records and Chill Corner. `scripts/build.py` incorporates those records into the existing static build and sitemap. To revise content, edit the journal JSON or renderer and run the normal build and tests. Do not hand-edit generated HTML.

`content/relaxation-videos.json` stores 12 video destinations and thumbnails verified through public video metadata on November 4, 2026. They belong to Relaxation Station Ambience, channel ID UCnt0WRg-Cv8RdcRQ011L1DA, handle @relaxationstationloops. The page provides one shared on-site YouTube player. Clicking a video card or Play here loads that video; no iframe is loaded and no sound starts on page arrival. The iframe uses YouTube privacy-enhanced embedding, inline playback, native controls and explicit referrer policy. Switching videos replaces the existing iframe; Stop video removes it. Direct YouTube links remain as a fallback. Card summaries describe the sound and duration, without promising therapeutic outcomes or advertising availability.

Tests cover series completeness, substantive distinct paragraphs, publication dates, hub membership, previous/next navigation, preserved origami links, and verified-channel video coverage, alongside the existing site checks.

Continuous listening: the embed queues the remaining unique card video IDs in page order, wraps around from the selected starting video, and repeats the collection with YouTube playlist/loop parameters. Page arrival is still silent; Stop removes the whole playlist. The heading and external fallback identify the session/starting video rather than claiming to track the currently playing item.
