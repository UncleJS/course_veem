# Veeam Backup & Replication v12.x Master Exam Bank — Answer Key

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

## Table of Contents


1. Backup creates recovery data; recovery is the use of that data to restore service or content.
2. Because its real value is enabling recovery outcomes across many workload types.
3. RPO is acceptable data loss; RTO is acceptable downtime.
4. It enforces copy separation and resilience basics.
5. It helps protect backup history from alteration or deletion.
6. Because how often you back up and how long you keep backups answer different business questions.
7. It creates a separate additional copy for resilience.
8. Replication is for faster failover, not broad retention flexibility.
9. Because untested backups may not be trustworthy in practice.
10. It improves recovery quality for transactional workloads.
11. Because different incidents need different scopes and speeds of recovery.
12. Because warnings, hidden inconsistency, or weak design may still exist.
13. A restore point usable for normal operational recovery needs.
14. Because corruption or compromise may be discovered long after it started.
15. Because physical and standalone systems may still host critical business services.
16. It coordinates jobs, services, infrastructure awareness, and configuration state.
17. It reads and moves source data through the backup pipeline.
18. It stores restore points and influences retention, performance, and security.
19. It preserves critical environment metadata used to manage and rebuild the platform.
20. Because management, proxy, and repository load all compete on one system.
21. The part of the design responsible for orchestration and management control.
22. The part responsible for reading and transferring backup data.
23. Because one compromised or failed domain should not destroy every recovery option.
24. Because repository access directly affects survivability of backup data.
25. Because resilience depends on shared operational understanding, not one person’s memory.
26. A single compromise may impact both control and stored recovery data.
27. Because backup environments grow in workload count, retention, and complexity.
28. Because losing it can disrupt management and recovery operations widely.
29. It makes handoff, troubleshooting, and safe change easier.
30. A design that functions technically but cannot scale, be secured, or be operated consistently.
31. Because many later failures begin with poor planning assumptions.
32. Name resolution failures, trust issues, and onboarding problems.
33. Because authentication, logging, and coordination depend on it.
34. To reduce blast radius and simplify troubleshooting.
35. Because target placement and storage strategy shape the whole deployment.
36. It creates excessive risk and broadens compromise impact.
37. To avoid partial component deployment and unstable setup state.
38. Build version, database choice, service health, and baseline assumptions.
39. Because Veeam depends on trusted access to many systems.
40. It provides centralized inventory and cleaner operational management.
41. WinRM, remote permissions, and cluster behavior.
42. Because SSH success alone does not guarantee role deployment or privilege success.
43. To support rotation, clarity, and faster issue isolation.
44. Simultaneous authentication failures across multiple workflows.
45. Because they are core protected systems in many real environments.
46. Because it affects performance, retention, restore speed, maintenance, and security.
47. It supports stronger protection against tampering through immutability.
48. It creates a logical pool of extents for growth and policy-based storage use.
49. It improves scalable retention and off-site or separate-domain copy design.
50. Because backups are only useful if recovery speed meets requirements.
51. Forced retention cuts, failed jobs, or emergency storage changes.
52. Because real repositories must survive merges, checks, expansion, and repairs.
53. Because one repository can fail, fill, or be compromised.
54. To avoid identical risk across all backup copies.
55. Because restore speed, retrieval path, and target behavior still matter.
56. For archival retention, offline separation, or compliance needs.
57. Because they hold high-value recovery data.
58. It improves the odds that backup history survives attack or error.
59. To ensure clear responsibility for maintenance and access.
60. Because storage exhaustion directly affects recovery readiness and job stability.
61. Because settings should reflect the recovery requirement, not convenience alone.
62. Because it mixes policies and makes windows and troubleshooting harder.
63. Because clear names improve operational clarity.
64. Because backup windows interact with application load, proxies, and storage behavior.
65. Because retention, encryption, and target choice all affect resilience.
66. Capturing disk state without app-aware coordination.
67. Capturing data with guest and application coordination for cleaner recovery.
68. Because transaction-heavy systems need better consistency.
69. Expired or incorrect guest credentials.
70. Because they may indicate meaningful application consistency risk.
71. Because primary jobs should be designed within a wider resilience chain.
72. Because daily mistakes and serious incidents need different historical depth.
73. Because business criticality should shape frequency, retention, and copy strategy.
74. It may run successfully while still having weak retention, grouping, or copy design.
75. To confirm the policy truly matches the recovery goal.
76. Because it often determines source-read efficiency and concurrency behavior.
77. Unexpected fallback to a slower transport mode.
78. It changes how efficiently data is read from the source.
79. The job may fall back or behave inefficiently.
80. Because too many tasks on one proxy reduce predictability and speed.
81. Queuing, inconsistent durations, or widespread slowdown.
82. Because they can affect backup quality and VM health.
83. Because backup size or change patterns may look wrong without obvious failure.
84. Because guest consistency and checkpoint mechanics are tightly involved.
85. Because host ownership and CSV behavior affect job execution.
86. When workloads are physical, standalone, or not best protected via hypervisor integration.
87. Because the local OS and endpoint state are directly part of the backup path.
88. Because full recovery may depend on bootable recovery tooling.
89. Kernel or snapshot-module compatibility issues.
90. To reduce drift and make administration clearer at scale.
91. Because it protects shares and file-state workflows rather than machine images.
92. Because it supports efficient awareness of file-share changes.
93. Because they centralize valuable user and departmental data.
94. Because resilience depends on copy separation regardless of workload type.
95. Because real environments combine VMs, physical systems, and file data.
96. When service must return quickly and a temporary run-from-backup state is acceptable.
97. When a narrow content restore solves the incident with minimal disruption.
98. Because it may be slower and broader than necessary.
99. Because targeted recovery is often safer and faster than whole-system rollback.
100. Because the application may still be unusable.
101. Because host, network, and datastore choices affect usable recovery.
102. Because restoring compromised data can recreate the incident.
103. Hardware, bootability, and driver assumptions all matter.
104. Because technical completion alone does not prove business usefulness.
105. Because incidents move faster when roles and decisions are already clear.
106. Because DR is incomplete if there is no plan to return or stabilize production.
107. Because not every workload justifies the extra complexity and target dependency.
108. Because copy jobs provide broader backup resilience that replication alone does not.
109. To support safer delegation and clearer operational boundaries.
110. Because automation should scale proven good process, not confusion.
111. Because capacity, warnings, drift, and unhealthy patterns matter too.
112. Because repeated warnings often indicate underlying weakness.
113. Because waiting until full creates avoidable operational risk.
114. It keeps large teams aligned in naming, workflows, and expectations.
115. Because backup resilience depends on both secure design and disciplined operation.
116. Which component or stage failed first.
117. Because environment changes often explain failures quickly.
118. Because it obscures cause and can create new problems.
119. A symptom is what you observe; root cause is why it happened.
120. Because classifying the failing layer narrows the real cause more reliably than memorizing messages alone.

[Go to TOC](#table-of-contents)

---

**License:** [CC BY-NC-SA 4.0](../LICENSE.md)
