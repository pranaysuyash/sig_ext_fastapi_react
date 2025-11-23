# Backup folder

This folder stores local backups created during sync and deploy operations for the landing pages.

Purpose:

- Preserve copies of manually-synced files before changes are propagated to `web/live`.
- Keep `web/live` clean for deployment while retaining copies for rollbacks or audits.

Naming convention:

- Backups are organized under subfolders named `landing-page-sync-YYYYMMDD`.

Note:

- Files in this folder are intentionally not tracked by git. See `.gitignore` at the repository root.
- If you need to apply changes in a backup, copy the files from this folder into `web/live`, validate locally, and commit to the `landing-page` branch.
