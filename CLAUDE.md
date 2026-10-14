# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is an **Obsidian vault that doubles as the content source for a Quartz v4 static blog**
("Jeakyoung's Notes", published at `jeakyoung.github.io/obsidian-database`). It is not an
application codebase — there is no local Quartz install, no `package.json`, no app to build.
The only "code" here is:

- A handful of **Python maintenance scripts** (`tools/*.py`) that keep frontmatter/body format
  consistent across hundreds of Markdown notes.
- **Quartz customization files** at the repo root (`quartz.config.ts`, `quartz.layout.ts`,
  `quartz.custom.scss`, `quartz.overrides/*.tsx`) that get copied into a freshly cloned Quartz
  checkout during CI — Quartz itself is never checked into this repo.
- A **GitHub Actions workflow** (`.github/workflows/deploy.yml`) that does the clone + copy +
  build + deploy to GitHub Pages on every push to `main`.

The actual blog content lives under `Jeakyoung_Blog/` — that folder is the Quartz `content/`
root. Everything else in the vault (outside `Jeakyoung_Blog/`) is private Obsidian scratch space
and is not published.

## Commands

All commands run from the repo root using whatever `python`/`python3` is on PATH (no venv,
no dependencies beyond the standard library).

```bash
# Preview changes (default, no args = dry-run) before writing anything:
python tools/normalize_frontmatter.py
python tools/apply_schema.py
python tools/apply_body_format.py
python tools/build_format_docs.py
python tools/build_index.py

# Actually write changes, in this order (order matters — see below):
python tools/normalize_frontmatter.py --apply   # fill missing title/date
python tools/apply_schema.py --apply            # normalize frontmatter schema per folder type
python tools/apply_body_format.py --apply       # enforce the 5-step H2 body skeleton
python tools/build_format_docs.py --apply       # refresh the "문서 양식" block in each index.md
python tools/build_index.py --apply             # refresh the AUTO-INDEX doc-list block in each index.md

# Add --show to any script to print exactly which files changed and why
python tools/apply_schema.py --apply --show
```

Run this full pipeline any time notes are added, removed, or moved under `Jeakyoung_Blog/`.
Every script is **idempotent** — running it twice produces no further diff — so it's safe to
re-run the whole chain after partial edits.

There are no tests, linters, or build commands to run locally; there is nothing to compile.
The only "build" is the GitHub Actions workflow, which runs remotely on push.

## Architecture

### Content pipeline (how a note becomes a published page)

