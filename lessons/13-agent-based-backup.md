# Lesson 13 — Agent-Based Backup: Windows, Linux and the No-Hypervisor Protection Model

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

> **VMCE Objective(s):** Agent architecture, physical and standalone workload protection, policy-based management  
> **Level:** Intermediate  
> **Estimated reading time:** 60–75 minutes  
> **Lab time:** 40 minutes

## Table of Contents

- [Learning Objectives](#learning-objectives)
- [Concepts and Theory](#concepts-and-theory)
- [What an Agent Changes](#what-an-agent-changes)
- [Common Agent Use Cases](#common-agent-use-cases)
- [Windows and Linux Agent Considerations](#windows-and-linux-agent-considerations)
- [Managed vs. Standalone Thinking](#managed-vs-standalone-thinking)
- [What You Need to Protect Successfully With Agents](#what-you-need-to-protect-successfully-with-agents)
- [Recovery Scope in Agent Environments](#recovery-scope-in-agent-environments)
- [Policy Design for Agent Estates](#policy-design-for-agent-estates)
- [Why Agent Policies Matter](#why-agent-policies-matter)
- [No-Hypervisor Design Principles](#no-hypervisor-design-principles)
- [Common Agent Failure Themes](#common-agent-failure-themes)
- [v12.x Notes](#v12x-notes)
- [Lab Walkthrough](#lab-walkthrough)
- [Key Takeaways](#key-takeaways)
- [Review Questions](#review-questions)

[Go to TOC](#table-of-contents)

## Learning Objectives

- explain when Veeam Agent is the right protection model
- compare agent-managed protection with hypervisor-based image protection
- understand policy-based deployment concepts for Windows and Linux agents
- design no-hypervisor protection workflows for physical and standalone systems

[Go to TOC](#table-of-contents)

## Concepts and Theory

Not every important workload lives neatly inside a virtualized environment that Veeam can protect from the outside. Organizations still rely on physical servers, isolated application systems, edge devices, branch office systems, standalone cloud VMs, and Linux hosts that are better protected directly through an agent. This is where Veeam Agent becomes essential.

The no-hypervisor path in this course is not a secondary topic. It is a real-world operational pattern. Many backup failures in the field happen because teams unconsciously design everything around their hypervisor estate and forget that critical standalone workloads need equal attention.

[Go to TOC](#table-of-contents)

## What an Agent Changes

```mermaid
flowchart LR
    A[Protected Server] --> B[Veeam Agent]
    B --> C[Repository or Target]
    C --> D[Restore Options]
```

In hypervisor-based backup, Veeam often reads the VM from the outside through the virtualization stack. In agent-based protection, the protected machine itself participates directly in the backup process. That means backup behavior depends more explicitly on the operating system, local services, volume layout, and guest-level configuration.

The advantage is flexibility. The tradeoff is that you must think more carefully about endpoint health, deployment, and recovery media.

[Go to TOC](#table-of-contents)

## Common Agent Use Cases

Typical reasons to use Veeam Agent include:

- physical Windows server protection
- physical Linux server protection
- standalone machines outside the main hypervisor estate
- cloud-hosted systems where agent control is preferable or necessary
- branch or edge workloads where centralized management still matters

[Go to TOC](#table-of-contents)

## Windows and Linux Agent Considerations

Windows and Linux agents solve a similar problem, but they do not behave identically. Windows agent workflows often align closely with familiar backup and VSS concepts. Linux agent workflows require more awareness of distribution support, kernel behavior, snapshot mechanisms, and credential models.

The core administrator skill is not memorizing every distro nuance. It is understanding that agent reliability depends on the local system’s readiness.

[Go to TOC](#table-of-contents)

## Managed vs. Standalone Thinking

Agents can often be managed centrally through Veeam policies or used more independently depending on the design. Central management is powerful because it gives the backup team control and visibility. But it also means onboarding, policy scope, and connectivity become more important.

Standalone agent operations may suit isolated or small environments, but they can create visibility gaps if not documented well.

[Go to TOC](#table-of-contents)

## What You Need to Protect Successfully With Agents

Agent-based protection usually requires:

- reachability or deployment path from Veeam to the system, where central management is used
- administrative or elevated access sufficient for deployment and configuration
- compatible OS and kernel support
- enough local stability for snapshot/consistency operations
- a target repository or backup destination that aligns with recovery goals

[Go to TOC](#table-of-contents)

## Recovery Scope in Agent Environments

Agent-based backups can support more than simple file restore. Depending on the policy and platform, they can support full machine, volume, or bare-metal-style recovery patterns. That makes them extremely valuable for physical workloads.

However, bare metal recovery is only useful if recovery media and hardware driver considerations are understood ahead of time. Backup without tested recovery media is a dangerous assumption in physical environments.

[Go to TOC](#table-of-contents)

## Policy Design for Agent Estates

When many standalone systems need protection, policy consistency becomes very important. Rather than building one-off settings for every machine, a good administrator defines policy families. For example:

- branch office Windows systems with daily backup and short retention
- critical physical application servers with tighter RPO and stronger copy policy
- Linux infrastructure nodes with a focus on system-state and config recovery

This kind of policy grouping reduces drift and makes backup behavior easier to explain to stakeholders.

[Go to TOC](#table-of-contents)

## Why Agent Policies Matter

At scale, you do not want to configure every agent manually forever. Centralized policy-based management helps standardize schedules, retention, processing behavior, and repository targets. This reduces drift and improves operational control.

Still, policy-based management is only as good as your scoping and credential hygiene. If systems are added sloppily or grouped badly, policy management becomes confusing.

[Go to TOC](#table-of-contents)

## No-Hypervisor Design Principles

For no-hypervisor environments, keep these principles in mind:

- standardize backup policy by role where possible
- document recovery media and boot assumptions
- treat repository access and network reachability as first-class design inputs
- test at least one restore path per system category
- do not assume physical recovery will resemble virtual recovery in speed or convenience

[Go to TOC](#table-of-contents)

## Common Agent Failure Themes

- deployment blocked by firewall, antivirus, or policy
- credential issues during installation or policy push
- snapshot/VSS problems on Windows
- kernel or snapshot-module problems on Linux
- connectivity loss between agent and central management point

The lesson here is not that agent backups are fragile. It is that endpoint-centered protection requires endpoint-centered operational discipline.

These topics become even more important in the troubleshooting lesson.

[Go to TOC](#table-of-contents)

## v12.x Notes

As Veeam environments became more hybrid, agent-based protection grew in importance. Administrators who understand only image-based VM backup are no longer seeing the full platform. Modern Veeam operations require comfort across both hypervisor-integrated and agent-based protection models.

[Go to TOC](#table-of-contents)

## Lab Walkthrough

### Prerequisites

- one Windows system such as `PHYS-SRV01` or `WIN-APP01`
- one Linux system such as `LIN-WEB01`
- repository available for agent-targeted backups

### Steps

1. Identify one system that would be better protected through an agent than through hypervisor integration.
2. Explain why.
3. Choose one Windows and one Linux workload for future agent-based protection.
4. Define a simple policy for each: schedule, retention, destination.
5. Decide what type of restore you would need most urgently for each system: file, volume, or full machine.

### Verification

You have completed the lab if you can explain the protection and recovery model for both a Windows and Linux standalone workload.

[Go to TOC](#table-of-contents)

## Key Takeaways

- Agent-based protection is essential for physical and standalone systems.
- The no-hypervisor path is a full Veeam operating model, not an exception.
- Policy design and recovery planning matter just as much in agent environments as in VM environments.

[Go to TOC](#table-of-contents)

## Review Questions

1. When is Veeam Agent preferable to hypervisor-based backup?
2. What does agent-based protection change operationally?
3. Why are recovery media important in physical environments?
4. Why is centralized policy management useful for agents?
5. What is one Linux-specific risk in agent deployment?

---

### Answers

1. When workloads are physical, standalone, isolated, or otherwise not best protected through hypervisor integration.
2. The protected system participates directly in the backup process, increasing dependence on guest OS health and local configuration.
3. Because full machine recovery may depend on bootable media and driver support.
4. It standardizes protection and reduces configuration drift across many endpoints.
5. Kernel or snapshot-module compatibility issues.

[Go to TOC](#table-of-contents)
---

**License:** [CC BY-NC-SA 4.0](../LICENSE.md)
