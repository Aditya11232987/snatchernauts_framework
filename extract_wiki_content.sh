#!/bin/bash

# Script to help extract and prepare wiki content for GitLab Wiki
echo "📖 GitLab Wiki Content Extractor"
echo "================================="

if [ ! -d "wiki" ]; then
    echo "❌ Error: wiki directory not found"
    exit 1
fi

# Create output directory for easy copying
mkdir -p wiki_content_for_gitlab

echo "📄 Extracting wiki content..."

# Process Home.md
if [ -f "wiki/Home.md" ]; then
    echo "Processing Home page..."
    cat "wiki/Home.md" > "wiki_content_for_gitlab/Home.md"
    echo "✅ Home page ready"
else
    echo "⚠️ Home.md not found in wiki directory"
fi

# Process Installation-Guide.md
if [ -f "wiki/Installation-Guide.md" ]; then
    echo "Processing Installation Guide..."
    cat "wiki/Installation-Guide.md" > "wiki_content_for_gitlab/Installation-Guide.md"
    echo "✅ Installation Guide ready"
else
    echo "⚠️ Installation-Guide.md not found in wiki directory"
fi

echo ""
echo "🎯 Wiki Setup Instructions"
echo "=========================="
echo "1. Go to: https://gitlab.com/grahfmusic/snatchernauts_framework"
echo "2. Enable Wiki in Settings → General → Visibility"
echo "3. Create wiki pages manually using content from wiki_content_for_gitlab/"
echo ""
echo "📋 Pages to create:"
echo "- Home (copy from wiki_content_for_gitlab/Home.md)"
echo "- Installation-Guide (copy from wiki_content_for_gitlab/Installation-Guide.md)"
echo ""
echo "📖 For detailed instructions, see: setup_wiki.md"

# List all available wiki files
echo ""
echo "📚 Available wiki files:"
ls -la wiki/

echo ""
echo "✅ Ready to set up GitLab Wiki!"
