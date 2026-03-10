# Veeam Backup & Replication v12.x Master Exam Bank

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

## Table of Contents

- [Section 1 — Fundamentals](#section-1-fundamentals)
- [Section 2 — Architecture](#section-2-architecture)
- [Section 3 — Installation and Infrastructure](#section-3-installation-and-infrastructure)
- [Section 4 — Repositories and Storage](#section-4-repositories-and-storage)
- [Section 5 — Jobs and Processing](#section-5-jobs-and-processing)
- [Section 6 — Proxy, Source and Platform Behavior](#section-6-proxy-source-and-platform-behavior)
- [Section 7 — Agents, NAS and Mixed Environments](#section-7-agents-nas-and-mixed-environments)
- [Section 8 — Restore and Recovery](#section-8-restore-and-recovery)
- [Section 9 — Replication, Copy, Scale and Operations](#section-9-replication-copy-scale-and-operations)
- [Section 10 — Troubleshooting and Exam Reasoning](#section-10-troubleshooting-and-exam-reasoning)

This file provides a larger practice bank for review sessions, mock exams, and instructor-led study. Questions are grouped by module for easier reuse.

[Go to TOC](#table-of-contents)

## Section 1 — Fundamentals

1. What is the practical difference between backup and recovery?
2. Why is Veeam best described as a recovery platform?
3. What is the difference between RPO and RTO?
4. Why does the 3-2-1 rule still matter?
5. What does an immutable copy protect against?
6. Why does retention need to be discussed separately from backup frequency?
7. What is a backup copy job meant to solve?
8. Why is replication not the same thing as backup?
9. Why should restore testing be part of backup strategy?
10. Why is application consistency important?
11. Why do organizations often need more than one kind of recovery path?
12. Why can a green job still hide operational risk?
13. What does “operational restore point” mean in practice?
14. Why should delayed incident discovery influence retention?
15. What is one practical reason to protect physical systems with the same seriousness as VMs?

[Go to TOC](#table-of-contents)

## Section 2 — Architecture

16. What is the role of the backup server?
17. What is the role of the proxy?
18. What is the role of the repository?
19. Why is the configuration database important?
20. Why can an all-in-one Veeam design become a limitation?
21. What is a management boundary in Veeam architecture?
22. What is a data movement boundary?
23. Why should fault domains matter in architecture design?
24. Why is a repository also a security boundary?
25. Why should architecture be understandable by more than one administrator?
26. What risks appear when control plane and storage plane are too tightly coupled?
27. Why should architecture planning include growth?
28. Why should a Veeam server itself be protected as a critical workload?
29. Why is documentation part of architecture quality?
30. What makes an architecture “works today” but weak tomorrow?

[Go to TOC](#table-of-contents)

## Section 3 — Installation and Infrastructure

31. Why should installation planning happen before running setup?
32. What can poor DNS cause during onboarding?
33. Why should time synchronization be checked?
34. Why should credentials be separated by purpose?
35. Why does repository planning belong in deployment planning?
36. What is one risk of using a domain admin account everywhere?
37. Why should pending reboots be cleared before installation?
38. What should be documented immediately after install?
39. Why is infrastructure onboarding a trust exercise?
40. Why should vCenter usually be added rather than only ESXi hosts one by one?
41. What often makes Hyper-V onboarding more sensitive than expected?
42. Why do Linux managed-server deployments deserve validation before production use?
43. Why should stored credentials be labeled clearly?
44. What kinds of failures commonly follow password rotation?
45. Why should no-hypervisor endpoints be included in early infrastructure onboarding?

[Go to TOC](#table-of-contents)

## Section 4 — Repositories and Storage

46. Why is repository design more than choosing a path?
47. What makes a hardened Linux repository important?
48. What is a SOBR trying to achieve?
49. Why does object storage matter in modern Veeam design?
50. Why should repository decisions include restore speed?
51. What is one common risk of underplanned repository growth?
52. Why do repository maintenance operations matter?
53. Why is one repository rarely enough?
54. Why should one copy differ meaningfully from the first copy?
55. Why do object storage designs still need restore planning?
56. When might tape still be useful?
57. Why are repositories attractive targets in ransomware scenarios?
58. What is one advantage of keeping an immutable copy?
59. Why should repository ownership be documented?
60. Why is capacity planning a backup topic rather than only a storage topic?

[Go to TOC](#table-of-contents)

## Section 5 — Jobs and Processing

61. Why should a backup job be designed around recovery intent?
62. Why can over-grouping workloads be harmful?
63. Why does job naming matter?
64. Why should scheduling consider more than “overnight”?
65. Why should security be considered in job design?
66. What is crash-consistent backup?
67. What is application-consistent backup?
68. Why do SQL workloads often need application-aware processing?
69. What is one common cause of guest processing failure?
70. Why should guest processing warnings be reviewed carefully?
71. Why should backup copy planning be considered when designing the primary job?
72. Why does retention need to fit both ordinary mistakes and serious incidents?
73. Why should a workload’s business role influence its job settings?
74. What is one reason a job may succeed but still be poorly designed?
75. Why should job review happen before broad production rollout?

[Go to TOC](#table-of-contents)

## Section 6 — Proxy, Source and Platform Behavior

76. Why is the proxy often central to performance?
77. What is one reason a VMware job may become slower without failing?
78. Why does transport mode matter?
79. What is one risk of a HotAdd expectation not being met?
80. Why should concurrency be considered in proxy planning?
81. What is one sign that a proxy is overloaded?
82. Why are VMware snapshot issues operationally important?
83. Why can CBT problems create confusing symptoms?
84. Why do Hyper-V jobs often require attention to VSS or checkpoint behavior?
85. Why should cluster behavior be considered in Hyper-V troubleshooting?

[Go to TOC](#table-of-contents)

## Section 7 — Agents, NAS and Mixed Environments

86. When is Veeam Agent the better protection model?
87. Why is endpoint health more visible in agent-based backup?
88. Why are recovery media important for physical systems?
89. What is one Linux-specific deployment risk for agents?
90. Why should agent policies be standardized where practical?
91. Why is NAS backup a distinct workload category?
92. Why does cache behavior matter in NAS backup?
93. Why are file-share workloads common ransomware targets?
94. Why should no-hypervisor environments still care about secondary copies?
95. Why is mixed-environment thinking important for Veeam administrators?

[Go to TOC](#table-of-contents)

## Section 8 — Restore and Recovery

96. When is Instant VM Recovery the best answer?
97. When is guest file restore the best answer?
98. Why should full VM restore not be the default response to every incident?
99. Why should application item restore be preferred when possible?
100. Why is a booted VM not automatically a recovered service?
101. Why should target mapping be reviewed during restore?
102. Why is clean restore-point selection important after suspected compromise?
103. What makes physical recovery more demanding than many VM recoveries?
104. Why is post-restore validation a required step?
105. Why should recovery ownership be clear before an incident?

[Go to TOC](#table-of-contents)

## Section 9 — Replication, Copy, Scale and Operations

106. Why is failback part of DR planning?
107. Why should replication be selective rather than automatic for every workload?
108. Why does backup copy complement replication?
109. Why do larger environments need RBAC?
110. Why is automation strongest when the process already works manually?
111. Why is monitoring more than counting success states?
112. Why do recurring warnings deserve trend review?
113. Why should capacity be reviewed periodically rather than only when full?
114. Why is standardization valuable at enterprise scale?
115. Why should security review and operations review intersect in backup environments?

[Go to TOC](#table-of-contents)

## Section 10 — Troubleshooting and Exam Reasoning

116. What is the first useful troubleshooting question after a job fails?
117. Why should you ask what changed recently?
118. Why is random setting-changing a bad habit?
119. What is the difference between symptom and root cause?
120. Why is layered troubleshooting more effective than memorizing isolated error strings?

[Go to TOC](#table-of-contents)
---

**License:** [CC BY-NC-SA 4.0](../LICENSE.md)
