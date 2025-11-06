# CloudGoat-GCP  
_A Cloud-Native Security Lab for Google Cloud Platform_

---

## 🌩️ Overview

**CloudGoat-GCP** is a hands-on, intentionally vulnerable lab environment inspired by the original [CloudGoat](https://github.com/RhinoSecurityLabs/cloudgoat), but rebuilt for **Google Cloud Platform (GCP)**.

It is designed for **cybersecurity learning, red-team/blue-team training, and academic demonstration**, focusing on **GCP-native misconfigurations** and realistic attack paths.

This repository currently contains the **infrastructure skeleton and documentation**.  
Future updates will include:
- Fully implemented challenges (6 planned, all GCP-native)
- Modern web UI (React + Tailwind)
- Terraform + GKE-based cloud deployment
- Automated CI/CD workflows

---

## 🎯 Project Goals

1. Recreate CloudGoat-style scenarios using **GCP services** (GKE, IAM, GCS, Cloud Functions, etc.)
2. Teach **GCP security concepts** through exploitation and remediation exercises.
3. Use **Infrastructure as Code (Terraform)** for reproducibility.
4. Provide a **modern, engaging interface** for learners and graders.
5. Maintain **clear documentation** and **ethical isolation** for safe testing.

---

## 🧩 Roadmap

| Phase | Focus | Status |
|-------|--------|--------|
| **1. Repo Skeleton & Docs** | Create structure, base docs, workflow | ✅ Done |
| **2. Challenge Development** | Add 6 high-quality GCP-native challenges | 🟨 Pending |
| **3. UI Development** | React portal for challenge management & leaderboard | ⏳ Pending |
| **4. GCP Deployment** | Terraform + GKE automation | ⏳ Pending |
| **5. Domain Integration** | Custom DNS (A record) + HTTPS setup | ⏳ Pending |

---

## 🏗️ Repository Structure

```bash
cloudgoat-gcp/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── MAINTAINERS.md
│
├── terraform/               # Terraform configs for GCP infra
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
│
├── k8s/                     # Kubernetes manifests & overlays
│   ├── README.md
│   └── overlays/
│
├── portal/                  # React + Node scaffold (UI)
│   ├── README.md
│   └── scaffold/
│
├── challenges/              # Challenge templates & final code
│   ├── templates/
│   └── README.md
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── GRADING_RUBRIC.md
│
├── scripts/                 # Deployment utilities
│   ├── deploy.sh
│   └── teardown.sh
│
└── .github/
    ├── ISSUE_TEMPLATE.md
    └── workflows/
        └── ci.yml
