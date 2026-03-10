/**
 * build.js — PDF build pipeline for Veeam B&R v12.x course
 *
 * Produces:
 *   output/course.pdf          — full combined PDF (all documents in order)
 *   output/lessons/<slug>.pdf  — one PDF per source .md file
 *
 * Run:  bun run build.js
 *       bun run build.js --combined-only
 *       bun run build.js --individual-only
 */

import fs from "fs";
import path from "path";
import { execSync, spawn } from "child_process";
import { fileURLToPath } from "url";
import { marked, Marked, Renderer } from "marked";
import puppeteer from "puppeteer";

// ─── Paths ────────────────────────────────────────────────────────────────────

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(__dirname, "output");
const OUT_LESSONS = path.join(OUT_DIR, "lessons");
const TEMPLATE_PATH = path.join(__dirname, "template.html");
const MERMAID_TMP = path.join(__dirname, ".mermaid-tmp");

// ─── Document order ───────────────────────────────────────────────────────────
// Defines the exact sequence for the combined PDF.
// Each entry: { file: path-relative-to-REPO_ROOT, group: string }

const DOCUMENTS = [
  // Cover / entry point
  { file: "README.md",                                     group: "cover"      },

  // Lessons
  { file: "lessons/00-index.md",                           group: "lessons"    },
  { file: "lessons/01-introduction.md",                    group: "lessons"    },
  { file: "lessons/02-backup-fundamentals.md",             group: "lessons"    },
  { file: "lessons/03-architecture-overview.md",           group: "lessons"    },
  { file: "lessons/04-installation-requirements.md",       group: "lessons"    },
  { file: "lessons/05-lab-install-vbr.md",                 group: "lessons"    },
  { file: "lessons/06-adding-infrastructure.md",           group: "lessons"    },
  { file: "lessons/07-backup-repositories.md",             group: "lessons"    },
  { file: "lessons/08-lab-configure-repository.md",        group: "lessons"    },
  { file: "lessons/09-vm-backup-jobs.md",                  group: "lessons"    },
  { file: "lessons/10-lab-vm-backup-job.md",               group: "lessons"    },
  { file: "lessons/11-backup-proxies.md",                  group: "lessons"    },
  { file: "lessons/12-application-aware-processing.md",    group: "lessons"    },
  { file: "lessons/13-agent-based-backup.md",              group: "lessons"    },
  { file: "lessons/14-lab-agent-backup.md",                group: "lessons"    },
  { file: "lessons/15-nas-backup.md",                      group: "lessons"    },
  { file: "lessons/16-restore-options.md",                 group: "lessons"    },
  { file: "lessons/17-lab-instant-vm-recovery.md",         group: "lessons"    },
  { file: "lessons/18-application-item-restore.md",        group: "lessons"    },
  { file: "lessons/19-replication.md",                     group: "lessons"    },
  { file: "lessons/20-lab-replication.md",                 group: "lessons"    },
  { file: "lessons/21-backup-copy-jobs.md",                group: "lessons"    },
  { file: "lessons/22-tape-support.md",                    group: "lessons"    },
  { file: "lessons/23-object-storage-cloud-tier.md",       group: "lessons"    },
  { file: "lessons/24-security-hardening.md",              group: "lessons"    },
  { file: "lessons/25-scale-enterprise.md",                group: "lessons"    },
  { file: "lessons/26-monitoring-reporting.md",            group: "lessons"    },
  { file: "lessons/27-troubleshooting.md",                 group: "lessons"    },

  // Quizzes
  { file: "quizzes/quiz-beginner.md",                      group: "quizzes"    },
  { file: "quizzes/quiz-beginner-answers.md",              group: "quizzes"    },
  { file: "quizzes/quiz-intermediate.md",                  group: "quizzes"    },
  { file: "quizzes/quiz-intermediate-answers.md",          group: "quizzes"    },
  { file: "quizzes/quiz-advanced.md",                      group: "quizzes"    },
  { file: "quizzes/quiz-advanced-answers.md",              group: "quizzes"    },

  // Exam
  { file: "exam/28-vmce-exam-prep.md",                     group: "exam"       },
  { file: "exam/exam-bank-120.md",                         group: "exam"       },
  { file: "exam/exam-bank-120-answers.md",                 group: "exam"       },

  // Instructor guide (last)
  { file: "instructor-guide.md",                           group: "instructor" },
];

