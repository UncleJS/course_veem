#!/usr/bin/env python3
"""
generate.py — Build course-complete.md and course-complete.pdf

Usage (run from the repo root or from inside export/):
    python3 export/generate.py [--md-only] [--pdf-only]

Options:
    --md-only   Generate only the Markdown file (skip PDF)
    --pdf-only  Generate only the PDF (course-complete.md must already exist)

Output:
    export/course-complete.md
    export/course-complete.pdf

Source files are NEVER modified.
"""

import os
import re
import sys
import shutil
import subprocess

# ── Resolve paths ─────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.dirname(SCRIPT_DIR)
EXPORT_DIR  = SCRIPT_DIR
MD_OUT      = os.path.join(EXPORT_DIR, "course-complete.md")
PDF_OUT     = os.path.join(EXPORT_DIR, "course-complete.pdf")
CSS_FILE    = os.path.join(EXPORT_DIR, "pdf-style.css")

# ── Source file order ──────────────────────────────────────────────────────────

SOURCE_FILES = [
    "README.md",
    "lessons/README.md",
    "lessons/00-index.md",
    "lessons/01-introduction.md",
    "lessons/02-backup-fundamentals.md",
    "lessons/03-architecture-overview.md",
    "lessons/04-installation-requirements.md",
    "lessons/05-lab-install-vbr.md",
    "lessons/06-adding-infrastructure.md",
    "lessons/07-backup-repositories.md",
    "lessons/08-lab-configure-repository.md",
    "lessons/09-vm-backup-jobs.md",
    "lessons/10-lab-vm-backup-job.md",
    "lessons/11-backup-proxies.md",
    "lessons/12-application-aware-processing.md",
    "lessons/13-agent-based-backup.md",
    "lessons/14-lab-agent-backup.md",
    "lessons/15-nas-backup.md",
    "lessons/16-restore-options.md",
    "lessons/17-lab-instant-vm-recovery.md",
    "lessons/18-application-item-restore.md",
    "lessons/19-replication.md",
    "lessons/20-lab-replication.md",
    "lessons/21-backup-copy-jobs.md",
    "lessons/22-tape-support.md",
    "lessons/23-object-storage-cloud-tier.md",
    "lessons/24-security-hardening.md",
    "lessons/25-scale-enterprise.md",
    "lessons/26-monitoring-reporting.md",
    "lessons/27-troubleshooting.md",
    "quizzes/quiz-beginner.md",
    "quizzes/quiz-beginner-answers.md",
    "quizzes/quiz-intermediate.md",
    "quizzes/quiz-intermediate-answers.md",
    "quizzes/quiz-advanced.md",
    "quizzes/quiz-advanced-answers.md",
    "exam/28-vmce-exam-prep.md",
    "exam/exam-bank-120.md",
    "exam/exam-bank-120-answers.md",
    "glossary.md",
]

# ── Section prefix map ─────────────────────────────────────────────────────────

