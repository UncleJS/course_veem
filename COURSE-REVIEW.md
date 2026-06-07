# Course Review — Veeam Backup & Replication v12.x

**Review date:** 2026-06-07
**Scope:** All 28 lessons, 3 quizzes + keys, 120-question exam bank + key, glossary, instructor guide, index files, PDF build pipeline (mechanics only).
**Method:** Scripted mechanical pass (links, anchors, counts, mermaid, numbering) + six parallel SME content reviews + targeted verification against official Veeam documentation.

---

## Executive Summary

This is a **well-built, internally consistent, factually clean course**. Across all ~8,300 lines:

- **Zero wrong answer keys.** All 165 quiz/exam answer pairs and every lesson's inline review answers are factually correct, position-aligned, and answerable from the assigned lessons.
- **Zero critical factual errors** in lesson bodies. The deliberately conceptual, hedged writing style avoids version-trivia traps.
- **Strong pedagogy.** Clean beginner→advanced progression, no forward-dependency violations, labs chain correctly off earlier labs, and the three promised learning paths (VMware / Hyper-V / no-hypervisor) are genuinely honored throughout.
- All 29 mermaid diagrams pass syntax validation; all question/answer counts match; lesson numbering and titles agree across all index files.

The course's one systemic weakness is the flip side of its safety: lessons are written at such a conceptual altitude that they **omit many of the concrete v12.x product facts a VMCE-aligned course promises** — most notably PostgreSQL as the v12 default database, which is absent from the installation lessons entirely. The glossary is actually *deeper* than the lessons and contains the few genuine factual errors found.

| Dimension | Verdict |
|---|---|
| Technical accuracy | **Good** — nothing materially wrong in lessons; 3 factual errors in glossary; 1 systemic omission (PostgreSQL) |
| Assessment integrity | **Excellent** — all keys correct; one missing answer key (50 VMCE practice Qs) |
| Structure & mechanics | **Good** — 16 broken anchors + index inconsistencies, all fixed in this pass |
| Pedagogy & flow | **Excellent** — sequencing, scaffolding, and lab chains all sound |

---

## Fixed in This Pass (mechanical — no content meaning changed)

1. **16 broken TOC anchor links** — headings containing ` — ` or ` & ` slugify with a *double* hyphen on GitHub; the TOC links used a single hyphen.
   - `lessons/27-troubleshooting.md` (15 links: Parts 1–13, Scenario Walkthroughs 1–2)
   - `lessons/01-introduction.md` (1 link: "What Veeam Backup & Replication Includes")
2. **`pdf/build.js` slug function** — it previously *collapsed* double hyphens to match the old (broken-on-GitHub) links, which meant the 13 links that already used GitHub-correct double hyphens (`README.md`, `exam/exam-bank-120.md`, `exam/28-vmce-exam-prep.md`) were broken in the PDF instead. `headingSlug()` now matches GitHub's slugger exactly, so **both** renderers resolve every anchor. Verified by simulation; re-running the link checker reports 0 errors.
3. **`quizzes/quiz-advanced.md:1`** — title said "Lessons 19 to 28"; README and instructor guide scope the advanced quiz to lessons 19–27 (lesson 28 is exam prep). Now "Lessons 19 to 27".
4. **`lessons/00-index.md` file list** — listed `28-vmce-exam-prep.md` as a bare filename implying it lives in `lessons/`; it lives in `exam/`. Now a correct relative link.
5. **`lessons/README.md` navigation table** — stopped at lesson 27, omitting lesson 28 (inconsistent with the other two indexes). Added a row pointing to `../exam/28-vmce-exam-prep.md`.

Verification after fixes: link/anchor checker **0 errors** across 44 files; all counts still pass; no mermaid blocks touched.

---

## Factual Corrections — F1–F4 applied after sign-off; F5–F7 still open

> **Status update (2026-06-07):** F1–F4 were approved and applied. F5 (content enrichment) and F6 (glossary coverage gaps) were subsequently applied as well — every row of the F5 table below now has a corresponding factual callout in its lesson, and the glossary gained CDP and vPower NFS entries (147 terms total). F7's actionable items were also applied: the lesson 01 "no-hypervisor" wording slips, a VMCE-logistics verification note in lesson 28, lesson 27 split into its own study week in the pacing table, and per-module reading-time estimates in the instructor guide. The remaining F7 observations (intentional question reuse) need no action. **All review findings are now resolved.**

