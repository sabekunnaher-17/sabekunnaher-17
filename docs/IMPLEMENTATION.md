# Profile implementation and provenance

Design: midnight-blue developer workspace with cyan/violet accents, compact analytical panels, quiet orbital motion, and editorial project descriptions. GitHub Markdown, supported HTML tables, and self-contained SVG images require no README JavaScript or custom page CSS. All essential content is visible in static frames. SVG motion honors `prefers-reduced-motion` where supported by the image renderer; clients may suppress SVG animation entirely.

## Evidence reviewed

On October 21, 2026, all five then-public repositories were inspected through GitHub metadata and recursive file trees. ProjectFlow's README, Web project file, architecture, services and test structure establish its stack and implemented features. Its genuine `docs/screenshots/projectflow-desktop.png` is copied unchanged as `assets/projectflow.png`; screenshot data belongs to a CI fixture, not production users.

Solar-System-Simulation's `main.cpp` establishes C++, GLUT/OpenGL, orbital rendering, DDA, midpoint circles, perspectives and a Bézier path. Q-Billiard-Shop's `Start.java`, class tree and `classes/Payment.java` establish Swing UI and screen navigation; no live payment gateway is claimed. The research repository's `src/analysis.py` and tree establish scientific Python dependencies, manuscript/results assets and an absent input CSV. Portfolio README, package.json and `src/content.ts` establish React/TypeScript, identity, university, and existing professional destinations. Self-reported skills without public code evidence were excluded from the toolkit.

The portfolio root returned HTTP 200. LinkedIn is listed by the GitHub account and portfolio but automated retrieval returned HTTP 405, so the README uses the verified portfolio contact destination instead. No unverified project deployment is presented as a live demo. Existing portfolio already supplies the interactive experience, so no duplicate website was created.

## Data definitions

The user confirmed **October 25, 2025** as the start. The inclusive end is the refresh date in Asia/Dhaka. Initial implementation date: October 21, 2026. GraphQL `contributionsCollection` retrieves actual daily contribution counts and separate commit, PR, issue, review and repository totals. Calendar dates are used as returned by GitHub, with date filtering and a completeness assertion. Zero days are shown; outside-period days are blank. GitHub calendar rules govern attribution. Private details, unsupported streaks and profile view counts are omitted. Collection queries are split into at most 365-day inclusive windows for long-term refreshes. Category totals can differ from calendar totals under GitHub's counting rules.

REST `/users/{login}`, paginated `/users/{login}/repos`, per-repo `/languages` and branch commit endpoints supply account counts, repository metadata, language bytes and source revision SHAs. Charts include non-fork public repositories; primary-language counts exclude repositories without a detected language. Byte distribution includes all detected languages; these are not measures of ability, time, authorship, or lines of code. The newly created profile repository is included once GitHub detects its languages. GitHub indexing can lag new pushes.

`data/github.json` records the retrieval time, query boundaries, public metadata, repository revisions and unmodified contribution collections. The workflow does not expose the token or retrieve private source. GitHub API access and repository-hosted image availability are the only runtime dependencies; no external stats-image service is required.

## Maintenance

`python scripts/update_profile.py --offline` deterministically regenerates all SVGs and the text snapshot without network access. Online refresh requires a GitHub token in `GITHUB_TOKEN` with public GraphQL access. The scheduled/manual workflow uses the repository-scoped built-in token, standard Python, and a pinned checkout action. It runs daily at 01:25 Asia/Dhaka, subject to GitHub scheduling delays. Updates use the Actions bot identity and only commit generated changes. No backdating, Git history rewriting or artificial contribution creation is performed.

Review changes to project descriptions manually as implementations evolve. The workflow refreshes metrics, not editorial claims. Check the latest Actions run before relying on freshness; the visible snapshot date remains the previous verified date if collection fails. A new retrieval timestamp can produce a bot maintenance commit even if counts remain unchanged. These bot updates are ordinary maintenance and are not attributed to Antora's contribution record.