PREFIX_MAP = {
    "README.md":                                  "readme",
    "lessons/README.md":                          "lessons-index",
    "lessons/00-index.md":                        "course-index",
    "lessons/01-introduction.md":                 "l01",
    "lessons/02-backup-fundamentals.md":          "l02",
    "lessons/03-architecture-overview.md":        "l03",
    "lessons/04-installation-requirements.md":    "l04",
    "lessons/05-lab-install-vbr.md":              "l05",
    "lessons/06-adding-infrastructure.md":        "l06",
    "lessons/07-backup-repositories.md":          "l07",
    "lessons/08-lab-configure-repository.md":     "l08",
    "lessons/09-vm-backup-jobs.md":               "l09",
    "lessons/10-lab-vm-backup-job.md":            "l10",
    "lessons/11-backup-proxies.md":               "l11",
    "lessons/12-application-aware-processing.md": "l12",
    "lessons/13-agent-based-backup.md":           "l13",
    "lessons/14-lab-agent-backup.md":             "l14",
    "lessons/15-nas-backup.md":                   "l15",
    "lessons/16-restore-options.md":              "l16",
    "lessons/17-lab-instant-vm-recovery.md":      "l17",
    "lessons/18-application-item-restore.md":     "l18",
    "lessons/19-replication.md":                  "l19",
    "lessons/20-lab-replication.md":              "l20",
    "lessons/21-backup-copy-jobs.md":             "l21",
    "lessons/22-tape-support.md":                 "l22",
    "lessons/23-object-storage-cloud-tier.md":    "l23",
    "lessons/24-security-hardening.md":           "l24",
    "lessons/25-scale-enterprise.md":             "l25",
    "lessons/26-monitoring-reporting.md":         "l26",
    "lessons/27-troubleshooting.md":              "l27",
    "quizzes/quiz-beginner.md":                   "quiz-beg",
    "quizzes/quiz-beginner-answers.md":           "quiz-beg-ans",
    "quizzes/quiz-intermediate.md":               "quiz-int",
    "quizzes/quiz-intermediate-answers.md":       "quiz-int-ans",
    "quizzes/quiz-advanced.md":                   "quiz-adv",
    "quizzes/quiz-advanced-answers.md":           "quiz-adv-ans",
    "exam/28-vmce-exam-prep.md":                  "l28",
    "exam/exam-bank-120.md":                      "exam-bank",
    "exam/exam-bank-120-answers.md":              "exam-bank-ans",
    "glossary.md":                                "glossary",
}

# ── Section separator H1s injected before certain files ───────────────────────

SECTION_SEPARATORS = {
    "README.md":                  ("section-1-course-overview", "SECTION 1 — Course Overview"),
    "lessons/01-introduction.md": ("section-2-lessons",         "SECTION 2 — Lessons"),
    "quizzes/quiz-beginner.md":   ("section-3-quizzes",         "SECTION 3 — Quizzes"),
    "exam/28-vmce-exam-prep.md":  ("section-4-exam-prep",       "SECTION 4 — Exam Prep"),
    "glossary.md":                ("section-5-reference",       "SECTION 5 — Reference"),
}

# ── Master TOC ─────────────────────────────────────────────────────────────────

