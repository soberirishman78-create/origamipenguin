# Phase-one rollback

## Verified source checkpoint

Before modification, the clean default branch was:

- Repository: https://github.com/soberirishman78-create/origamipenguin
- Commit: `47ecea9803be57b8f40c499a1620ab9048fb0f72`
- Remote backup: `backup/pre-phase-one-20261001`
- Existing successful Cloudflare deployment: https://56bad621.origamipenguin.pages.dev

The live homepage matched that commit byte-for-byte. A full-history Git bundle and source tar archive were created and the bundle was verified. This protects all tracked static source/assets. It is not a complete export of Cloudflare DNS, dashboard configuration, analytics or other account state, which was unavailable. No such account settings were modified in this phase.

## Restore without rewriting history

For a clean checkout with no other uncommitted work, inspect the current `main` first. Revert the phase-one deployment commit(s), run the original site's relevant checks, and push the revert through the existing workflow. Alternatively create a new branch based on current `main`, use `git restore --source=backup/pre-phase-one-20261001 --staged --worktree .`, inspect the complete diff, commit the restoration, and merge normally. Preserve unrelated later work. Never reset/force-push main casually.

After either path, wait for the Cloudflare check on the exact restore commit and verify the custom domain, a tutorial, affiliate destinations, CSS, robots/sitemap and a genuinely missing URL. The account owner may also use Cloudflare Pages' existing deployment rollback UI after checking its current behavior and available deployment. Do not change DNS to roll back static content.
