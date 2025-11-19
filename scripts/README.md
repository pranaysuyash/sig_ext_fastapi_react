# Scripts Directory

This directory contains various scripts for development, testing, and utilities.

## Structure

- **debug/** - Debugging scripts for troubleshooting issues
- **test/** - Test scripts for validating functionality
- **util/** - Utility scripts for development tasks

## Debug Scripts

- `debug_session_issue.py` - Debug session-related issues
- `debug_results_pane.py` - Debug results pane functionality
- `debug_result_pane_issue.py` - Debug result pane specific issues
- `debug_layout_issue.py` - Debug layout-related problems

## Test Scripts

- `test_modern_mac_button.py` - Test macOS button styling
- `test_result_pane.py` - Test results pane functionality
- `test_upload_debug.py` - Test upload functionality with debugging
- `test_fix_verification.py` - Test fix verification
- `test_layout_issue.py` - Test layout-related functionality

## Utility Scripts

- `create_demo_pdf.py` - Create demo PDF files for testing
- `take_screenshots.py` - Take screenshots for documentation

### Git commit helper

We add a convenience script for staging all changes, asking for branch confirmation, committing, and pushing.

- `scripts/util/git_commit_and_push.sh` - interactive helper that:
  - prints the current branch and status
  - prompts before staging all changes (git add -A)
  - asks for a commit message (can be provided as argument)
  - requires final confirmation before committing and pushing

Usage:

```bash
# interactive commit with prompt
./scripts/util/git_commit_and_push.sh

# provide commit message as argument
./scripts/util/git_commit_and_push.sh "Fix extractor bug"
```

Notes: the script intentionally uses `git add -A` to ensure all changes (including deletions) are staged before commit; it also explicitly asks which branch to push to and asks for user confirmation before performing the commit and push.

## Usage

Most scripts can be run directly:

```bash
python scripts/debug/debug_session_issue.py
python scripts/test/test_modern_mac_button.py
python scripts/util/create_demo_pdf.py
```

Note: These scripts are for development and testing purposes only.

Tip: Make the script executable with `chmod +x scripts/util/git_commit_and_push.sh` to run it directly.