MASTER_TOC_ENTRIES = {
    "Section 1 — Course Overview": [
        ("Veeam Backup & Replication v12.x Course",
         "veeam-backup-replication-v12x-course"),
        ("Lessons Index",
         "lessons-index"),
    ],
    "Section 2 — Lessons": [
        ("Veeam Backup & Replication v12.x — Beginner to Advanced Course",
         "veeam-backup-replication-v12x-beginner-to-advanced-course"),
        ("Lesson 1 — Veeam Backup & Replication v12: Product Overview, Editions and Licensing",
         "lesson-1-veeam-backup-replication-v12-product-overview-editions-and-licensing"),
        ("Lesson 2 — Backup Theory: RPO, RTO, 3-2-1 and Backup Types",
         "lesson-2-backup-theory-rpo-rto-3-2-1-and-backup-types"),
        ("Lesson 3 — Veeam Architecture: Components, Data Flow and Deployment Models",
         "lesson-3-veeam-architecture-components-data-flow-and-deployment-models"),
        ("Lesson 4 — Planning Your Deployment: Requirements, Ports, Service Accounts and Readiness",
         "lesson-4-planning-your-deployment-requirements-ports-service-accounts-and-readiness"),
        ("Lesson 5 — Lab: Installing Veeam Backup & Replication v12 on Windows Server",
         "lesson-5-lab-installing-veeam-backup-replication-v12-on-windows-server"),
        ("Lesson 6 — Adding Managed Infrastructure: vCenter, Hyper-V, Windows, Linux and Physical Systems",
         "lesson-6-adding-managed-infrastructure-vcenter-hyper-v-windows-linux-and-physical-systems"),
        ("Lesson 7 — Backup Repositories: Types, Design, Performance and Resilience",
         "lesson-7-backup-repositories-types-design-performance-and-resilience"),
        ("Lesson 8 — Lab: Configure a Repository and Scale-Out Backup Repository (SOBR)",
         "lesson-8-lab-configure-a-repository-and-scale-out-backup-repository-sobr"),
        ("Lesson 9 — VM Backup Jobs: Settings, Scheduling, Retention and Recovery Intent",
         "lesson-9-vm-backup-jobs-settings-scheduling-retention-and-recovery-intent"),
        ("Lesson 10 — Lab: Create and Run a VM Backup Job (VMware and Hyper-V)",
         "lesson-10-lab-create-and-run-a-vm-backup-job-vmware-and-hyper-v"),
        ("Lesson 11 — Backup Proxies: Data Movement, Transport Modes and Performance Behavior",
         "lesson-11-backup-proxies-data-movement-transport-modes-and-performance-behavior"),
        ("Lesson 12 — Application-Aware Processing: Consistency, Guest Interaction and Transaction-Safe Recovery",
         "lesson-12-application-aware-processing-consistency-guest-interaction-and-transaction-safe-recovery"),
        ("Lesson 13 — Agent-Based Backup: Windows, Linux and the No-Hypervisor Protection Model",
         "lesson-13-agent-based-backup-windows-linux-and-the-no-hypervisor-protection-model"),
        ("Lesson 14 — Lab: Deploy an Agent Policy for Windows and Linux Workloads",
         "lesson-14-lab-deploy-an-agent-policy-for-windows-and-linux-workloads"),
        ("Lesson 15 — NAS Backup: File Share Protection, Change Tracking and Recovery Expectations",
         "lesson-15-nas-backup-file-share-protection-change-tracking-and-recovery-expectations"),
        ("Lesson 16 — Restore Options Overview: VM, File, Volume and Service Recovery",
         "lesson-16-restore-options-overview-vm-file-volume-and-service-recovery"),
        ("Lesson 17 — Lab: Instant VM Recovery and Recovery Validation",
         "lesson-17-lab-instant-vm-recovery-and-recovery-validation"),
        ("Lesson 18 — Veeam Explorers and Application Item Recovery",
         "lesson-18-veeam-explorers-and-application-item-recovery"),
        ("Lesson 19 — VM Replication: Design, Use Cases and Failover Strategy",
         "lesson-19-vm-replication-design-use-cases-and-failover-strategy"),
        ("Lesson 20 — Lab: Configure Replication and Perform a Planned Failover",
         "lesson-20-lab-configure-replication-and-perform-a-planned-failover"),
        ("Lesson 21 — Backup Copy Jobs: Secondary Protection, GFS and Retention Strategy",
         "lesson-21-backup-copy-jobs-secondary-protection-gfs-and-retention-strategy"),
        ("Lesson 22 — Tape Infrastructure: Archive Workflows, Media Pools and Long-Term Retention",
         "lesson-22-tape-infrastructure-archive-workflows-media-pools-and-long-term-retention"),
        ("Lesson 23 — Object Storage, Capacity Tier and Cloud-Aligned Retention Design",
         "lesson-23-object-storage-capacity-tier-and-cloud-aligned-retention-design"),
        ("Lesson 24 — Security Hardening: Immutability, Least Privilege and Cyber-Resilient Backup Operations",
         "lesson-24-security-hardening-immutability-least-privilege-and-cyber-resilient-backup-operations"),
        ("Lesson 25 — Enterprise Scale: Enterprise Manager, RBAC, REST API and Automation Concepts",
         "lesson-25-enterprise-scale-enterprise-manager-rbac-rest-api-and-automation-concepts"),
        ("Lesson 26 — Monitoring and Reporting: Health Visibility, Capacity Planning and Operational Confidence",
         "lesson-26-monitoring-and-reporting-health-visibility-capacity-planning-and-operational-confidence"),
        ("Lesson 27 — Deep-Dive Troubleshooting: Common Failures, Root Causes and Recovery Tactics",
         "lesson-27-deep-dive-troubleshooting-common-failures-root-causes-and-recovery-tactics"),
    ],
    "Section 3 — Quizzes": [
        ("Beginner Quiz — Lessons 1 to 6",      "beginner-quiz-lessons-1-to-6"),
        ("Beginner Quiz — Answer Key",           "beginner-quiz-answer-key"),
        ("Intermediate Quiz — Lessons 7 to 18", "intermediate-quiz-lessons-7-to-18"),
        ("Intermediate Quiz — Answer Key",       "intermediate-quiz-answer-key"),
        ("Advanced Quiz — Lessons 19 to 28",    "advanced-quiz-lessons-19-to-28"),
        ("Advanced Quiz — Answer Key",           "advanced-quiz-answer-key"),
    ],
    "Section 4 — Exam Prep": [
        ("Lesson 28 — VMCE Exam Preparation: Review, Scenario Practice and Reference Lab Appendix",
         "lesson-28-vmce-exam-preparation-review-scenario-practice-and-reference-lab-appendix"),
        ("Veeam Backup & Replication v12.x Master Exam Bank",
         "veeam-backup-replication-v12x-master-exam-bank"),
        ("Veeam Backup & Replication v12.x Master Exam Bank — Answer Key",
         "veeam-backup-replication-v12x-master-exam-bank-answer-key"),
    ],
    "Section 5 — Reference": [
        ("Glossary of Terms — Veeam Backup & Replication v12.x",
         "glossary-of-terms-veeam-backup-replication-v12x"),
    ],
}

