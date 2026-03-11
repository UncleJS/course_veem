# export — Course Export Scripts

This directory contains the scripts and assets used to build the combined
course document from the individual source files.

**The output files in this directory are auto-generated. Do not edit them
manually** — re-run `generate.py` instead.

---

## Files

| File | Description |
|---|---|
| `generate.py` | Main build script — produces the Markdown and PDF |
| `pdf-style.css` | A4 CSS stylesheet used by the PDF renderer |
| `course-complete.md` | **Generated** — combined Markdown document (do not edit) |
| `course-complete.pdf` | **Generated** — A4 PDF export (do not edit) |

---

## Requirements

- **Python 3.8+** — standard library only; no pip dependencies
- **Node.js + npx** — used to run `md-to-pdf` for PDF export
  - `md-to-pdf` is fetched automatically via `npx` if not installed globally
  - To install globally (faster on repeated runs): `npm install -g md-to-pdf`

---

## Usage

Run from the **repo root** or from inside the `export/` directory.

### Build both Markdown and PDF

```bash
python3 export/generate.py
```

### Build Markdown only (fast — no browser required)

```bash
python3 export/generate.py --md-only
```

### Build PDF only (Markdown file must already exist)

```bash
python3 export/generate.py --pdf-only
```

---

## What the script does

1. Reads the 40 source files (lessons, quizzes, exam, glossary) in order
2. Injects section separator headings (`SECTION 1 — Course Overview`, etc.)
3. Builds a master Table of Contents at the top of the combined document
4. Scopes all H2/H3 heading anchors with a per-section prefix (e.g. `l01-`, `quiz-beg-`) to avoid collisions across sections
5. Rewrites all within-file heading links to their scoped targets, handling both modern and legacy GitHub slug formats
6. Replaces `[Go to TOC]` nav links with dual nav blocks:
   ```
   [Go to Lesson TOC](#toc-xxx)
   [Go to Course TOC](#master-table-of-contents)
   ```
7. Injects explicit `<a id="...">` anchors before every H1/H2/H3 for renderer compatibility
8. Exports the Markdown to A4 PDF via `md-to-pdf` + Puppeteer using `pdf-style.css`
9. Prints a link-integrity report on completion

**Source files are never modified.**

---

## Output integrity

After each run the script prints:

```
Anchors : 748
Links   : 1547
Broken  : 0
```

A broken link count above `0` means a heading was renamed or removed in a
source file without a corresponding update to `generate.py`. Check the printed
list of broken targets and update `EXTRA_ALIASES` in the script if needed.

---

## Section prefix map

Each source file is assigned a unique prefix used for anchor scoping:

| Prefix | Source file |
|---|---|
| `readme` | `README.md` |
| `lessons-index` | `lessons/README.md` |
| `course-index` | `lessons/00-index.md` |
| `l01` – `l27` | `lessons/01-introduction.md` – `lessons/27-troubleshooting.md` |
| `quiz-beg` | `quizzes/quiz-beginner.md` |
| `quiz-beg-ans` | `quizzes/quiz-beginner-answers.md` |
| `quiz-int` | `quizzes/quiz-intermediate.md` |
| `quiz-int-ans` | `quizzes/quiz-intermediate-answers.md` |
| `quiz-adv` | `quizzes/quiz-advanced.md` |
| `quiz-adv-ans` | `quizzes/quiz-advanced-answers.md` |
| `l28` | `exam/28-vmce-exam-prep.md` |
| `exam-bank` | `exam/exam-bank-120.md` |
| `exam-bank-ans` | `exam/exam-bank-120-answers.md` |
| `glossary` | `glossary.md` |
