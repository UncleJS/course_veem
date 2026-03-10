# Instructor Guide and Module-Based Syllabus

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

## Table of Contents

- [Course Purpose](#course-purpose)
- [Delivery Options](#delivery-options)
- [Suggested Module Structure](#suggested-module-structure)
- [Assessment Model](#assessment-model)
- [Recommended Milestones](#recommended-milestones)
- [Instructor Question Bank Prompts](#instructor-question-bank-prompts)
- [Practical Teaching Advice](#practical-teaching-advice)
- [Suggested Deliverables for Learners](#suggested-deliverables-for-learners)
- [Use With the Quiz and Exam Bank Files](#use-with-the-quiz-and-exam-bank-files)

[Go to TOC](#table-of-contents)

## Course Purpose

This guide helps an instructor, team lead, or internal trainer deliver the Veeam Backup & Replication v12.x course as a structured program rather than only a self-study reading pack.

[Go to TOC](#table-of-contents)

## Delivery Options

- self-study with weekly check-ins
- live internal training over 6 to 8 weeks
- compressed bootcamp for experienced administrators
- blended model with reading before live lab sessions

[Go to TOC](#table-of-contents)

## Suggested Module Structure

### Module 1 — Foundations

Lessons: 00 to 04  
Learning goal: Build shared vocabulary, architecture awareness, and planning discipline.

Instructor focus:

- make sure learners can explain RPO and RTO in business language
- make sure learners stop thinking of backup as only a nightly task
- challenge vague architecture answers until learners can name the main components clearly

Suggested live exercise:

- ask learners to design a minimal Veeam environment for a small company and justify each component

### Module 2 — Core Platform Setup

Lessons: 05 to 09  
Learning goal: Install Veeam, add infrastructure, understand repositories, and design meaningful jobs.

Instructor focus:

- watch for overuse of defaults
- ask learners why each repository or job choice was made
- reinforce that install success is not deployment quality

Suggested live exercise:

- compare two job designs for the same environment and discuss which is more resilient

### Module 3 — Data Processing and Mixed Workloads

Lessons: 10 to 15  
Learning goal: Understand job behavior, proxy impact, application-aware processing, agents, and NAS.

Instructor focus:

- challenge learners to explain the difference between hypervisor-based and agent-based protection
- use examples where a physical system is more important than a VM
- ask when application-aware processing is mandatory and when it is optional

Suggested live exercise:

- case study with one VMware workload, one Hyper-V workload, one physical server, and one file share

### Module 4 — Restore and DR

Lessons: 16 to 21  
Learning goal: Choose the right restore method, understand replication, and design secondary copy strategy.

Instructor focus:

- do not let learners answer every scenario with full restore
- insist on the difference between low RTO and long retention
- make learners articulate the purpose of failback, not only failover

Suggested live exercise:

- give five incident scenarios and require learners to map each to a recovery action

### Module 5 — Long-Term Retention, Security and Scale

Lessons: 22 to 26  
Learning goal: Understand tape, object storage, hardening, RBAC, automation, monitoring, and governance.

Instructor focus:

- reinforce that security is part of backup design
- ask learners to compare repository choices under both performance and ransomware pressure
- make learners define what a good weekly report should answer

Suggested live exercise:

- security review of a fictional backup design with weak credentials and no immutable copy

### Module 6 — Troubleshooting and Exam Readiness

Lessons: 27 to 28  
Learning goal: Troubleshoot by layer and reason through VMCE-style questions.

Instructor focus:

- teach calm, layered diagnosis rather than message memorization
- insist on identifying the first failing component
- use scenario questioning instead of trivia

Suggested live exercise:

- troubleshooting tabletop using three failure cases and one recovery validation failure

[Go to TOC](#table-of-contents)

## Assessment Model

Use three kinds of assessment:

1. **Concept checks** — short oral or written explanations
2. **Lab checks** — demonstration of backup and restore tasks
3. **Scenario checks** — design or troubleshooting reasoning

[Go to TOC](#table-of-contents)

## Recommended Milestones

- after Module 1: learner can explain Veeam architecture and planning basics
- after Module 2: learner can install and onboard core components
- after Module 3: learner can protect mixed workload types confidently
- after Module 4: learner can choose the correct restore or DR approach
- after Module 5: learner can critique a weak design from security and governance perspectives
- after Module 6: learner can troubleshoot and answer scenario questions with clear reasoning

[Go to TOC](#table-of-contents)

## Instructor Question Bank Prompts

Use prompts like these in discussion:

- Why is this a backup problem rather than a storage problem?
- Why is this a restore problem rather than a backup problem?
- What would happen if the primary repository disappeared right now?
- Which credential do you expect this workflow to use?
- What changed in the environment before the failure?
- What is the smallest safe test that would validate your theory?

[Go to TOC](#table-of-contents)

## Practical Teaching Advice

- ask learners to explain design choices aloud
- prefer scenario questions over memorization drills
- require recovery validation, not only job creation
- revisit warnings and weak signals, not only hard failures
- make no-hypervisor systems part of the core curriculum, not an optional appendix

[Go to TOC](#table-of-contents)

## Suggested Deliverables for Learners

By the end of the course, each learner should be able to submit:

- a simple architecture diagram
- one backup policy rationale document
- one restore decision matrix
- one troubleshooting checklist
- one short hardening plan for a Veeam environment

[Go to TOC](#table-of-contents)

## Use With the Quiz and Exam Bank Files

Recommended progression:

- module quiz after each major block
- `exam/exam-bank-120.md` for final mock review
- `exam/28-vmce-exam-prep.md` as the closing consolidation lesson

[Go to TOC](#table-of-contents)

---

**License:** [CC BY-NC-SA 4.0](LICENSE.md)