# ── Slug helpers ───────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert heading text to a GitHub-compatible anchor slug."""
    text = text.lower()
    text = re.sub(r'[—–]', '-', text)           # em/en dash → hyphen
    text = re.sub(r'[^\w\s-]', '', text)         # strip punctuation (incl. &)
    text = re.sub(r'[\s_]+', '-', text)          # whitespace → hyphen
    text = re.sub(r'-+', '-', text)              # collapse hyphens
    return text.strip('-')


def toc_anchor(prefix: str) -> str:
    return f"toc-{prefix}"


def h1_anchor(heading_text: str) -> str:
    return slugify(heading_text)


def scoped_anchor(prefix: str, heading_text: str) -> str:
    return f"{prefix}-{slugify(heading_text)}"

# ── Per-file link rewrite map ──────────────────────────────────────────────────

def slugify_github_old(text: str) -> str:
    """
    Reproduce GitHub's OLD slugging behaviour where:
      - spaces, tabs, underscores  → hyphen (each char individually)
      - literal hyphens            → kept as-is
      - em dash (—), en dash (–),
        ampersand (&), colon, etc. → STRIPPED (no hyphen inserted)
      - word chars (\\w)            → kept (lowercased)

    This produces double-hyphens wherever a stripped non-word char sat between
    two spaces, e.g. "Backup & Replication" → "backup--replication" and
    "Section 1 — Fundamentals" → "section-1--fundamentals".

    Some source TOC links were generated under this old scheme; we map those
    targets back to the correct final (modern) anchor.
    """
    result = []
    for ch in text.lower():
        if ch in (' ', '\t', '_'):
            result.append('-')
        elif ch == '-':
            result.append('-')
        elif re.match(r'\w', ch):
            result.append(ch)
        # else: strip silently (em dash, en dash, &, ., :, (, ), etc.)
    return ''.join(result).strip('-')


def build_link_rewrite_map(text: str, prefix: str) -> dict:
    """
    Scan all H1/H2/H3 headings in *text* and return a dict mapping
    source-file slug variants → final anchor id used in the combined doc.

    Two slug variants are mapped per heading so that both the modern
    (collapsed) and old (double-hyphen) link targets resolve correctly:
        modern slug  → final anchor
        old slug     → final anchor   (only added when it differs)
    """
    mapping = {}
    for m in re.finditer(r'^(#{1,3})\s+(.+)$', text, re.MULTILINE):
        level   = len(m.group(1))
        heading = m.group(2).strip()

        modern_slug = slugify(heading)
        old_slug    = slugify_github_old(heading)

        if level == 1:
            final_anchor = h1_anchor(heading)
        elif re.match(r'^Table of Contents', heading, re.IGNORECASE):
            final_anchor = toc_anchor(prefix)
        else:
            final_anchor = scoped_anchor(prefix, heading)

        mapping[modern_slug] = final_anchor
        if old_slug != modern_slug:
            mapping[old_slug] = final_anchor

    return mapping


