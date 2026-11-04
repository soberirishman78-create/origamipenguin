# Jeremy Kelly book collection

`content/books.json` records the 120 distinct titles observed on Jeremy Kelly's Amazon all-books author page on November 4, 2026. The author page showed 121 listings; two Aeries Query Handbook listings are combined into one card with both destination links. The Kelly Brothers Mysteries group includes 22 numbered entries in series order and six additional adventures whose covers identify the series even though their Amazon titles omit it. Series membership is curated in the category and series fields, not inferred solely from listing titles. Fiction appears at `/books`; educational curricula and teaching guides appear at `/textbooks`, coloring and puzzles at `/coloring-puzzles`, journals and logbooks at `/journals`, and practical guides at `/nonfiction`. Teacher planners and school record books are journals, not textbooks.

Cover URLs are the actual thumbnails observed in the author-owned Amazon catalog supplied by the site owner. They are loaded from Amazon's media host, with intrinsic dimensions, lazy loading, and accessible alternatives. Prices, ratings, availability promises, and invented summaries are omitted. Purchase links have no newly added affiliate tracking. Existing affiliate links elsewhere are preserved.

To update:
1. Verify the author's actual listings and update `content/books.json`, including edition links and `verifiedAt`. Keep primary IDs unique. Keep companion journals distinct from curriculum books using the category field.
2. Run `python scripts/update_book_pages.py` to refresh the two page content records.
3. Run `python scripts/build.py` and `python scripts/build.py --check`.
4. Check image loading, search, categories, series order and mobile layout, then commit the catalog, page content records and generated HTML together.

The inventory is a checked-in snapshot, not a live Amazon feed. The older empty `content/products.json` is reserved for a different proposed origami product catalog and is not used here.
