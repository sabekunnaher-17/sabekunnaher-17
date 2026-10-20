# Profile implementation and provenance

Design: dark emerald terminal workspace with green/teal accents, compact analytical panels, moving code streams, circuit packets and quiet orbital motion, and editorial project descriptions. GitHub Markdown, supported HTML tables, and self-contained SVG images require no README JavaScript or custom page CSS. All essential content is visible in static frames. SVG motion honors `prefers-reduced-motion` where supported by the image renderer; clients may suppress SVG animation entirely.

## Evidence reviewed

On October 21, 2026, all five then-public repositories were inspected through GitHub metadata and recursive file trees. ProjectFlow's README, Web project file, architecture, services and test structure establish its stack and implemented features. Its genuine `docs/screenshots/projectflow-desktop.png` is copied unchanged as `assets/projectflow.png`; screenshot data belongs to a CI fixture, not production users.

Solar-System-Simulation's `main.cpp` establishes C++, GLUT/OpenGL, orbital rendering, DDA, midpoint circles, perspectives and a Bézier path. Q-Billiard-Shop's `Start.java`, class tree and `classes/Payment.java` establish Swing UI and screen navigation; no live payment gateway is claimed. The research repository's `src/analysis.py` and tree establish scientific Python dependencies, manuscript/results assets and an absent input CSV. Portfolio README, package.json and `src/content.ts` establish React/TypeScript, identity, university, and existing professional destinations. Self-reported skills without public code evidence were excluded from the toolkit.

The portfolio root returned HTTP 200. LinkedIn is listed by the GitHub account and portfolio but automated retrieval returned HTTP 405, so the README uses the verified portfolio contact destination instead. No unverified project deployment is presented as a live demo. Existing portfolio already supplies the interactive experience, so no duplicate website was created.

## Data definitions

The user confirmed **October 25, 2025** as the start. The inclusive end is the refresh date in Asia/Dhaka. Initial implementation date: October 21, 2026. GraphQL `contributionsCollection` retrieves actual daily contribution counts and separate commit, PR, issue, review and repository totals. Calendar dates are used as returned by GitHub, with date filtering and a completeness assertion. Zero days are shown; outside-period days are blank. GitHub calendar rules govern attribution. Private details, unsupported streaks and profile view counts are omitted. Collection queries are split into at most 365-day inclusive windows for long-term refreshes. Category totals can differ from calendar totals under GitHub's counting rules.

REST `/users/{login}`, paginated `/users/{login}/repos`, per-repo `/languages` and branch commit endpoints supply account counts, repository metadata, language bytes and source revision SHAs. Charts include non-fork public repositories; primary-language counts exclude repositories without a detected language. Byte distribution includes all detected languages; these are not measures of ability, time, authorship, or lines of code. The newly created profile repository is included once GitHub detects its languages. GitHub indexing can lag new pushes.

`data/github.json` records the retrieval time, query boundaries, public metadata, repository revisions and unmodified contribution collections. The workflow does not expose the token or retrieve private source. GitHub API access and repository-hosted image availability are the only runtime dependencies; no external stats-image service is required.

## Maintenance

`python scripts/update_profile.py --offline` deterministically regenerates all SVGs and the text snapshot without network access. Online refresh requires a GitHub token in `GITHUB_TOKEN` with public GraphQL access. The scheduled/manual workflow uses the repository-scoped built-in token, standard Python, and a pinned checkout action. It runs daily at 01:25 Asia/Dhaka, subject to GitHub scheduling delays. Updates use the Actions bot identity and only commit generated changes. The refresh workflow itself does not backdate commits or rewrite Git history. See the decorative-calendar disclosure below for the separate artwork repository.

Review changes to project descriptions manually as implementations evolve. The workflow refreshes metrics, not editorial claims. Check the latest Actions run before relying on freshness; the visible snapshot date remains the previous verified date if collection fails. A new retrieval timestamp can produce a bot maintenance commit even if counts remain unchanged. These bot updates are ordinary maintenance and are not attributed to Antora's contribution record.

## Organization and repository motion update — October 21, 2026

All six personally owned public repositories and the public hospital organization project use matching terminal-themed README visuals. Existing project documentation and team attribution are preserved. Organization PR #2 was verified as authored by sabekunnaher-17 and merged on October 16, 2026. It is featured separately from owned-repository metrics. No organization-wide branding or other developers’ profiles were changed.

All in-range calendar cells use a green palette: dark green explicitly means zero contributions, brighter greens mean recorded contributions. During the original theme-only update, empty days were not turned into activity. A subsequent, explicitly requested decorative-calendar addition is described below. Native GitHub heatmap colors and GitHub page backgrounds are controlled by GitHub, not README assets. Motion lives inside the SVG background; reduced-motion mode disables animations.

## Decorative calendar addition — October 21, 2026

After the user explicitly requested the commit-based approach, a separate public `sabekunnaher-17/contribution-calendar-art` repository was created with 362 decorative commits: one artwork cell per author date, October 25, 2025 through October 21, 2026 inclusive. Committer dates retain actual execution time. Existing project history was not rewritten. The artwork README and profile visibly disclose that this is backdated art, not historical development or a coding streak. There is no daily art automation. The native graph and API account totals may include these cells after GitHub indexing; the custom dashboard identifies their inclusion. Data retrieval from GitHub does not establish that all activity represents software engineering work.

## CV-aligned editorial update — October 21, 2026

The user supplied the two-page Sabekunnaher_Antora.pdf CV. Both pages were rendered and inspected, and embedded hyperlinks were extracted. The profile now leads with full-stack development, testing and research, followed by engineering projects, the CV toolkit, research, education and leadership; account metrics are secondary. The original PDF is copied byte-for-byte to assets/Sabekunnaher_Antora_CV.pdf. SHA-256: 756c8dd4c44a322d55855d88594c50a4bff4f416725f470c01b9677ee609c22e. No changes were made to the supplied CV.

AIUB education, coursework, four-member thesis leadership, academic project coordination and Ostad AI Engineering Bootcamp (2025) are CV-sourced claims; no graduation date or employment was inferred. The full CV toolkit is labeled accordingly and separated from selected publicly evidenced project technologies. The CV email and LinkedIn destination match its embedded links. The public README does not separately repeat the phone number; the downloadable original CV retains all its supplied content.

The CV Solar System hyperlink points to rifatur17/Solar-System-Simulation. The profile instead links to Antora’s existing public repository of that name, already inspected for its source. Organization attribution is governed by the verified merged PR #2, rather than claiming authorship of the teammate’s authentication/admin work. Research figures (183 valid cases, 50.8% recognition, CV R2 0.578, CV AUC 0.879) were cross-checked against the public recorded results, not rerun without the private input dataset. Publication status was not inferred. The calendar-art disclosure remains beside the optional contribution chart.