def rewrite_internal_links(text: str, link_map: dict) -> str:
    """
    Rewrite every internal Markdown link `[...](#old-slug)` to
    `[...](#new-anchor)` using the provided map.

    Links whose target is not in the map are left unchanged
    (they are cross-file links that were already handled by the master TOC,
    or external links).
    """
    def replacer(m):
        link_text = m.group(1)
        target    = m.group(2)
        new_target = link_map.get(target, target)
        return f"[{link_text}](#{new_target})"

    return re.sub(r'\[([^\]]+)\]\(#([^)]+)\)', replacer, text)

# ── Nav block rewrite ──────────────────────────────────────────────────────────

def rewrite_nav_blocks(text: str, prefix: str) -> str:
    """
    Replace `[Go to TOC](#table-of-contents)` nav links (which may already be
    surrounded by `---` lines in source) with the full normalised dual-nav block:

        ---

        [Go to Lesson TOC](#toc-{prefix})

        [Go to Course TOC](#master-table-of-contents)

        ---
    """
    replacement = (
        "---\n\n"
        f"[Go to Lesson TOC](#{toc_anchor(prefix)})\n\n"
        "[Go to Course TOC](#master-table-of-contents)\n\n"
        "---"
    )
    # Match: optional leading ---, optional blank lines, the Go to TOC link,
    #        optional blank lines, optional trailing ---
    pattern = re.compile(
        r'(?:^---\s*\n+)?'
        r'\[Go to TOC\]\(#[^)]+\)'
        r'(?:\s*\n+---)?',
        re.MULTILINE
    )
    return pattern.sub(replacement, text)

# ── Anchor injection ───────────────────────────────────────────────────────────

def inject_anchors(text: str, prefix: str) -> str:
    """
    Walk every line; before each H1/H2/H3 inject `<a id="..."></a>` on its
    own line (if not already present).

    H1   → slugify(heading_text)
    TOC  → toc-{prefix}
    H2/H3 → {prefix}-{slug}
    """
    lines  = text.split('\n')
    result = []

    for line in lines:
        m = re.match(r'^(#{1,3})\s+(.+)$', line)
        if m:
            level   = len(m.group(1))
            heading = m.group(2).strip()

            if level == 1:
                anchor = h1_anchor(heading)
            elif re.match(r'^Table of Contents', heading, re.IGNORECASE):
                anchor = toc_anchor(prefix)
            else:
                anchor = scoped_anchor(prefix, heading)

            anchor_tag = f'<a id="{anchor}"></a>'

            # Don't duplicate: check the last non-empty result line
            last_nonempty = next(
                (l for l in reversed(result) if l.strip()), ""
            )
            if last_nonempty != anchor_tag:
                # If the last non-empty line is a different <a id>, replace it
                if re.match(r'^<a id="', last_nonempty):
                    for i in range(len(result) - 1, -1, -1):
                        if result[i].strip():
                            result[i] = anchor_tag
                            break
                else:
                    result.append(anchor_tag)

        result.append(line)

    return '\n'.join(result)

# ── Master TOC builder ─────────────────────────────────────────────────────────

def build_master_toc() -> str:
    lines = [
        '<a id="master-table-of-contents"></a>',
        "",
        "## Master Table of Contents",
        "",
    ]
    for section, entries in MASTER_TOC_ENTRIES.items():
        lines.append(f"### {section}")
        lines.append("")
        for display, anchor in entries:
            lines.append(f"- [{display}](#{anchor})")
        lines.append("")
    return "\n".join(lines)

# ── Main build ─────────────────────────────────────────────────────────────────