// ─── Slug generation ──────────────────────────────────────────────────────────
// Converts a file path to a stable HTML id used as the section anchor.
// "lessons/01-introduction.md" → "lessons-01-introduction"
// "README.md"                  → "readme"

function fileToSlug(filePath) {
  return filePath
    .replace(/\.md$/, "")
    .replace(/[/\\]/g, "-")
    .toLowerCase();
}

// Build a lookup: filePath → slug for all documents in order
const SLUG_MAP = new Map(DOCUMENTS.map((d) => [d.file, fileToSlug(d.file)]));

// ─── Mermaid pre-rendering ────────────────────────────────────────────────────

/**
 * Finds all ```mermaid ... ``` blocks in markdown text and replaces each with
 * an inline SVG rendered via mmdc (Mermaid CLI).
 */
async function renderMermaidBlocks(markdown, docSlug) {
  const mermaidRegex = /```mermaid\s*\n([\s\S]*?)```/g;
  const replacements = [];
  let match;

  while ((match = mermaidRegex.exec(markdown)) !== null) {
    replacements.push({ full: match[0], source: match[1], index: match.index });
  }

  if (replacements.length === 0) return markdown;

  fs.mkdirSync(MERMAID_TMP, { recursive: true });

  let result = markdown;
  // Process in reverse so string indices remain valid
  for (let i = replacements.length - 1; i >= 0; i--) {
    const { full, source } = replacements[i];
    const id = `${docSlug}-mmd-${i}`;
    const inFile = path.join(MERMAID_TMP, `${id}.mmd`);
    const outFile = path.join(MERMAID_TMP, `${id}.svg`);

    fs.writeFileSync(inFile, source.trim(), "utf8");

    try {
      // mmdc is in node_modules/.bin
      const mmdc = path.join(__dirname, "node_modules", ".bin", "mmdc");
      execSync(
        `"${mmdc}" -i "${inFile}" -o "${outFile}" --backgroundColor white --quiet`,
        { timeout: 30000, stdio: "pipe" }
      );
      const svg = fs.readFileSync(outFile, "utf8");
      // Strip XML declaration if present, wrap in a div
      const cleanSvg = svg.replace(/<\?xml[^?]*\?>/g, "").trim();
      const replacement = `<div class="mermaid-diagram">${cleanSvg}</div>`;
      result = result.slice(0, replacements[i].index) +
               replacement +
               result.slice(replacements[i].index + full.length);
    } catch (err) {
      console.warn(
        `  ⚠  Mermaid render failed for block ${i} in ${docSlug}: ${err.message?.split("\n")[0]}`
      );
      // Fall back to a styled code block so content is not lost
      const fallback = `<pre class="mermaid-fallback"><code>${escapeHtml(source)}</code></pre>`;
      result = result.slice(0, replacements[i].index) +
               fallback +
               result.slice(replacements[i].index + full.length);
    }
  }

  return result;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ─── Badge / image embedding ──────────────────────────────────────────────────

// Cache fetched URLs across documents
const IMAGE_CACHE = new Map();

/**
 * Fetches an image URL and returns a base64 data URI.
 * Returns null on failure so the original src is kept.
 */
async function fetchAsDataUri(url) {
  if (IMAGE_CACHE.has(url)) return IMAGE_CACHE.get(url);

  try {
    const res = await fetch(url, {
      signal: AbortSignal.timeout(10000),
      headers: { "User-Agent": "course-pdf-builder/1.0" },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buffer = await res.arrayBuffer();
    const mime = res.headers.get("content-type") || "image/svg+xml";
    const b64 = Buffer.from(buffer).toString("base64");
    const dataUri = `data:${mime};base64,${b64}`;
    IMAGE_CACHE.set(url, dataUri);
    return dataUri;
  } catch (err) {
    console.warn(`  ⚠  Could not embed image ${url}: ${err.message}`);
    IMAGE_CACHE.set(url, null);
    return null;
  }
}

/**
 * Replaces all <img src="https://..."> with embedded base64 data URIs.
 */
async function embedExternalImages(html) {
  const imgRegex = /<img([^>]*?)src="(https?:\/\/[^"]+)"([^>]*?)>/g;
  const matches = [];
  let m;
  while ((m = imgRegex.exec(html)) !== null) {
    matches.push({ full: m[0], before: m[1], url: m[2], after: m[3] });
  }

  // Deduplicate URLs then fetch in parallel
  const uniqueUrls = [...new Set(matches.map((m) => m.url))];
  await Promise.all(uniqueUrls.map(fetchAsDataUri));

  // Replace in HTML
  let result = html;
  for (const { full, before, url, after } of matches) {
    const dataUri = IMAGE_CACHE.get(url);
    if (dataUri) {
      result = result.replace(full, `<img${before}src="${dataUri}"${after}>`);
    }
  }
  return result;
}

// ─── Link rewriting ───────────────────────────────────────────────────────────

/**
 * In the COMBINED PDF every document is a <div id="<slug>"> inside one HTML file.
 *
 * Rules:
 *  1. "../LICENSE.md" / "LICENSE.md" → strip (not in combined doc, just remove link target)
 *  2. Cross-doc .md links → #<slug>
 *  3. Within-doc #anchor links → #<slug>-<anchor>
 *     (headings are given scoped IDs so same-doc anchors still work)
 *  4. External https:// links → unchanged
 */
function rewriteLinksForCombined(html, docSlug) {
  // Rewrite href attributes
  return html.replace(/href="([^"]+)"/g, (fullMatch, href) => {
    // External links — keep as-is
    if (/^https?:\/\//.test(href)) return fullMatch;

    // mailto: — keep as-is
    if (/^mailto:/.test(href)) return fullMatch;

    // Pure anchor within this document: #foo → #<slug>-foo
    if (href.startsWith("#")) {
      const anchor = href.slice(1);
      return `href="#${docSlug}-${anchor}"`;
    }

    // Cross-document .md link (with or without a fragment)
    const [filePart, fragment] = href.split("#");

    // Resolve the referenced file path relative to the source doc's folder
    const docFolder = path.dirname(
      DOCUMENTS.find((d) => fileToSlug(d.file) === docSlug)?.file ?? ""
    );
    const resolved = path.normalize(path.join(docFolder, filePart)).replace(/\\/g, "/");

    // Is it a known document in our combined PDF?
    const targetSlug = SLUG_MAP.get(resolved);

    if (targetSlug) {
      if (fragment) {
        return `href="#${targetSlug}-${fragment}"`;
      }
      return `href="#${targetSlug}"`;
    }

    // LICENSE.md or other files not in the combined set — remove the link href
    // by pointing to a no-op anchor so the text remains but the link does nothing
    return `href="#"`;
  });
}


