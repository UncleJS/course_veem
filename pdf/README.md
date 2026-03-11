# PDF Build Pipeline

Converts all course Markdown files into PDFs using [Puppeteer](https://pptr.dev/) (headless Chromium) and [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli).

## Prerequisites

- [Bun](https://bun.sh/) v1.0+
- Chromium system dependencies (Puppeteer downloads its own Chromium automatically)

## Setup

Run once from inside the `pdf/` directory:

```bash
bun install
```

## Usage

All commands must be run from the `pdf/` directory.

### Full build (combined + individual)

```bash
bun run build
```

Produces both `output/course.pdf` and all `output/lessons/*.pdf` files.

### Combined PDF only

```bash
bun run build:combined
```

Produces a single `output/course.pdf` containing every document in order (cover → lessons → quizzes → exam → instructor guide), with working cross-document links and section dividers.

### Individual PDFs only

```bash
bun run build:individual
```

Produces one PDF per source `.md` file under `output/lessons/`. Cross-document links are rewritten to point to the sibling PDF files.

### Direct invocation (flags)

The same flags can be passed directly to `build.js`:

```bash
bun run build.js --combined-only
bun run build.js --individual-only
```

## Output structure

```
pdf/
└── output/
    ├── course.pdf          # Full combined PDF
    ├── course.html         # Intermediate HTML (debug artifact)
    └── lessons/
        ├── readme.pdf
        ├── lessons-01-introduction.pdf
        ├── lessons-02-backup-fundamentals.pdf
        └── ...             # One file per source .md
```

File names are derived from the source path:
`lessons/01-introduction.md` → `lessons-01-introduction.pdf`

## How it works

1. **Mermaid pre-rendering** — every ` ```mermaid ` block is rendered to an inline SVG via `mmdc` (Mermaid CLI) before HTML conversion. If a block fails to render, it falls back to a styled code block.
2. **Markdown → HTML** — [`marked`](https://marked.js.org/) converts each file with GFM enabled. Heading IDs are scoped per-document in the combined PDF so same-page anchor links resolve correctly.
3. **Image embedding** — external `https://` images (e.g. badge shields) are fetched and inlined as base64 data URIs so the PDF is fully self-contained.
4. **Link rewriting** — `.md` cross-document links are rewritten to `#<slug>` anchors (combined PDF) or sibling `.pdf` file paths (individual PDFs).
5. **Puppeteer PDF export** — the assembled HTML is rendered to A4 PDF with a header/footer showing the course title and page numbers.
