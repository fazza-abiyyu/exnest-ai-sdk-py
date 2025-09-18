# Scripts

This directory contains helper scripts for development and Git workflow management.

## Git Workflow Helper Script

The [git-workflow.sh](file:///Users/fazza_abiyyu/Documents/Projects/Express/sdk-exnestai-py/scripts/git-workflow.sh) script helps automate common Git workflow tasks.

### Usage

```bash
# Make the script executable (if not already)
chmod +x scripts/git-workflow.sh

# Create a new feature branch
./scripts/git-workflow.sh feature feature-name

# Create a new hotfix branch
./scripts/git-workflow.sh hotfix hotfix-name

# Create a new release branch
./scripts/git-workflow.sh release v1.2.0

# Sync develop branch with main
./scripts/git-workflow.sh sync-develop

# Show help
./scripts/git-workflow.sh help
```

### Commands

- `feature <name>`: Creates a new feature branch from `develop`
- `hotfix <name>`: Creates a new hotfix branch from `main`
- `release <version>`: Creates a new release branch from `develop`
- `sync-develop`: Syncs the `develop` branch with `main`
- `help`: Shows the help message

### Examples

```bash
# Create a feature branch for adding streaming support
./scripts/git-workflow.sh feature add-streaming-support

# Create a hotfix for a critical bug
./scripts/git-workflow.sh hotfix fix-authentication-error

# Create a release branch for version 1.2.0
./scripts/git-workflow.sh release v1.2.0
```