// ─── Markdown → HTML ──────────────────────────────────────────────────────────

/**
 * GitHub-compatible heading slug: lowercase, strip non-word chars, spaces→dashes.
 * Matches what the course authors used when writing their TOC anchor links.
 *   "What Veeam Backup & Replication Includes" → "what-veeam-backup-replication-includes"
 *   "Practical Differences Between Learning v12 and Operating v12.x" → "practical-differences-between-learning-v12-and-operating-v12x"
 */
function headingSlug(text) {
  // Strip any inline HTML (e.g. from badge images in headings)
  const plain = text.replace(/<[^>]+>/g, "");
  return plain
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")   // remove punctuation (keeps letters, digits, _, -, spaces)
    .trim()
    .replace(/\s+/g, "-")       // spaces → hyphens
    .replace(/-{2,}/g, "-");    // collapse double-hyphens
}

/**
 * Build a marked instance whose heading renderer generates IDs scoped to docSlug.
 * Combined PDF:   id="<docSlug>-<headingSlug>"  → matches rewritten href="#<docSlug>-<anchor>"
 * Individual PDF: id="<headingSlug>"            → matches original href="#<anchor>"
 *
 * @param {string|null} docSlug  Pass the doc slug for combined mode, null for individual mode.
 */
function buildMarked(docSlug) {
  const renderer = new Renderer();

  renderer.heading = function ({ text, depth }) {
    const slug = headingSlug(text);
    const id = docSlug ? `${docSlug}-${slug}` : slug;
    // text may contain inline HTML (e.g. rendered badge images) — emit as-is
    return `<h${depth} id="${id}">${text}</h${depth}>\n`;
  };

  const instance = new Marked({
    gfm: true,
    breaks: false,
    renderer,
  });

  return instance;
}

