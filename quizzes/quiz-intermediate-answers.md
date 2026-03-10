# Intermediate Quiz — Answer Key

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

## Table of Contents


1. Because repositories affect ingest speed, retention behavior, restore speed, blast radius, and immutability.
2. It supports stronger resilience through immutability and reduced backup tampering risk.
3. It groups multiple extents into one logical repository design for growth and policy-based placement.
4. Because its settings should reflect business recovery needs, not arbitrary defaults.
5. Because policy mismatch, backup window growth, and troubleshooting complexity increase.
6. Because it strongly affects how efficiently the proxy reads source data.
7. Because jobs may still complete while the proxy is overloaded or falling back to a slower path.
8. Crash-consistent captures disk state; application-consistent coordinates with the guest and relevant applications for cleaner recovery.
9. Because they often require cleaner transaction state and better restore reliability.
10. When workloads are physical, standalone, isolated, or otherwise not best protected from the hypervisor layer.
11. Because recovery media, bootability, and hardware or driver assumptions become important.
12. Because NAS protection centers on file-share state, change tracking, indexing, and granular restores.
13. When service must return quickly and running temporarily from backup storage is acceptable.
14. Because it restores the needed item with minimal disruption.
15. Because it allows narrow-scope recovery of important objects without full system rollback.

[Go to TOC](#table-of-contents)
---

**License:** [CC BY-NC-SA 4.0](../LICENSE.md)
