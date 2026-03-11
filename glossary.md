# Glossary of Terms — Veeam Backup & Replication v12.x

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Markdown](https://img.shields.io/badge/Format-Markdown-blue)
![Course](https://img.shields.io/badge/Course-Veeam%20B%26R%20v12.x-00bcd4)

> **Scope:** Terms and acronyms used throughout the course. Entries are sorted alphabetically. Where a term is covered in depth by a specific lesson, that lesson number is noted in parentheses.

## Table of Contents

- [A](#a)
- [B](#b)
- [C](#c)
- [D](#d)
- [E](#e)
- [F](#f)
- [G](#g)
- [H](#h)
- [I](#i)
- [J](#j)
- [K](#k)
- [L](#l)
- [M](#m)
- [N](#n)
- [O](#o)
- [P](#p)
- [Q](#q)
- [R](#r)
- [S](#s)
- [T](#t)
- [U](#u)
- [V](#v)
- [W](#w)
- [X–Z](#xz)

[Go to TOC](#table-of-contents)

---

## A

**Active Full Backup** — A complete backup of all data blocks in a protected workload, performed by reading every block from the source. Unlike a synthetic full, an active full reads directly from the live source rather than constructing the full from existing backup data. It guarantees a clean restore starting point but places the heaviest load on the source and network. (Lesson 09)

**Agent Policy** — A configuration object in Veeam Backup & Replication that governs how the Veeam Agent behaves on one or more managed machines: what data to protect, which repository to use, what schedule to follow, and how retention is applied. Policies are distributed to agents automatically when the agents are connected to a managed protection group. (Lesson 13, 14)

**Alarm** — A configured notification trigger in Veeam ONE or the VBR console that fires when a condition such as a failed job, low repository space, or missed SLA is detected. Alarms can be routed to email, SNMP, or ticketing systems. (Lesson 26)

**Application-Aware Processing (AAP)** — A set of capabilities in Veeam that quiesce application state before a backup snapshot is taken and optionally truncate transaction logs after the backup completes. AAP uses VSS on Windows and script hooks on Linux to produce application-consistent restore points rather than crash-consistent ones. It is required for reliable recovery of exchange, SQL Server, SharePoint, Active Directory, and Oracle workloads. (Lesson 12)

**Application-Consistent Backup** — A backup taken after the application has flushed its in-flight transactions and committed them to disk, so that the restored workload can start cleanly without needing crash recovery. Contrast with crash-consistent backup. (Lesson 12)

**Application Item Restore** — Recovery of individual objects from inside an application, such as a single mailbox, email, database, SharePoint document, or Active Directory object, without restoring the entire virtual machine or volume. Performed using the Veeam Explorers. (Lesson 18)

**Archive Extent** — The third tier in a Scale-Out Backup Repository hierarchy. Archive extents connect to object storage with a very long or unlimited retention policy and are used for regulatory archival, compliance retention, or deep cold storage. Data in the archive tier is not typically accessible for immediate restore without a retrieval step. (Lesson 07, 23)

**Archive Tier** — See Archive Extent. In the context of object storage integration, the archive tier is the lowest-cost, highest-latency storage layer. (Lesson 23)

[Go to TOC](#table-of-contents)

---

## B

**Backup** — A point-in-time copy of data stored in a format that can be used to restore the original workload to its state at the time of the copy. In Veeam, backup files use the .vbk (full) and .vib or .vrb (incremental) formats. (Lesson 02)

**Backup Console** — The Veeam Backup & Replication management user interface, installed on the backup server. Used for configuring jobs, monitoring activity, initiating restores, and managing infrastructure. (Lesson 03)

**Backup Copy Job** — A job type that moves existing backup data from one repository to another, typically to satisfy offsite or 3-2-1 requirements. Backup copy jobs are independent of the original backup job and maintain their own GFS retention schedule. They do not re-read from the source workload. (Lesson 21)

**Backup File** — The on-disk artifact produced by a Veeam backup job. Full backup files use the .vbk extension. Incremental backup files use .vib (forward incremental) or .vrb (reverse incremental). Metadata files use .vbm. (Lesson 09)

**Backup Infrastructure** — The collective set of components managed by Veeam: backup server, proxies, repositories, tape servers, WAN accelerators, and the managed machines being protected. (Lesson 03)

**Backup Job** — A configured task that runs on a schedule to protect one or more workloads, producing restore points stored in a repository. A backup job defines the source objects, destination repository, processing options, schedule, and retention policy. (Lesson 09)

**Backup Proxy** — A Veeam component responsible for retrieving data from a source workload, processing it (compression, deduplication, encryption), and sending it to a repository. The proxy offloads data movement work from the backup server. One or more proxies can be added and load-balanced across jobs. (Lesson 11)

**Backup Repository** — A storage location where Veeam stores backup files, metadata, and restore points. Repositories can be local Windows or Linux directories, SMB/NFS shares, deduplication appliances, object storage buckets, or Scale-Out Backup Repositories. (Lesson 07)

**Backup Server** — The central management component of a Veeam deployment. It runs the Veeam Backup Service, hosts the configuration database, orchestrates all jobs, and provides the management console. All other components communicate with or are managed by the backup server. (Lesson 03)

**Backup Window** — The time period during which backup jobs are permitted or expected to run. Backup windows are typically defined to avoid peak production hours. Veeam jobs can be scheduled to stop at the end of a backup window and resume at the next window opening. (Lesson 09)

**Block Cloning** — A storage-accelerated operation available on ReFS (Windows) and XFS (Linux) volumes that allows backup files to be synthesized without physically copying blocks, dramatically reducing CPU and I/O overhead for synthetic full creation. (Lesson 07)

**Bootable Media** — Recovery media, such as a USB drive or ISO, built with Veeam Recovery Media Builder, used to perform a bare-metal restore of a physical machine or to recover a system in cases where the operating system is unbootable. (Lesson 13)

[Go to TOC](#table-of-contents)

---

## C

**Capacity Tier** — The second tier of a Scale-Out Backup Repository. It offloads backup data from the performance tier to cost-effective object storage after a configurable period. Restore operations can read from the capacity tier without full retrieval. (Lesson 07, 23)

**CBT (Change Block Tracking)** — A VMware vSphere feature that records which disk blocks have changed since the last backup snapshot. Veeam uses CBT to transfer only modified blocks during incremental backups, greatly reducing backup time and data transferred. If CBT becomes corrupt, it must be reset and a new active full taken. (Lesson 09, 11)

**Chain** — The sequence of backup files that together describe the full state of a workload at a given restore point. A chain always begins with a full backup (.vbk) and may include one or more incremental files. To restore from a given point, all files in the chain up to that point must be intact. (Lesson 09)

**Cloud Connect** — A Veeam capability that allows end-user Veeam deployments to send backup data to a service provider's repository over the internet without requiring a VPN. The service provider runs a Cloud Gateway and exposes tenant-specific storage. (Lesson 23)

**Configuration Backup** — A scheduled export of the Veeam Backup & Replication configuration database to a backup file (.bcf). It enables full server recovery after a disaster or rebuild. It should be stored offsite or on a separate repository. (Lesson 03, 24)

**Configuration Database** — The SQL Server (or PostgreSQL in later v12.x releases) database that stores all Veeam job definitions, infrastructure records, credentials, schedules, retention settings, and restore point metadata. If this database is lost and there is no configuration backup, all job definitions and metadata are lost even if the backup files on disk are intact. (Lesson 03)

**Crash-Consistent Backup** — A backup taken by snapshotting the virtual machine disk at an arbitrary moment without asking the application to flush its state first. The resulting restore point may require crash recovery (log replay) when the workload is powered on. Contrast with application-consistent backup. (Lesson 12)

**Credential** — A stored username and password or certificate used by Veeam to authenticate against managed infrastructure such as vCenter, Hyper-V hosts, repositories, and protected machines. Credentials are stored in the Veeam credentials manager and should be treated with the same sensitivity as privileged accounts. (Lesson 04, 24)

[Go to TOC](#table-of-contents)

---

## D

**Data Sovereignty** — A compliance and governance requirement that certain data must reside within a defined geographic or legal jurisdiction. Relevant when using cloud or object storage tiers that span multiple regions. (Lesson 23)

**Deduplication** — The process of identifying and eliminating duplicate data blocks within backup files or across a repository, storing repeated blocks only once and referencing them by pointer. Veeam performs inline per-job deduplication. Deduplication appliances such as ExaGrid, HPE StoreOnce, or Dell EMC Data Domain can extend this further at the repository level. (Lesson 07)

**Deduplication Appliance** — A purpose-built storage device that provides hardware or software-accelerated deduplication. Veeam integrates with several deduplication appliances using proprietary APIs to improve throughput and efficiency. (Lesson 07)

**Direct NFS Access** — A transport mode in which the Veeam proxy communicates directly with an NFS datastore on a VMware environment without routing through the ESXi host. Reduces load on the ESXi kernel but requires the proxy to be on the same network as the NFS storage. (Lesson 11)

**Direct SAN Access** — A transport mode in which the Veeam proxy reads VM data directly from a SAN (Fibre Channel or iSCSI) LUN, bypassing the ESXi host entirely. Produces the fastest backup performance and zero impact on the ESXi kernel but requires the proxy to have SAN connectivity. (Lesson 11)

**Disaster Recovery (DR)** — The set of processes, infrastructure, and plans used to restore normal operations after a failure that affects the primary site or primary workloads. In Veeam, DR typically involves replication jobs, failover plans, and tested failover procedures. (Lesson 19)

**DR Site** — The secondary location where replicated VMs or backup copies reside and where recovery operations are executed during a disaster. Also called the recovery site. (Lesson 19)

[Go to TOC](#table-of-contents)

---

## E

**Encryption** — The transformation of backup data into an unreadable form using a cryptographic key, so that the data cannot be read if the backup media or storage is accessed by an unauthorized party. Veeam supports encryption at the job level (AES-256), in transit, and for tapes. Encryption keys must be stored and protected separately from the backup data. (Lesson 24)

**Enterprise Manager** — A web-based, multi-server management and reporting component for Veeam that aggregates visibility across multiple VBR servers, supports delegated administration, provides self-service file restore for end users, and enables centralized license management. (Lesson 25)

**ESXi** — VMware's bare-metal hypervisor product that runs directly on server hardware and hosts virtual machines. In Veeam, ESXi hosts are added as managed infrastructure and their VMs are protected via the vSphere API using VADP. (Lesson 01, 06)

**Extent** — An individual storage unit within a Scale-Out Backup Repository. A SOBR can contain multiple extents. Veeam uses a placement policy to distribute backup data across extents. Extents can be local, network, hardened Linux, or object storage targets. (Lesson 07)

[Go to TOC](#table-of-contents)

---

## F

**Failback** — The process of returning production workloads from the DR site to the original primary site after a failover event. Failback involves synchronizing any writes that occurred on the failover VM back to the original primary VM or creating a new replica. (Lesson 19)

**Failover** — The process of activating replicated VMs at a DR site in response to a failure or test. Planned failover is an intentional graceful switch (e.g., for maintenance). Unplanned failover is an emergency activation in response to a disaster. (Lesson 19)

**Failover Plan** — A pre-defined, ordered sequence of VM failover steps stored in Veeam. A failover plan can include boot sequencing, delays between groups, and recovery scripts, so that dependent services come up in the correct order. (Lesson 19)

**Fast Clone** — See Block Cloning.

**Forever-Forward Incremental** — A backup chain structure where an initial full backup is followed by an unending series of incremental files. There are no subsequent scheduled full backups. The retention mechanism removes the oldest incremental by merging it into the full. This method minimizes daily data transfer and storage growth. (Lesson 09)

**Full Backup** — A backup containing all data blocks for the protected workload at the time of the backup, without dependency on any other backup file. A full backup forms the base of every backup chain. (Lesson 02, 09)

[Go to TOC](#table-of-contents)

---

## G

**GFS (Grandfather-Father-Son)** — A long-term retention scheme that preserves specific backup restore points on a weekly, monthly, and yearly schedule, independently of the regular short-term retention. GFS is commonly required for compliance and regulatory purposes. In Veeam, GFS can be applied to backup copy jobs and tape jobs. (Lesson 21, 22)

**Guest Interaction Proxy (GIP)** — A Veeam component deployed inside the production network that communicates with the guest OS of a protected VM to perform application-aware processing, log truncation, pre- and post-job scripts, and file indexing. The GIP connects to the VM over the network rather than through the VMware tools channel. (Lesson 12)

**Guest OS Processing** — See Application-Aware Processing. Also refers to any in-guest operation performed during backup, such as file indexing, pre-freeze scripts, and log truncation. (Lesson 12)

[Go to TOC](#table-of-contents)

---

## H

**Hardened Linux Repository** — A Veeam repository running on a minimal, locked-down Linux system configured to accept backup writes but deny modification or deletion of existing backup files. The hardened repository implements single-use credentials (so Veeam cannot re-authenticate to delete files), immutability at the file system level, and optional XFS block cloning. It is the recommended on-premises solution for ransomware-resilient backup storage. (Lesson 07, 24)

**Health Check** — A periodic verification run against stored backup files to detect data corruption at the block level. Veeam performs health checks using CRC and hash validation. If corruption is detected, Veeam can automatically trigger a new backup to repair the chain. (Lesson 09)

**Hot Add** — A transport mode for VMware environments where a backup proxy VM is running on the same ESXi host or storage fabric as the protected VM. The proxy mounts the VM's VMDK directly via the storage layer, allowing high-speed reads without LAN overhead. Also called Virtual Appliance mode. (Lesson 11)

**Hyper-V** — Microsoft's hypervisor platform, available as a Windows Server role or as the free Hyper-V Server edition. Veeam protects Hyper-V VMs using Microsoft's Resilient Change Tracking (RCT) API rather than VMware's VADP/CBT. (Lesson 01, 06)

[Go to TOC](#table-of-contents)

---

## I

**Immutability** — The property of a backup file that prevents it from being modified or deleted for a defined retention period, regardless of OS-level credentials or ransomware activity. Veeam supports immutability on hardened Linux repositories (using chattr +i), on S3-compatible object storage (using S3 Object Lock), and on some deduplication appliances. (Lesson 07, 23, 24)

**Incremental Backup** — A backup containing only the data blocks that changed since the previous backup, whether that previous backup was a full or another incremental. Incremental backups are much smaller and faster than full backups but require the entire chain to be intact for a restore. (Lesson 02, 09)

**Instant VM Recovery (IVR)** — A Veeam technology that starts a VM directly from the backup file in the repository, without waiting for a full restore to complete. The VM runs from the repository storage, and any writes are redirected to a change log. IVR allows recovery in minutes. A subsequent storage vMotion or Quick Migration moves the VM to production storage. (Lesson 16, 17)

**Instant Recovery** — The broader term covering Instant VM Recovery and similar rapid-start capabilities for physical machines, NAS data, and application servers. Veeam extends instant recovery to non-VM workloads in later v12.x releases. (Lesson 16)

**Item-Level Restore (ILR)** — Recovery of a single item from inside a backup, such as a file, folder, email, database record, or Active Directory object. Item-level restores avoid restoring an entire VM when only specific data is needed. (Lesson 16, 18)

[Go to TOC](#table-of-contents)

---

## J

**Job** — Any configured task in Veeam: backup, backup copy, replication, tape, NAS, agent, or restore verification. Every job has a source, destination, schedule, and retention policy. (Lesson 09)

**Job Chaining** — Configuring one Veeam job to start automatically after another job completes. Commonly used to ensure a backup copy or tape job runs only after the primary backup job finishes. (Lesson 09)

[Go to TOC](#table-of-contents)

---

## K

**Kasten K10** — A Veeam-owned Kubernetes-native data protection platform for container workloads, separate from the core VBR product. Mentioned in the course context for completeness when discussing the Veeam product portfolio. (Lesson 01)

[Go to TOC](#table-of-contents)

---

## L

**LAN Mode (Network Mode)** — A transport mode in which the backup proxy reads VM data from the ESXi host via the VMware NBD (Network Block Device) protocol over the standard TCP/IP network. This is the fallback transport mode and requires no special storage connectivity, but it consumes production network bandwidth. (Lesson 11)

**License** — The entitlement that governs how many instances (sockets, VMs, or agents) Veeam will protect. VBR licenses are issued per managed instance. Community edition provides limited free protection for a small number of workloads. License types include perpetual, rental, and cloud subscription models. (Lesson 01)

**Log Truncation** — The post-backup deletion of committed transaction log files from an application server, triggered by Veeam after a successful application-aware backup. Log truncation prevents transaction log volumes from filling up. It is performed by the VSS infrastructure on Windows or via script on Linux. It should be disabled if a DBA manages log backups independently. (Lesson 12)

[Go to TOC](#table-of-contents)

---

## M

**Malware-Aware Recovery** — A set of Veeam features in v12.1+ that integrate with threat intelligence (YARA rules, antivirus scanning) to identify infected restore points and select a clean restore point during recovery. The goal is to avoid restoring ransomware along with the data. (Lesson 24)

**Media Pool** — A logical grouping of tape cartridges in a tape library, managed by Veeam to control which tapes are used for specific jobs, GFS sets, or archival destinations. (Lesson 22)

**Mount Server** — A Veeam component that mounts backup file contents as a local drive to enable file-level restore, item-level restore, and certain verification operations. It is automatically deployed alongside repositories and can be a dedicated server in larger environments. (Lesson 03, 16)

**Multi-Factor Authentication (MFA)** — An authentication requirement in which a user must provide two or more verification factors. Veeam supports MFA for console login starting in v12 as part of its security hardening posture. (Lesson 24)

[Go to TOC](#table-of-contents)

---

## N

**NAS Backup** — A Veeam job type designed to protect file shares exposed via SMB or NFS. NAS backup uses file-change tracking (FCT) for incremental passes and stores versions in a file-based backup format separate from the VM backup format. (Lesson 15)

**NBD (Network Block Device)** — The VMware protocol used in LAN transport mode to stream VM disk data from an ESXi host to a backup proxy over TCP/IP. Slower than SAN or Hot Add transport but universally compatible. (Lesson 11)

**NDMP (Network Data Management Protocol)** — A standard protocol for moving data between network-attached storage devices and backup systems. Veeam supports NDMP for backing up data on NAS filers that expose an NDMP interface. (Lesson 22)

**Network (NBD) Mode** — See LAN Mode.

[Go to TOC](#table-of-contents)

---

## O

**Object Storage** — Storage accessed via an HTTP API (S3-compatible or Azure Blob-compatible) rather than a file system or block device. Object storage is cost-effective for large-volume backup data. Veeam uses it for capacity tier, archive tier, and immutable cloud backup. Examples: AWS S3, Azure Blob, Wasabi, MinIO. (Lesson 23)

**Object Storage Repository** — A Veeam repository type pointing to an S3-compatible or Azure Blob endpoint. Object storage repositories can be used directly as backup targets (for cloud backups or Veeam Agent backups) or as extents within a SOBR. (Lesson 23)

**Offload Policy** — A SOBR setting that defines when backup data is automatically moved or copied from the performance tier to the capacity tier in object storage. Can be based on time elapsed or when backup files are no longer needed by local retention. (Lesson 07, 23)

[Go to TOC](#table-of-contents)

---

## P

**Performance Tier** — The primary, fastest tier of a Scale-Out Backup Repository. It consists of local or network-attached extents and stores recent restore points for fast backup and restore operations. (Lesson 07)

**Physical Server Protection** — See Veeam Agent.

**Planned Failover** — A graceful switchover to replicated VMs at the DR site, performed with the source VMs powered off and the replica fully synchronized. Used for maintenance, site migrations, and DR drills. Contrast with unplanned failover. (Lesson 19)

**Protection Group** — A Veeam construct that discovers and organizes physical machines, cloud instances, or unmanaged systems to which Veeam Agents are deployed or applied via policy. Protection groups can be defined by IP range, Active Directory OU, CSV list, or cloud connector. (Lesson 13)

**Proxy** — See Backup Proxy.

[Go to TOC](#table-of-contents)

---

## Q

**Quiescence** — The state in which an application has suspended writes and flushed all in-flight transactions to disk, making the data consistent for a point-in-time snapshot. Quiescence is triggered by VSS on Windows and by pre-freeze scripts or VMware Tools on Linux. (Lesson 12)

[Go to TOC](#table-of-contents)

---

## R

**RBAC (Role-Based Access Control)** — A security model in which permissions are assigned to roles rather than individual users, and users are assigned to roles. Veeam Enterprise Manager and VBR both support RBAC to limit what administrators, operators, and restore operators can see and do. (Lesson 25)

**RCT (Resilient Change Tracking)** — The Microsoft Hyper-V equivalent of VMware CBT. RCT tracks which VM disk blocks have changed since the last backup checkpoint, enabling efficient incremental backups on Hyper-V without re-reading the entire virtual disk. (Lesson 09, 11)

**Recovery Point** — See Restore Point.

**Recovery Point Objective (RPO)** — The maximum acceptable amount of data loss expressed as a unit of time. An RPO of 4 hours means the business can tolerate losing up to 4 hours of changes. RPO determines how frequently backups must run. (Lesson 02)

**Recovery Time Objective (RTO)** — The maximum acceptable time between a failure event and the restoration of full service. An RTO of 2 hours means the system must be fully functional again within 2 hours of a failure. RTO determines which recovery method (e.g., Instant VM Recovery versus full restore) is appropriate. (Lesson 02)

**ReFS (Resilient File System)** — A Windows file system that supports block cloning, enabling Veeam to synthesize full backups and create backup copy files without physically copying data blocks. ReFS volumes are strongly recommended for Windows-based Veeam repositories when synthetic full operations are frequent. (Lesson 07)

**Replica** — A powered-off copy of a virtual machine maintained at the DR site, kept synchronized with the production VM through periodic replication jobs. A replica can be powered on during failover in seconds. (Lesson 19)

**Replication Job** — A Veeam job that reads from a source VM or from a backup file and writes incremental changes to a replica VM at the target (DR) site. (Lesson 19)

**Repository** — See Backup Repository.

**Restore Point** — A single point in time from which a protected workload can be restored. Each time a backup job runs successfully, it creates a new restore point. The number of restore points retained is governed by the retention policy. (Lesson 09)

**Retention Policy** — The rule that defines how many restore points, or how many days of restore points, are kept in a repository before older ones are deleted or merged. Short-term retention controls day-to-day restore points; GFS controls long-term archival copies. (Lesson 09)

**Reverse Incremental** — A backup chain structure where the most recent backup is always stored as a full copy, and older restore points are reconstructed by working backward through incremental difference files called rollback files (.vrb). The newest restore point is always the fastest to restore from. (Lesson 09)

**RPO** — See Recovery Point Objective.

**RTO** — See Recovery Time Objective.

[Go to TOC](#table-of-contents)

---

## S

**Scale-Out Backup Repository (SOBR)** — A Veeam repository abstraction layer that groups multiple individual storage extents into a single logical target. VBR manages placement, load balancing, and data lifecycle (offload to capacity tier, archive tier) across the extents automatically. A SOBR can combine local disks, network shares, hardened Linux nodes, and object storage. (Lesson 07)

**Secure Restore** — A Veeam restore option that runs antivirus scanning against restored files or VM images before publishing them to production, to detect malware before it can spread. (Lesson 16, 24)

**Self-Service File Restore** — A capability in Veeam Enterprise Manager that allows end users to recover their own files from a backup without administrator involvement, through a web portal. (Lesson 25)

**S3 Object Lock** — An S3-compatible API feature that enforces WORM (write-once-read-many) policy on object storage buckets. When Veeam uses a bucket with S3 Object Lock enabled, backup objects become immutable for the configured lock period. (Lesson 23, 24)

**SMTP** — Simple Mail Transfer Protocol. Used by Veeam to send email notifications for job results, alarms, and report delivery. (Lesson 26)

**SOBR** — See Scale-Out Backup Repository.

**SLA (Service Level Agreement)** — A formal commitment that defines the expected level of service for backup or recovery. In Veeam ONE, SLA compliance is tracked and reported based on job success rates, RPO adherence, and restore readiness. (Lesson 26)

**SMB (Server Message Block)** — A Windows file sharing protocol. Veeam can use SMB shares as backup repositories and as NAS backup sources. (Lesson 07, 15)

**Snapshot** — A point-in-time frozen image of a virtual machine's disk state, created by the hypervisor (VMware or Hyper-V) during backup to allow the backup proxy to read a consistent copy of the data while the VM continues running. Snapshots are temporary and are removed after the backup data is transferred. Stale or delta-bloated snapshots are a common source of VMware backup problems. (Lesson 09, 27)

**Snapshot Consolidation** — The VMware process of collapsing snapshot delta files back into the base VMDK after a snapshot is deleted. If consolidation fails or is blocked, the VM can accumulate snapshot delta chains that degrade performance and consume storage. Veeam identifies and alerts on orphaned snapshot states. (Lesson 27)

**Standalone Mode (Agent)** — A Veeam Agent deployment model in which the agent is installed manually and operated independently, without a central VBR server managing it. Useful for workstations, remote machines, and environments where central management is not available. (Lesson 13)

**Support Bundle** — A package of diagnostic files generated by Veeam (logs, configuration exports, event records) submitted to Veeam Support for case investigation. (Lesson 27)

**Synthetic Full Backup** — A full backup file constructed by Veeam using the existing full backup plus accumulated incremental files, without reading from the source VM again. Synthetic fulls reset the incremental chain and improve restore performance. On ReFS or XFS, Veeam uses block cloning to synthesize fulls with near-zero disk I/O. (Lesson 09)

[Go to TOC](#table-of-contents)

---

## T

**Tape Job** — A Veeam job type that reads from a backup repository and writes data to tape cartridges. Tape jobs can apply GFS retention and are used for archival, compliance, or air-gapped offsite copies. (Lesson 22)

**Tape Library** — A physical robotic tape storage system containing one or more tape drives and a collection of tape cartridges. VBR controls the library via a tape server. (Lesson 22)

**Tape Server** — A Veeam component that communicates with tape drives and tape libraries. The tape server manages cartridge inventory, mount/dismount operations, and data streaming to/from tape. (Lesson 22)

**Task** — A single unit of work within a Veeam job, typically corresponding to one protected VM or agent machine. A job processes multiple tasks, and task concurrency is governed by the available proxy and repository slot counts. (Lesson 11)

**Thin Provisioning** — A storage allocation model in which only the disk space actually consumed by data is reserved, rather than the full declared disk size. Relevant during restore when Veeam can restore disks as thin-provisioned to a target datastore that supports it. (Lesson 16)

**3-2-1 Rule** — A widely recommended backup strategy: keep at least **3** copies of data, on at least **2** different storage types, with at least **1** copy stored offsite. Veeam's backup copy jobs and cloud integration are designed to make 3-2-1 compliance straightforward. (Lesson 02)

**3-2-1-1-0 Rule** — An extended version of the 3-2-1 rule: 3 copies, 2 media types, 1 offsite, **1** immutable or air-gapped copy, **0** errors verified by automated restore testing. Increasingly adopted as ransomware defense guidance. (Lesson 02, 24)

**Transaction Log** — A database file that records every transaction made against a database before those changes are written permanently to the data files. Transaction logs must be managed and backed up as part of a complete database protection strategy. Veeam can truncate transaction logs after a successful application-aware backup. (Lesson 12)

**Transport Mode** — The method by which a Veeam backup proxy retrieves data from a protected VM. The main modes are Direct SAN Access, Hot Add (Virtual Appliance), NBD (LAN), and Direct NFS Access. Veeam automatically selects the most efficient available mode. (Lesson 11)

[Go to TOC](#table-of-contents)

---

## U

**Unplanned Failover** — An emergency activation of replica VMs at the DR site in response to an outage at the primary site. Unlike planned failover, the source VMs may still be running or corrupted. Requires careful sequencing to avoid split-brain and data conflicts during failback. (Lesson 19)

**Update (v12.x)** — A maintenance release of Veeam Backup & Replication v12 (e.g., v12.1, v12.2, v12.3) that may include new platform support, bug fixes, security patches, and feature additions. Always review release notes before updating a production environment. (Lesson 01)

[Go to TOC](#table-of-contents)

---

## V

**VADP (vSphere APIs for Data Protection)** — The VMware API framework that Veeam uses to create and delete snapshots, enumerate changed blocks via CBT, and transfer VM disk data in VMware vSphere environments. VADP is the foundation of all VMware-based Veeam backup and replication operations. (Lesson 11)

**VBR** — See Veeam Backup & Replication.

**Veeam Agent for Linux** — A standalone agent installed on Linux physical or virtual machines to protect them with file-level or volume-level or entire-machine backups, independently of the hypervisor. Managed from VBR via protection groups and agent policies. (Lesson 13)

**Veeam Agent for Windows** — A standalone agent installed on Windows physical or virtual machines to protect them with file-level, volume-level, or entire-machine backups, independently of the hypervisor. Supports workstation, server, and standalone deployment modes. (Lesson 13)

**Veeam Backup & Replication (VBR)** — The core product covered in this course. An enterprise data protection platform that backs up, replicates, and recovers virtual, physical, NAS, cloud, and containerized workloads. (Lesson 01)

**Veeam Explorer for Active Directory** — A Veeam tool that mounts a backup of a domain controller and allows recovery of individual AD objects, OUs, group policies, passwords, and attributes without restoring the entire DC. (Lesson 18)

**Veeam Explorer for Exchange** — A Veeam tool that opens a backup of a Microsoft Exchange server and allows recovery of individual mailboxes, folders, emails, contacts, and calendar items. (Lesson 18)

**Veeam Explorer for Oracle** — A Veeam tool that mounts and presents Oracle database backups, enabling tablespace and object-level recovery. (Lesson 18)

**Veeam Explorer for PostgreSQL** — A Veeam tool for item-level recovery from PostgreSQL database backups. Introduced in later v12.x releases. (Lesson 18)

**Veeam Explorer for SharePoint** — A Veeam tool that opens SharePoint farm backups and allows recovery of individual sites, libraries, lists, documents, and items. (Lesson 18)

**Veeam Explorer for SQL Server** — A Veeam tool that opens SQL Server database backups and allows recovery of individual databases, tables, and SQL objects to a target SQL instance. (Lesson 18)

**Veeam ONE** — A separate Veeam product for monitoring, reporting, and capacity planning. It connects to VBR, vCenter, and Hyper-V to provide dashboards, alarms, SLA reports, and predictive analytics. (Lesson 26)

**VeeamZIP** — An ad-hoc, single-run full backup operation that creates a self-contained backup file from a VM, without configuring a formal job. Useful for creating a point-in-time snapshot before maintenance or migration. (Lesson 09)

**vCenter Server** — The VMware management server that centralizes control of ESXi hosts and their VMs. Veeam adds vCenter as a managed infrastructure object, after which all VMs on all managed ESXi hosts become available for protection. (Lesson 06)

**Virtual Appliance Mode** — See Hot Add.

**VMCA (Veeam Certified Architect)** — An advanced Veeam certification for architects who design and validate complex Veeam environments. Above the VMCE level. (Lesson 28 / exam)

**VMCE (Veeam Certified Engineer)** — The primary Veeam professional certification, validating knowledge of VBR deployment, configuration, management, and troubleshooting. This course is aligned to VMCE-level knowledge. (Lesson 01, 28)

**VMDK (Virtual Machine Disk)** — The VMware disk format used to store a virtual machine's data. Veeam reads VMDK files during backup via VADP. (Lesson 03)

**VHD / VHDX (Virtual Hard Disk)** — The Hyper-V disk format equivalent to VMware's VMDK. Veeam reads VHD/VHDX files via the Hyper-V integration API. (Lesson 03)

**Volume Shadow Copy Service (VSS)** — A Windows framework that coordinates the creation of consistent snapshots of volumes across applications and the file system. Veeam uses VSS to request application quiescence during backup of Windows workloads. VSS providers, requestors, and writers all participate in the VSS process, and failures at any point can interrupt application-aware backups. (Lesson 12)

**vSphere** — The VMware product suite for server virtualization, encompassing ESXi (the hypervisor), vCenter Server (the management platform), and associated storage, networking, and management components. (Lesson 01)

[Go to TOC](#table-of-contents)

---

## W

**WAN Accelerator** — A Veeam component that reduces the bandwidth consumed by backup copy jobs sent over slow WAN links by applying global data deduplication and compression across the data stream. Requires a WAN accelerator at both the source and target sites. Relevant for backup copy to remote or branch sites. (Lesson 21)

**Windows Hardened Repository** — A Windows-based backup repository with restricted permissions. Less common than a hardened Linux repository, but achievable by removing Veeam's ability to delete files after backup. (Lesson 07)

**WORM (Write Once Read Many)** — A data storage property that prevents written data from being altered or deleted. Implemented via hardware (tape), file system attributes (Linux chattr +i), or object storage policies (S3 Object Lock). WORM is a key mechanism for achieving backup immutability. (Lesson 24)

[Go to TOC](#table-of-contents)

---

## X–Z

**XFS** — A high-performance Linux file system that supports fast clone (reflink) operations, enabling efficient synthetic full backup creation on Linux-based Veeam repositories. Recommended over ext4 for hardened and high-volume Linux repositories. (Lesson 07)

**YARA Rules** — Pattern-matching rules used in malware detection and threat intelligence. Veeam integrates with YARA-based scanning in its malware-aware recovery workflow in v12.1+ to flag restore points that contain known malware signatures before restoring them to production. (Lesson 24)

[Go to TOC](#table-of-contents)

---

**License:** [CC BY-NC-SA 4.0](LICENSE.md)