/**
 * Converts a markdown string to an HTML fragment.
 * Mermaid blocks must already be replaced with <div class="mermaid-diagram">
 * before calling this function.
 *
 * @param {string} markdown
 * @param {string|null} docSlug  Scoped slug for combined PDF; null for individual PDF.
 */
function mdToHtml(markdown, docSlug) {
  return buildMarked(docSlug).parse(markdown);
}

// ─── Per-document processing ──────────────────────────────────────────────────

/**
 * Full processing pipeline for one .md file.
 *
 * Returns:
 *   combinedHtml   — scoped IDs + combined-PDF links; ready to embed in course.html
 *   individualHtml — unscoped IDs; links rewritten later in main() with the output path
 */
async function processDocument(doc) {
  const absPath = path.join(REPO_ROOT, doc.file);
  const slug = fileToSlug(doc.file);

  console.log(`  • ${doc.file}`);

  // 1. Read source
  let markdown = fs.readFileSync(absPath, "utf8");

  // 2. Pre-render Mermaid blocks → inline SVG (shared between both variants)
  markdown = await renderMermaidBlocks(markdown, slug);

  // ── Combined-PDF variant ───────────────────────────────────────────────────
  // Heading IDs are pre-scoped: id="<slug>-<headingSlug>"
  let combinedHtml = mdToHtml(markdown, slug);
  combinedHtml = await embedExternalImages(combinedHtml);
  combinedHtml = rewriteLinksForCombined(combinedHtml, slug);
  combinedHtml = `<div class="doc-section" id="${slug}">\n${combinedHtml}\n</div>`;

  // ── Individual-PDF variant ─────────────────────────────────────────────────
  // Heading IDs are plain (unscoped): id="<headingSlug>"
  // TOC anchors like #table-of-contents therefore resolve correctly within the page.
  // Cross-file link rewriting happens later in main() once we know the output path.
  let individualHtml = mdToHtml(markdown, null);
  individualHtml = await embedExternalImages(individualHtml);
  individualHtml = `<div class="doc-section" id="${slug}">\n${individualHtml}\n</div>`;

  return { doc, slug, combinedHtml, individualHtml };
}

// ─── Section dividers ─────────────────────────────────────────────────────────

function makeDivider(label) {
  return `<div class="section-divider"><h2>${label}</h2></div>`;
}

// ─── HTML assembly ────────────────────────────────────────────────────────────

function assembleHtml(sections) {
  const template = fs.readFileSync(TEMPLATE_PATH, "utf8");
  const content = sections.join("\n\n");
  return template.replace("<!--CONTENT-->", content);
}

// ─── Puppeteer PDF export ─────────────────────────────────────────────────────

async function renderPdf(htmlContent, outPath, browser) {
  const page = await browser.newPage();
  try {
    await page.setContent(htmlContent, {
      waitUntil: ["networkidle0", "domcontentloaded"],
      timeout: 120000,
    });

    // Wait a moment for any remaining layout to settle
    await new Promise((r) => setTimeout(r, 500));

    await page.pdf({
      path: outPath,
      format: "A4",
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: `<div style="font-size:8pt;font-family:Arial,sans-serif;color:#999;
        width:100%;text-align:center;padding:0 18mm;">
        Veeam Backup &amp; Replication v12.x Course
      </div>`,
      footerTemplate: `<div style="font-size:8pt;font-family:Arial,sans-serif;color:#999;
        width:100%;text-align:center;padding:0 18mm;">
        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
      </div>`,
      margin: { top: "22mm", bottom: "22mm", left: "18mm", right: "18mm" },
    });
  } finally {
    await page.close();
  }
}

// ─── Individual PDF: link rewriting for file:// links ─────────────────────────

/**
 * For individual per-lesson PDFs, rewrite .md cross-links to the actual
 * output PDF file paths so they open the corresponding PDF when clicked.
 */
