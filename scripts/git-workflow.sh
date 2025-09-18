#!/bin/bash

# Git Workflow Helper Script for ExnestAI Python SDK

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "ExnestAI Python SDK Git Workflow Helper"
    echo ""
    echo "Usage: ./scripts/git-workflow.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  feature <name>     Create a new feature branch"
    echo "  hotfix <name>      Create a new hotfix branch"
    echo "  release <version>  Create a new release branch"
    echo "  sync-develop       Sync develop branch with main"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/git-workflow.sh feature add-streaming-support"
    echo "  ./scripts/git-workflow.sh release v1.2.0"
}

# Function to create feature branch
create_feature_branch() {
    local feature_name=$1
    
    if [ -z "$feature_name" ]; then
        print_error "Feature name is required"
        return 1
    fi
    
    print_info "Creating feature branch: feature/$feature_name"
    
    # Switch to develop and pull latest changes
    git checkout develop
    git pull origin develop
    
    # Create feature branch
    git checkout -b feature/$feature_name
    
    print_success "Feature branch 'feature/$feature_name' created successfully"
    print_info "You are now on branch: $(git branch --show-current)"
}

# Function to create hotfix branch
create_hotfix_branch() {
    local hotfix_name=$1
    
    if [ -z "$hotfix_name" ]; then
        print_error "Hotfix name is required"
        return 1
    fi
    
    print_info "Creating hotfix branch: hotfix/$hotfix_name"
    
    # Switch to main and pull latest changes
    git checkout main
    git pull origin main
    
    # Create hotfix branch
    git checkout -b hotfix/$hotfix_name
    
    print_success "Hotfix branch 'hotfix/$hotfix_name' created successfully"
    print_info "You are now on branch: $(git branch --show-current)"
}

# Function to create release branch
create_release_branch() {
    local version=$1
    
    if [ -z "$version" ]; then
        print_error "Version is required"
        return 1
    fi
    
    print_info "Creating release branch: release/$version"
    
    # Switch to develop and pull latest changes
    git checkout develop
    git pull origin develop
    
    # Create release branch
    git checkout -b release/$version
    
    print_success "Release branch 'release/$version' created successfully"
    print_info "You are now on branch: $(git branch --show-current)"
}

# Function to sync develop with main
sync_develop() {
    print_info "Syncing develop branch with main"
    
    # Switch to main and pull latest changes
    git checkout main
    git pull origin main
    
    # Switch to develop and pull latest changes
    git checkout develop
    git pull origin develop
    
    # Merge main into develop
    git merge main
    
    # Push changes
    git push origin develop
    
    print_success "Develop branch synced with main successfully"
}

# Main script logic
case $1 in
    "feature")
        create_feature_branch $2
        ;;
    "hotfix")
        create_hotfix_branch $2
        ;;
    "release")
        create_release_branch $2
        ;;
    "sync-develop")
        sync_develop
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac