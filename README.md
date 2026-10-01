# Origami Penguin

Free paper-folding education funded by recommended supplies and, when ready, real original products.

## Existing hosting

This is a static HTML/CSS site. Cloudflare Pages has an existing Git integration for this repository; successful GitHub Pages checks also exist. The public domain responds through Cloudflare. Do not change DNS, either hosting integration, or account credentials to work on content.

The generated `.html` files are checked in, so the current root-directory deployment needs no new build command or framework. Cloudflare Pages serves extensionless URLs and redirects `.html` requests. Keep existing filenames so inbound legacy links continue to work.

## Edit, build, test

Python 3 is the only build/test dependency:

    python3 scripts/build.py
    python3 -m unittest discover -s tests -v

- `templates/page.html`: common accessible page shell, navigation and metadata
- `style.css`: responsive styles, contrast, reduced motion and print layout; no remote fonts
- `content/site.json`: metadata for existing pages
- `content/legacy/`: existing owned article bodies, preserved during migration
- `content/tutorials/`: structured tutorial records used by the reusable tutorial renderer
- `content/pages/`: new structured pages, including the classroom lesson and paper guide
- `content/products.json`: deliberately empty verified-product catalog
- `scripts/build.py`: generates pages, truthful structured data and XML sitemap
- `tests/`: checks output freshness, internal links/fragments, metadata, schema, image dimensions and original affiliate URLs

Commit both content/template changes and generated output. `python3 scripts/build.py --check` fails if they drift. The validation workflow runs on pushes and pull requests. GitHub Actions validation does not gate the already-installed Cloudflare integration; run tests before updating `main`.

For a faithful local preview, use a static server that resolves extensionless URLs to their `.html` files. Production verification must include the actual custom domain, not just a successful build status.

See [development and editorial notes](docs/content-system.md), [rollback](docs/rollback.md) and [classroom/product guidelines](docs/classroom-editorial.md).
