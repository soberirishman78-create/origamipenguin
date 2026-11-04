# Jeremy Kelly book collection

`content/books.json` records the 120 distinct titles observed on Jeremy Kelly's Amazon all-books author page on November 4, 2026. The author page showed 121 listings; two Aeries Query Handbook listings are combined into one card with both destination links. Each of the 22 Kelly Brothers Mysteries is included in series order. Fiction appears at `/books`; the remaining curriculum, reference, planning and activity titles appear in clearly labeled groups at `/textbooks`.

Cover URLs are the actual thumbnails observed in the author-owned Amazon catalog supplied by the site owner. They are loaded from Amazon's media host, with intrinsic dimensions, lazy loading, and accessible alternatives. Prices, ratings, availability promises, and invented summaries are omitted. Purchase links have no newly added affiliate tracking. Existing affiliate links elsewhere are preserved.

To update:
1. Verify the author's actual listings and update `content/books.json`, including edition links and `verifiedAt`. Keep primary IDs unique. Keep companion journals distinct from curriculum books using the category field.
2. Run `python scripts/update_book_pages.py` to refresh the two page content records.
3. Run `python scripts/build.py` and `python scripts/build.py --check`.
4. Check image loading, search, categories, series order and mobile layout, then commit the catalog, page content records and generated HTML together.

The inventory is a checked-in snapshot, not a live Amazon feed. The older empty `content/products.json` is reserved for a different proposed origami product catalog and is not used here.
