#!/bin/bash

# Snatchernauts Framework - GitLab Setup Script
# This script helps you upload the framework to GitLab

echo "🚀 Snatchernauts Framework - GitLab Setup"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "game" ]; then
    echo "❌ Error: Please run this script from the snatchernauts_framework directory"
    exit 1
fi

# Check git status
echo "📋 Checking git status..."
git status --porcelain
if [ $? -ne 0 ]; then
    echo "❌ Error: Git repository not found or corrupted"
    exit 1
fi

echo "✅ Git repository is ready"

# Instructions for GitLab project creation
echo ""
echo "📝 Step 1: Create GitLab Project"
echo "================================"
echo "1. Go to https://gitlab.com"
echo "2. Click 'New project' → 'Create blank project'"
echo "3. Project name: snatchernauts_framework"
echo "4. Project slug: snatchernauts_framework"  
echo "5. Description: A comprehensive Ren'Py point-and-click adventure game framework"
echo "6. Visibility: Public (recommended for open source)"
echo "7. Initialize with README: NO (we have our own)"
echo "8. Click 'Create project'"

echo ""
read -p "Press Enter after you've created the GitLab project..."

# Get GitLab username and project URL
echo ""
echo "🔧 Step 2: Configure Remote Repository"
echo "======================================"
read -p "Enter your GitLab username: " GITLAB_USERNAME

if [ -z "$GITLAB_USERNAME" ]; then
    echo "❌ Error: GitLab username is required"
    exit 1
fi

GITLAB_URL="https://gitlab.com/${GITLAB_USERNAME}/snatchernauts_framework.git"
echo "GitLab URL: $GITLAB_URL"

# Add remote origin
echo ""
echo "📡 Adding GitLab remote..."
git remote add origin "$GITLAB_URL"

if [ $? -eq 0 ]; then
    echo "✅ Remote origin added successfully"
else
    echo "❌ Error adding remote origin"
    exit 1
fi

# Push to GitLab
echo ""
echo "⬆️  Step 3: Push to GitLab"
echo "=========================="
echo "Pushing main branch and tags..."

git push -u origin main
if [ $? -eq 0 ]; then
    echo "✅ Main branch pushed successfully"
else
    echo "❌ Error pushing main branch"
    echo "Make sure:"
    echo "  - Your GitLab project exists"
    echo "  - You have push permissions"
    echo "  - Your SSH keys are set up (or use HTTPS with username/password)"
    exit 1
fi

# Push tags
echo ""
echo "🏷️  Pushing tags..."
git push origin --tags
if [ $? -eq 0 ]; then
    echo "✅ Tags pushed successfully"
else
    echo "⚠️  Warning: Could not push tags (this is usually okay)"
fi

# Success message
echo ""
echo "🎉 SUCCESS! Repository uploaded to GitLab!"
echo "============================================"
echo "Your project is now available at:"
echo "https://gitlab.com/${GITLAB_USERNAME}/snatchernauts_framework"
echo ""

# Next steps
echo "📋 Step 4: Configure GitLab Features"
echo "===================================="
echo "Visit your GitLab project and:"
echo ""
echo "1. 📖 Enable Wiki:"
echo "   - Go to Settings → General → Visibility"
echo "   - Enable 'Wiki' feature"
echo "   - Create wiki pages from the wiki/ directory content"
echo ""
echo "2. 🐛 Configure Issues:"
echo "   - Go to Settings → General → Visibility"
echo "   - Enable 'Issues' feature"
echo "   - Issue templates are already configured in .gitlab/issue_templates/"
echo ""
echo "3. 💬 Enable Discussions:"
echo "   - Go to Settings → General → Visibility"  
echo "   - Enable 'Discussions' feature"
echo ""
echo "4. 🔧 Set Project Description:"
echo "   - Go to Settings → General → Project information"
echo "   - Copy description from .gitlab/description_templates/project.md"
echo "   - Add tags: renpy, game-framework, point-and-click, detective-game"
echo ""
echo "5. 🚀 Configure CI/CD:"
echo "   - CI/CD pipeline is already configured in .gitlab-ci.yml"
echo "   - It will run automatically on pushes and merge requests"
echo ""
echo "6. 📄 Set up GitLab Pages (optional):"
echo "   - Pages will be automatically deployed from main branch"
echo "   - Documentation will be available at:"
echo "   - https://${GITLAB_USERNAME}.gitlab.io/snatchernauts_framework"
echo ""

echo "✨ Your Snatchernauts Framework is now live on GitLab!"
echo "Share it with the community and start building amazing games! 🎮"
