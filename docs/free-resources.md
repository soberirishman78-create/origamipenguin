# Free Resources

The /free-resources page offers 19 original US Letter one-page PDFs, a 19-page combined pack, and JPEG previews. Suggested grade bands span K-6; they are guidance rather than a standards-alignment claim. Each sheet includes a pale OPP watermark and attribution footer. Content is available without signup, free for personal/home/classroom use; credit must remain and resale is excluded.

Run scripts/create_free_resources.py using Python with reportlab and pypdf plus Poppler pdftoppm to rebuild the PDFs, previews, manifest and page data. Then run scripts/build.py. Normal builds need no PDF dependencies. All source content is in the generator; grade labels and preview filenames are in content/free-resources.json.

Quality review: every individual PDF is one page, pack order follows the manifest, all 19 pages rendered and reviewed, tables and worked arithmetic reviewed. U.S. customary units are distinguished from metric and volume from weight. Thirds use repeating decimals and exact mixed-number percents. PDFs contain selectable text. Preview images are only thumbnails; the PDFs are the printable versions.

Grade and subject filters combine with AND logic and match all grades in each suggested range (K is encoded as 0). Reset restores all 19 sheets. Empty subject sections are hidden. Filtering never changes the complete-pack download. With JavaScript off, all resources and subject jump links remain visible. scripts/resource_filters.py adds controls and card metadata to page data without regenerating PDFs. The PDF generator calls the same helper for future rebuilds.