1. A note is created in `Jeakyoung_Blog/<project-or-category>/...` from a template in
   `_templates/` (via Obsidian's "Insert Template" command).
2. The five `tools/*.py` scripts normalize it:
   - `normalize_frontmatter.py` — guarantees `title` and `date` exist. `date` is inferred, in
     priority order, from: a date embedded in the filename (`09.15`, `25.11.03`,
     `(2025-10-15)`), a `created`-like key already in frontmatter, the file's first commit date
     (`git log --diff-filter=A --follow`), or finally the file's mtime.
   - `apply_schema.py` — determines a note's `type` (작업/기술문서/회의록/참고자료/학습자료/...)
     purely from **which directory it's in** (`DIR_TYPE` / folder name → type), and its
     `project` from a fixed folder→project map (`PROJECT`). It then rewrites frontmatter to the
     canonical key set/order for that type and coerces free-text status/priority values into the
     fixed enums (`STATUS`, `PRIORITY`).
   - `apply_body_format.py` — reshapes the note body into a fixed 5-step H2 skeleton (see below),
     demoting any pre-existing headings to H3+ under whichever step they land in. It never
     deletes content, only re-nests it.
   - `build_format_docs.py` / `build_index.py` — regenerate the auto-managed blocks inside each
     folder's `index.md` (format cheat-sheet, and the doc listing) between
     `<!-- FORMAT:START/END -->` and `<!-- AUTO-INDEX:START/END -->` markers. Anything outside
     those markers in `index.md` is hand-written and preserved.
3. On push to `main` touching `Jeakyoung_Blog/**` (or any `quartz.*` file), CI clones Quartz
   v4.4.0 fresh, overlays this repo's config/overrides onto it, `rsync`s `Jeakyoung_Blog/` into
   `quartz-build/content/`, builds, renders the `02_Career` docs to PDF via Puppeteer
   (`scripts/render-pdf.mjs`, consumed by the `PdfButton` override), and deploys `public/` to
   GitHub Pages.

### Why type/project is derived from folder path, not frontmatter

`apply_schema.py`'s `DIR_TYPE` and `PROJECT` dicts are the single source of truth for a note's
`type`/`project` — whatever is already in frontmatter is ignored/overwritten based on path. This
means **moving a note to a different folder changes its published type**, and adding a new
project requires adding an entry to `PROJECT` (and usually `FOLDER_NAMES` in `build_index.py`),
not just writing frontmatter by hand.

### The 5-step body skeleton (format contract)

Every note (except `index.md`) must have exactly 5 H2 sections, in fixed order, with the exact
icon + name for its type — these strings must match **character-for-character** between
`apply_body_format.py`'s `SPEC`, `build_format_docs.py`'s `SPEC`, and
`_templates/_문서 양식 명세.md`, because the tooling matches on that text. The 5 slots are always:
overview → background/context → main body → verification/follow-up → references, but the exact
icon+label differs per type (e.g. 작업 uses "🔍 현상 및 원인" / "🔧 조치 내용"; 회의록 uses
"💬 논의 내용" / "✅ 결정 사항"). See `_templates/_문서 양식 명세.md` for the full table before
touching any of the three files that encode it.

Folders with a dedicated template (`01_Tasks`, `02_TechDocs`/`03_TechDocs`, `03_Meetings`,
`04_References`) get their type from path. Everything else (`03_Learning`, `02_Career`, project
root docs) gets its type from frontmatter `type`, matched against the same spec.

### Quartz customization layering

Quartz itself is not vendored — `deploy.yml` clones it at tag `v4.4.0` into `quartz-build/` and
then overwrites specific files with this repo's versions:

| This repo | Overwrites in quartz-build |
|---|---|
| `quartz.config.ts` | `quartz.config.ts` |
| `quartz.layout.ts` | `quartz.layout.ts` |
| `quartz.custom.scss` | `quartz/styles/custom.scss` |
| `quartz.overrides/*.tsx`, `index.ts` | matching files under `quartz/components/` |
| `quartz.static/*.png` | `quartz/static/` (favicon, og-image) |

`quartz.overrides/` exists because Quartz has no plugin hook for these behaviors — the files are
copied whole over the originals: `FolderContent.tsx` (dedupe folder index doc list),
`Backlinks.tsx` (hide empty backlinks block), `ExplorerNode.tsx` (hover tooltips in file tree),
`PdfButton.tsx` (new component — "Save as PDF" button, only used on `02_Career` pages).

`enableSPA: false` in `quartz.config.ts` is intentional, not an oversight — some corporate
DLP/security browser extensions intercept `fetch()` and strip the path, breaking SPA
client-side navigation; plain `<a href>` navigation avoids that.

### Content conventions worth knowing before editing notes

- Code/queries must be inside fenced code blocks — unfenced text like `#FFFACD` gets
  misinterpreted as a tag by the blog.
- Images referenced by notes must live under `Jeakyoung_Blog/resources/`; images pasted at the
  vault root are excluded from the blog build (`.gitignore` blocks `Pasted image *.png/jpg/jpeg`
  everywhere except under `Jeakyoung_Blog/resources/`).
- `ignorePatterns` in `quartz.config.ts` excludes `05_Archive/**`, `01_Projects/Archive/**`, and
  `**/*.base` (Obsidian Bases files) from publishing even though they live under
  `Jeakyoung_Blog/`.
