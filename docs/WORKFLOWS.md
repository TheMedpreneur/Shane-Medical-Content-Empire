# GitHub Actions Workflows Guide

This document provides an overview of all GitHub Actions workflows in the Shane Medical Content Empire project.

## Workflow Overview

| Workflow | Trigger | Purpose | Artifacts |
|----------|---------|---------|-----------|
| Daily Backup | Schedule (2 AM UTC) / Manual | Back up UE5 project and content | Backup archives (30 days) |
| Content Validation | Push/PR to main/develop | Validate medical content | Validation reports (90 days) |
| Deployment | Push to main / Tags / Manual | Build cross-platform releases | Platform packages |
| Security Audit | Weekly (Mon 9 AM) / Push/PR | Security and compliance scanning | Security reports (365 days) |

## 1. Daily Backup Workflow

**File:** `.github/workflows/daily-backup.yml`

### Trigger
- **Schedule:** Daily at 2:00 AM UTC
- **Manual:** Via workflow_dispatch

### What It Does
1. Checks out repository with full Git history and LFS
2. Creates compressed archives of UE5 project, templates, and scripts
3. Generates backup manifest with metadata
4. Uploads to GitHub Actions artifacts (30-day retention)
5. Optionally uploads to S3 for long-term storage

### Required Secrets (Optional)
- `AWS_ACCESS_KEY_ID` - For S3 backups
- `AWS_SECRET_ACCESS_KEY` - For S3 backups
- `S3_BACKUP_BUCKET` - S3 bucket name

## 2. Content Validation Workflow

**File:** `.github/workflows/content-validation.yml`

### Trigger
- **Push:** To main or develop branches
- **Pull Request:** To main or develop branches
- **Manual:** Via workflow_dispatch

### What It Does
1. Medical accuracy checking with schema validation
2. Medical terminology verification
3. Educational standards validation
4. Citation compliance checking
5. Accessibility compliance
6. HIPAA compliance validation

## 3. Deployment Workflow

**File:** `.github/workflows/deployment.yml`

### Trigger
- **Push:** To main branch
- **Tags:** Version tags (v*.*.*)
- **Manual:** Via workflow_dispatch

### What It Does
1. Builds for Windows, Linux, and macOS
2. Creates GitHub releases for version tags
3. Deploys to staging/production environments

## 4. Security Audit Workflow

**File:** `.github/workflows/security-audit.yml`

### Trigger
- **Schedule:** Weekly on Mondays at 9:00 AM UTC
- **Push:** To main or develop branches
- **Manual:** Via workflow_dispatch

### What It Does
1. Dependency security scanning
2. CodeQL code analysis
3. HIPAA, FDA CFR 11, and GDPR compliance audits
4. License compliance checks
5. Security scorecard generation

---

*For detailed information, see individual workflow files in `.github/workflows/`*