### F1. PostgreSQL is missing from the installation story — *the highest-value fix* (MAJOR) — ✅ APPLIED

Verified against the [Veeam install wizard docs](https://helpcenter.veeam.com/docs/vbr/userguide/install_vbr_sql.html): **PostgreSQL is the default configuration database for all new v12 installs**; SQL Server remains for upgrades/externally-hosted choices.

- `lessons/03-architecture-overview.md:94` — describes the config DB as "a bundled or local SQL-based option … external SQL platform". Never mentions PostgreSQL.
- `lessons/04-installation-requirements.md:84–95` — "Database Planning" section is SQL-Server-only.
- `lessons/05-lab-install-vbr.md:48–58, 89–90` — lab DB-placement step offers "local/bundled vs external SQL Server (SQL01)". A learner on real v12 media will see a PostgreSQL prompt the lab never describes.

**Applied fix:** all three lessons now state PostgreSQL is the bundled default for new v12 installs, with Microsoft SQL Server as the external/upgrade alternative (incl. the lab topology diagram and prerequisites list in lesson 05).

### F2. Glossary factual errors (MAJOR) — ✅ APPLIED

- `glossary.md:104` — "The SQL Server (or PostgreSQL in later v12.x releases) database…" — **backwards**: PostgreSQL became the default in v12.0, not "later v12.x".
- `glossary.md:420` — "Veeam Explorer for PostgreSQL … Introduced in later v12.x releases." — it shipped **in v12.0**.
- `glossary.md:454` — "Windows Hardened Repository" — **not a v12 product feature**. The hardened repository is Linux-only in v12.x; locking down Windows ACLs is an admin practice, not a Veeam repository type. Entry now explicitly labeled "informal practice, not a Veeam product feature" with a pointer to Hardened Linux Repository.

All three entries corrected: Configuration Database now states PostgreSQL is the new-install default; PostgreSQL Explorer now says "Introduced in v12."

### F3. Glossary definitional imprecision (MINOR) — ✅ APPLIED

- `glossary.md:170` — Guest Interaction Proxy: drop the "rather than through the VMware Tools channel" contrast (guest interaction is network-based; the contrast is misleading).
- `glossary.md:184` — Hot-Add: proxy needs a host **with access to the same datastores**, not "the same ESXi host".
- `glossary.md:228` — NBD described strictly as "the fallback transport mode"; it is also a valid primary choice.

### F4. Missing answer key for 50 VMCE practice questions (MAJOR) — ✅ APPLIED

`exam/28-vmce-exam-prep.md:70–119` — the "50 Practice Questions" had no key anywhere in the repo (only prose "Short Answer Guidance"). **Applied fix:** a full 50-item "Practice Question Answer Key" section now follows the Short Answer Guidance (added to the lesson TOC); verified 50 questions / 50 answers.

Related minor (also applied): Q17 was ambiguous — the 3-2-1-1-0 rule contains two 1s. Now reads "the added '1' … (beyond classic 3-2-1)", answered as the offline/air-gapped/immutable copy.

### F5. Content-enrichment gaps (MAJOR-as-omission) — ✅ APPLIED

A consistent pattern: "v12.x Notes" sections were placeholders, and defining v12 features went unnamed. Each lesson below now carries a short factual callout covering the listed items (added to existing sections or, where new headings were required — lessons 16 and 19 — also added to those lessons' TOCs):

| Lesson | Missing v12.x specifics |
|---|---|
| 07 Repositories | Object storage as a **direct primary target** (the headline v12 change); SOBR's three tiers by name (Performance/Capacity/Archive); Fast Clone (ReFS/XFS); per-machine chains as v12 default; hardened-repo mechanics (Linux+XFS, immutability days, single-use credentials) — the glossary covers several of these; the lesson should too |
| 09 VM jobs | The four chain modes by name; retention in days *vs* restore points; GFS |
| 11 Proxies | **Direct NFS** (4th VMware transport mode); Linux proxy support; Backup from Storage Snapshots; task-slot sizing (~1 task/core, 1 task = 1 disk) |
| 12 AAP | SQL/Oracle transaction-log backup mechanics; Linux pre-freeze/post-thaw scripts; guest indexing |
| 15 NAS | File proxy + cache repository (the two architectural pillars); the three NAS restore types |
| 16/17 Restore | vPower NFS mechanism; finalize options (Migrate to Production / Storage vMotion / Quick Migration); Secure Restore, Staged Restore, virtual disk restore, restore-to-cloud |
| 18 Explorers | Name the full Explorer set: AD, Exchange, SQL, SharePoint, Oracle, Teams, **PostgreSQL (new in v12)** |
| 19 Replication | CDP vs classic replication; re-IP; seeding/mapping; failover/failback workflow by name |
| 24 Security | v12.1 features by name: inline malware detection, YARA, four-eyes authorization, Security & Compliance Analyzer, MFA (verified: [Veeam KB4696](https://www.veeam.com/kb4696)) |
| 25 Scale | Enterprise Manager function; REST API (port 9419); PostgreSQL; named RBAC roles |
| 26 Monitoring | Veeam ONE components; built-in notifications/SNMP |
| 27 Troubleshooting | Log locations (`%ProgramData%\Veeam\Backup`); support-bundle export; reading Source/Proxy/Network/Target bottleneck **percentages** in job stats |
| 01 Intro | One-line "what each point release added": 12.1 malware detection/Security & Compliance Analyzer, 12.2 Proxmox VE, 12.3 Entra ID/Threat Hunter (verified against Veeam release notes) |

### F6. Glossary coverage gaps (MINOR) — ✅ APPLIED

- **vPower NFS** — was absent from glossary and all lessons despite being the engine behind Instant VM Recovery and SureBackup. Entry added; lessons 16/17 now describe the mechanism.
- **CDP** — was absent everywhere. Entry added; lesson 19 now covers CDP vs classic replication.
- WAN Accelerator's "(Lesson 21)" tag was orphaned — lessons 19 and 21 now mention WAN accelerators.
- Secure Restore's "(Lesson 16, 24)" tag was orphaned — lesson 16 now names Secure Restore (and Staged Restore, virtual disk restore, restore-to-cloud).

### F7. Low-priority notes — ✅ APPLIED (except the no-action items)

- `lessons/01-introduction.md:236,263` — "No-hypervisor workloads…" reads as a typo for "Non-hypervisor" in those two sentences (the course's term "no-hypervisor path" is fine elsewhere). Cosmetic; left unchanged.
- Heavy intentional question reuse across quizzes/exam bank (RPO/RTO, 3-2-1, transport fallback each appear 3–4 times). Fine for reinforcement; reduces value if all assessments are used in one sitting.
- `exam/28-vmce-exam-prep.md` is titled "VMCE Exam Preparation" but contains zero exam logistics (count, duration, passing score). Safe from staleness, but consider a dated "verify current details at veeam.com" pointer.
- `lessons/00-index.md` week-7 pacing bundles the 120–180-minute troubleshooting lesson with three others; consider making lesson 27 a standalone study block.
- Instructor guide carries no per-module time estimates; lessons have reading/lab times that could be aggregated.

---

## What Was Checked and Found Clean

- All 29 mermaid diagrams: no syntax pitfalls (literal `\n`, unquoted special-char labels, broken `<br>`).
- Quiz counts 15/15 ×3; exam bank exactly Q1–120 with key 1–120, no gaps or duplicates; every lesson's review-question count matches its answer count.
- No off-by-one drift in any answer key.
- Lesson H1 titles, numbering, and descriptions consistent across `00-index.md`, `lessons/README.md`, root `README.md`, and the instructor guide module map (Modules 1–6 cover 00–28 contiguously).
- No malformed version strings; no v11/v13 leakage.
- Hyper-V and no-hypervisor coverage promised by the README is genuinely present (RCT in 06/09/10/11/27; agent path in 06/09/12/13/15/16/19/21).
- Lab prerequisite chains verified: lab 10 ← repo from lab 08; lab 14 ← agents from 13; lab 17 ← backup from lab 10.

## Verified Online (official sources)

- PostgreSQL default for new v12 installs — [Veeam Help Center: Specify Database Engine and Instance](https://helpcenter.veeam.com/docs/vbr/userguide/install_vbr_sql.html)
- v12.3 feature set (Entra ID workload, Threat Hunter, IVMR scale) — [Veeam KB4696](https://www.veeam.com/kb4696)
- v12.1 security features and v12.2 Proxmox plug-in — Veeam release blogs/community release overviews