def build_markdown() -> None:
    print("Building course-complete.md …")

    parts = []

    # File header
    parts.append("> [!NOTE]")
    parts.append("> Auto-generated combined document — do not edit manually.")
    parts.append("")
    parts.append('<a id="course-complete-export"></a>')
    parts.append("# Course Complete Export")
    parts.append("")
    parts.append(build_master_toc())
    parts.append("")
    parts.append("---")
    parts.append("")

    for rel_path in SOURCE_FILES:
        abs_path = os.path.join(REPO_ROOT, rel_path)
        prefix   = PREFIX_MAP[rel_path]

        if not os.path.exists(abs_path):
            print(f"  WARNING: source file not found — {rel_path}", file=sys.stderr)
            continue

        with open(abs_path, encoding="utf-8") as fh:
            raw = fh.read()

        # Optional section separator H1
        if rel_path in SECTION_SEPARATORS:
            sep_anchor, sep_heading = SECTION_SEPARATORS[rel_path]
            parts.append(f'<a id="{sep_anchor}"></a>')
            parts.append(f"# {sep_heading}")
            parts.append("")

        # Build the within-file link rewrite map BEFORE any transformations
        link_map = build_link_rewrite_map(raw, prefix)

        # Extra aliases: some source files use legacy link targets that
        # cannot be inferred from heading text alone.
        # Key = legacy target found in links; Value = correct final anchor.
        EXTRA_ALIASES = {
            # glossary.md: [X–Z](#xz) — GitHub used to strip en-dash entirely
            "xz": f"{prefix}-x-z",
        }
        link_map.update(EXTRA_ALIASES)

        # 1. Rewrite [Go to TOC] → dual nav blocks
        text = rewrite_nav_blocks(raw, prefix)

        # 2. Rewrite all internal heading links to scoped targets
        text = rewrite_internal_links(text, link_map)

        # 3. Inject <a id> anchors before every H1/H2/H3
        text = inject_anchors(text, prefix)

        parts.append(text.rstrip())
        parts.append("")
        parts.append("---")
        parts.append("")

    content = "\n".join(parts)

    with open(MD_OUT, "w", encoding="utf-8") as fh:
        fh.write(content)

    line_count = content.count("\n")
    print(f"  Written : {MD_OUT}  ({line_count:,} lines)")

    # Sanity check
    defined = set(re.findall(r'<a id="([^"]+)"', content))
    links   = re.findall(r'\[[^\]]+\]\(#([^)]+)\)', content)
    broken  = [t for t in links if t not in defined]
    print(f"  Anchors : {len(defined)}")
    print(f"  Links   : {len(links)}")
    print(f"  Broken  : {len(broken)}")
    if broken:
        print("  ── Broken link targets ──")
        for b in sorted(set(broken))[:30]:
            print(f"    #{b}")
        if len(set(broken)) > 30:
            print(f"    … and {len(set(broken)) - 30} more unique targets")


def build_pdf() -> None:
    print("Building course-complete.pdf …")

    if not os.path.exists(MD_OUT):
        print(f"  ERROR: {MD_OUT} not found — run without --pdf-only first.",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(CSS_FILE):
        print(f"  ERROR: {CSS_FILE} not found (expected alongside this script).",
              file=sys.stderr)
        sys.exit(1)

    # Prefer the binary on PATH; fall back to npx (which can download on demand)
    if shutil.which("md-to-pdf"):
        md_to_pdf_cmd = ["md-to-pdf"]
    elif shutil.which("npx"):
        md_to_pdf_cmd = ["npx", "--yes", "md-to-pdf"]
    else:
        print("  ERROR: neither md-to-pdf nor npx found on PATH.", file=sys.stderr)
        print("    Install with:  npm install -g md-to-pdf", file=sys.stderr)
        sys.exit(1)

    cmd = md_to_pdf_cmd + [
        MD_OUT,
        "--config-file", "/dev/null",
        "--highlight-style", "github",
        "--stylesheet", CSS_FILE,
        "--pdf-options", '{"format":"A4","printBackground":true}',
        "--launch-options", '{"args":["--no-sandbox"]}',
        # Output is written as <input-basename>.pdf in the same directory.
        # Since MD_OUT is already in EXPORT_DIR, this produces PDF_OUT directly.
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  ERROR: md-to-pdf failed.", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(PDF_OUT) / 1_048_576
    print(f"  Written : {PDF_OUT}  ({size_mb:.1f} MB)")


def main() -> None:
    args     = sys.argv[1:]
    md_only  = "--md-only"  in args
    pdf_only = "--pdf-only" in args

    if md_only and pdf_only:
        print("ERROR: --md-only and --pdf-only are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    if not pdf_only:
        build_markdown()

    if not md_only:
        build_pdf()

    print("Done.")


if __name__ == "__main__":
    main()