function rewriteLinksForIndividual(html, docSlug, outBaseDir) {
  return html.replace(/href="([^"]+)"/g, (fullMatch, href) => {
    // External links — keep
    if (/^https?:\/\//.test(href)) return fullMatch;
    if (/^mailto:/.test(href)) return fullMatch;

    // Within-doc anchors — keep (they work in individual PDFs)
    if (href.startsWith("#")) return fullMatch;

    const [filePart, fragment] = href.split("#");
    const docFolder = path.dirname(
      DOCUMENTS.find((d) => fileToSlug(d.file) === docSlug)?.file ?? ""
    );
    const resolved = path.normalize(path.join(docFolder, filePart)).replace(/\\/g, "/");
    const targetSlug = SLUG_MAP.get(resolved);

    if (targetSlug) {
      const pdfFile = path.join(outBaseDir, `${targetSlug}.pdf`);
      const linkHref = fragment
        ? `${pdfFile}#${fragment}`
        : pdfFile;
      return `href="${linkHref}"`;
    }

    return `href="#"`;
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const combinedOnly = args.includes("--combined-only");
  const individualOnly = args.includes("--individual-only");
  const doCombined = !individualOnly;
  const doIndividual = !combinedOnly;

  console.log("\n╔══════════════════════════════════════════════════╗");
  console.log("║   Veeam B&R v12.x Course — PDF Build Pipeline   ║");
  console.log("╚══════════════════════════════════════════════════╝\n");

  // Ensure output dirs exist
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(OUT_LESSONS, { recursive: true });

  // ── Step 1: Process all documents ────────────────────────────────────────
  console.log("▶  Processing documents…");
  const processedDocs = [];
  for (const doc of DOCUMENTS) {
    const result = await processDocument(doc);
    processedDocs.push(result);
  }

  // ── Step 2: Build combined HTML ───────────────────────────────────────────
  let combinedSections = [];
  let lastGroup = null;

  const GROUP_LABELS = {
    quizzes:    "Quizzes",
    exam:       "Exam Preparation",
    instructor: "Instructor Guide",
  };

  for (const { doc, combinedHtml } of processedDocs) {
    // Insert a section divider when the group changes (except for cover→lessons)
    if (
      lastGroup !== null &&
      doc.group !== lastGroup &&
      doc.group !== "lessons" &&
      GROUP_LABELS[doc.group]
    ) {
      combinedSections.push(makeDivider(GROUP_LABELS[doc.group]));
    }
    combinedSections.push(combinedHtml);
    lastGroup = doc.group;
  }

  // ── Step 3: Launch Puppeteer ──────────────────────────────────────────────
  console.log("\n▶  Launching Puppeteer (headless Chromium)…");
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--font-render-hinting=none",
    ],
  });

  try {
    // ── Step 4: Combined PDF ────────────────────────────────────────────────
    if (doCombined) {
      console.log("\n▶  Generating combined PDF…");
      const combinedHtml = assembleHtml(combinedSections);

      // Optionally write the intermediate HTML for debugging
      fs.writeFileSync(path.join(OUT_DIR, "course.html"), combinedHtml, "utf8");

      const outPath = path.join(OUT_DIR, "course.pdf");
      await renderPdf(combinedHtml, outPath, browser);
      const size = (fs.statSync(outPath).size / 1024 / 1024).toFixed(1);
      console.log(`   ✓  output/course.pdf  (${size} MB)`);
    }

    // ── Step 5: Individual PDFs ────────────────────────────────────────────
    if (doIndividual) {
      console.log("\n▶  Generating individual PDFs…");

      for (const { doc, slug, individualHtml } of processedDocs) {
        // Rewrite cross-file .md links → sibling PDF file paths
        const linkedHtml = rewriteLinksForIndividual(individualHtml, slug, OUT_LESSONS);
        const pageHtml = assembleHtml([linkedHtml]);

        const outPath = path.join(OUT_LESSONS, `${slug}.pdf`);
        await renderPdf(pageHtml, outPath, browser);

        const size = (fs.statSync(outPath).size / 1024).toFixed(0);
        console.log(`   ✓  output/lessons/${slug}.pdf  (${size} KB)`);
      }
    }
  } finally {
    await browser.close();
  }

  // ── Cleanup temp dir ──────────────────────────────────────────────────────
  try {
    fs.rmSync(MERMAID_TMP, { recursive: true, force: true });
  } catch (_) {}

  console.log("\n✅  Build complete!\n");
  if (doCombined)    console.log(`   📄  pdf/output/course.pdf`);
  if (doIndividual)  console.log(`   📁  pdf/output/lessons/*.pdf`);
  console.log();
}

main().catch((err) => {
  console.error("\n❌  Build failed:", err);
  process.exit(1);
});
