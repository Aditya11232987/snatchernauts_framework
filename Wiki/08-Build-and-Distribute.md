<div align="center">
  <img src="snatcher-logo.png" alt="Snatchernauts Logo" style="max-width: 480px; width: 100%;" />
</div>

# Build & Distribution Guide

## Overview

This comprehensive guide covers building, testing, and distributing games created with the Snatchernauts Framework. The framework leverages Ren'Py's build system while providing additional tooling and automation for development workflows, continuous integration, and multi-platform distribution.

## Development Workflow

### Prerequisites

**Required Software**:
- **Ren'Py SDK** (version 8.1+ recommended)
- **Python 3.9+** (usually included with Ren'Py SDK)
- **Git** for version control
- **Text editor** with Python/Ren'Py syntax support

**Recommended Tools**:
- **VS Code** with Ren'Py extension
- **GitLab CLI** or **GitHub CLI** for release management
- **Image editing software** for asset creation
- **Audio editing software** for sound assets

**Environment Setup**:
```bash
# Set up Ren'Py SDK path (adjust path as needed)
export RENPY_SDK="/path/to/renpy-sdk"

# For Windows PowerShell
$env:RENPY_SDK = "C:\path\to\renpy-sdk"

# Add to shell profile for persistence
echo 'export RENPY_SDK="/path/to/renpy-sdk"' >> ~/.bashrc
```

### Local Development

#### Running the Game

**Command Line Method**:
```bash
# Navigate to your game directory
cd /path/to/your/snatchernauts-game

# Run the game directly
$RENPY_SDK/renpy.sh .

# Run with specific options
$RENPY_SDK/renpy.sh . --args "debug=true"

# Run in windowed mode
$RENPY_SDK/renpy.sh . --windowed
```

**Ren'Py Launcher Method**:
1. Open the Ren'Py Launcher
2. Navigate to your game directory
3. Select your game from the project list
4. Click "Launch Project"

**Development Shortcuts**:
```bash
# Create aliases for common commands (add to shell profile)
alias run-game='$RENPY_SDK/renpy.sh .'
alias lint-game='$RENPY_SDK/renpy.sh . lint'
alias build-game='$RENPY_SDK/renpy.sh . distribute'
```

#### Code Quality and Linting

**Ren'Py Lint**:
```bash
# Basic linting
$RENPY_SDK/renpy.sh . lint

# Verbose linting with detailed output
$RENPY_SDK/renpy.sh . lint --verbose

# Lint specific files
$RENPY_SDK/renpy.sh . lint game/logic/
```

**Common Lint Issues and Solutions**:
- **Undefined variables**: Check variable initialization and scope
- **Missing images**: Ensure all referenced images exist in `game/images/`
- **Unreachable code**: Review conditional statements and return paths
- **Style warnings**: Follow Ren'Py naming conventions

**Framework-Specific Linting**:
```python
# Add to game/script.rpy for custom lint checks
label lint_framework:
    python:
        # Check for required framework files
        required_files = [
            "game/api/room_api.rpy",
            "game/api/interactions_api.rpy",
            "game/core/options.rpy"
        ]
        
        for file_path in required_files:
            if not renpy.loadable(file_path):
                renpy.error(f"Missing required framework file: {file_path}")
    
    return
```

#### Testing and Debugging

**Debug Mode Activation**:
```python
# In game/core/options.rpy
define config.developer = True  # Enable developer mode
define config.debug = True      # Enable debug features
define config.console = True    # Enable console access
```

**Testing Checklist**:
- [ ] All rooms load without errors
- [ ] Object interactions work correctly
- [ ] Save/load functionality operates properly
- [ ] Visual effects (CRT, bloom, letterbox) render correctly
- [ ] Audio plays correctly across all scenes
- [ ] Multiple input methods (mouse, keyboard, gamepad) function
- [ ] Performance is acceptable on target hardware

**Debugging Tools**:
```python
# Enable framework debug overlay
# Press Cmd+Shift+F12 (macOS) or Ctrl+Shift+F12 (Windows/Linux)
# Cycles through: hidden → compact → verbose → hidden

# Console debugging
# Press Shift+O to open console
$ store.debug_mode = True
$ store.sn_log_enabled = True
$ renpy.display_log("test message")
```

## Build Configuration

### Build Settings

**Build Configuration File** (`game/options.rpy`):
```python
# Build configuration
define build.name = "YourGameName"
define build.version = "0.5.3"
define build.include_update = False

# Archive settings
define build.archive_files = True
define build.classify_renpy = True
define build.encrypt_data = False  # Set True for release

# Platform-specific settings
define build.windows = True
define build.linux = True
define build.mac = True
define build.android = False  # Enable if targeting mobile

# Documentation and assets
define build.documentation_patterns = [
    "*.txt", "*.md", "README*", "CHANGELOG*"
]

# Exclude development files from builds
define build.classify = {
    # Development files
    "**/.git/**": None,
    "**/.vscode/**": None,
    "**/node_modules/**": None,
    
    # Source files
    "**/*.psd": None,
    "**/*.xcf": None,
    "**/*.blend": None,
    
    # Development scripts
    "scripts/dev/**": None,
    "tools/**": None,
    
    # Archive specific classifications
    "game/**.rpy": "archive",
    "game/**.rpyc": "archive",
    "game/images/**": "images",
    "game/audio/**": "audio"
}
```

## Automated Development Workflows

### Repository Synchronization

The Snatchernauts Framework includes powerful automation tools that streamline development workflows across GitLab and GitHub platforms.

**Intelligent README Management**:
```bash
# Manual GitHub README sync
scripts/sync-github-readme.sh

# Automatic sync (enabled by default)
export AUTO_SYNC_README=1  # Set in your shell profile
```

The framework automatically maintains platform-optimized READMEs:
- **GitLab**: Shows pipeline status, GitLab-specific badges
- **GitHub**: Clean presentation, proper logo paths, GitHub-specific badges
- **Zero maintenance**: Edit main `README.md`, GitHub version auto-generated

**Universal Wiki Synchronization**:
```bash
# Sync to both GitLab and GitHub wikis
scripts/sync-wiki.sh

# Platform-specific syncing
scripts/sync-wiki.sh --gitlab-only
scripts/sync-wiki.sh --github-only

# Test changes before deployment
scripts/sync-wiki.sh --dry-run

# Automatic sync on wiki changes
export AUTO_SYNC_WIKI=1
```

**Pre-Push Hook Automation**:
The enhanced pre-push hook provides intelligent automation:
- **README Auto-Sync**: Detects `README.md` changes, updates GitHub version
- **Wiki Auto-Sync**: Pushes `Wiki/` changes to both platform wikis
- **Smart Detection**: Only processes what actually changed
- **Non-blocking**: Never prevents code commits or pushes
- **Environment Controls**: `AUTO_SYNC_README=1` `AUTO_SYNC_WIKI=1`

**Multi-Platform Push Workflow**:
```bash
# Push to both GitLab and GitHub simultaneously
scripts/push-both.sh

# Push specific branches
scripts/push-both.sh feature-branch

# Push all branches
scripts/push-both.sh all
```

### Development Environment Configuration

**Recommended Shell Profile Setup**:
```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
export RENPY_SDK="/path/to/renpy-sdk"
export AUTO_SYNC_README=1  # Enable automatic GitHub README sync
export AUTO_SYNC_WIKI=0    # Manual wiki sync (set to 1 for auto)

# Development aliases
alias run-game='scripts/run-game.sh'
alias lint-game='scripts/lint.sh'
alias sync-readme='scripts/sync-github-readme.sh'
alias sync-wiki='scripts/sync-wiki.sh'
alias push-all='scripts/push-both.sh'
```

**Git Hook Installation**:
The automation hooks install automatically, but you can verify:
```bash
# Verify pre-push hook is active
ls -la .git/hooks/pre-push

# Reinstall hooks if needed
cp scripts/hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### Continuous Integration Setup

**GitLab CI/CD Configuration** (`.gitlab-ci.yml`):
The framework includes production-ready CI/CD pipelines:
- **Linting Stage**: Code quality checks
- **Testing Stage**: Framework functionality tests  
- **Build Stage**: Multi-platform builds
- **Deploy Stage**: Automated releases
- **Mirror Stage**: Repository synchronization to GitHub

**Environment Variables for CI/CD**:
```bash
# GitLab CI/CD Variables (Repository Settings → CI/CD → Variables)
RENPY_SDK_PATH          # Path to Ren'Py SDK in CI environment
GITHUB_MIRROR_TOKEN     # GitHub access token for mirroring
DEPLOY_KEY_PRIVATE      # SSH private key for deployments
BUILD_ENCRYPTION_KEY    # Key for encrypting release builds
```

### Asset Optimization

**Image Optimization**:
```bash
# Optimize PNG images
for img in game/images/**/*.png; do
    optipng -o7 "$img"
done

# Optimize JPEG images
for img in game/images/**/*.jpg; do
    jpegoptim --max=85 "$img"
done

# Convert large images to WebP (if supported)
for img in game/images/**/*.png; do
    cwebp -q 80 "$img" -o "${img%.png}.webp"
done
```

**Audio Optimization**:
```bash
# Optimize OGG files
for audio in game/audio/**/*.ogg; do
    # Re-encode at optimal quality
    oggenc -q 6 "$audio" -o "${audio}_optimized"
    mv "${audio}_optimized" "$audio"
done

# Convert WAV to OGG
for audio in game/audio/**/*.wav; do
    oggenc -q 6 "$audio" -o "${audio%.wav}.ogg"
done
```

**Pre-Build Optimization Script**:
```python
# tools/optimize_assets.py
import os
import subprocess
from pathlib import Path

def optimize_images(game_path):
    """Optimize all images in the game directory"""
    images_path = Path(game_path) / "game" / "images"
    
    for img_file in images_path.rglob("*.png"):
        print(f"Optimizing {img_file}")
        subprocess.run(["optipng", "-o7", str(img_file)])
    
    for img_file in images_path.rglob("*.jpg"):
        print(f"Optimizing {img_file}")
        subprocess.run(["jpegoptim", "--max=85", str(img_file)])

def optimize_audio(game_path):
    """Optimize all audio files in the game directory"""
    audio_path = Path(game_path) / "game" / "audio"
    
    for audio_file in audio_path.rglob("*.wav"):
        ogg_file = audio_file.with_suffix(".ogg")
        print(f"Converting {audio_file} to {ogg_file}")
        subprocess.run(["oggenc", "-q", "6", str(audio_file), "-o", str(ogg_file)])
        os.remove(audio_file)  # Remove original WAV

if __name__ == "__main__":
    game_directory = os.getcwd()
    optimize_images(game_directory)
    optimize_audio(game_directory)
    print("Asset optimization complete!")
```

## Distribution

### Ren'Py Launcher Method

**Step-by-Step Build Process**:
1. **Open Ren'Py Launcher**
2. **Select your project** from the project list
3. **Click "Build & Distribute"**
4. **Configure build options**:
   - Select target platforms (Windows, Linux, macOS)
   - Choose build type (Normal or Update)
   - Set up signing (if applicable)
5. **Click "Build" to start the build process**
6. **Monitor build progress** in the console output
7. **Verify build outputs** in the `dist/` directory

**Build Output Structure**:
```
dist/
├── YourGame-1.0-win.zip          # Windows build
├── YourGame-1.0-linux.tar.bz2    # Linux build  
├── YourGame-1.0-mac.zip           # macOS build
└── YourGame-1.0-update.zip        # Update package
```

### Command Line Build Method

**Basic Distribution**:
```bash
# Build for all configured platforms
$RENPY_SDK/renpy.sh . distribute

# Build for specific platforms
$RENPY_SDK/renpy.sh . distribute --platform windows
$RENPY_SDK/renpy.sh . distribute --platform linux
$RENPY_SDK/renpy.sh . distribute --platform mac

# Build with custom destination
$RENPY_SDK/renpy.sh . distribute --dest /custom/build/path

# Clean build (remove previous builds)
$RENPY_SDK/renpy.sh . distribute --clean
```

**Advanced Build Options**:
```bash
# Build with signing (requires configured certificates)
$RENPY_SDK/renpy.sh . distribute --sign

# Build update package only
$RENPY_SDK/renpy.sh . distribute --update-only

# Verbose build output
$RENPY_SDK/renpy.sh . distribute --verbose

# Build with specific Ren'Py version
$RENPY_SDK/renpy.sh . distribute --renpy-version 8.1.0
```

### Automated Build Script

**Build Automation Script** (`scripts/build.py`):
```python
#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def clean_build_directory():
    """Clean previous build artifacts"""
    dist_path = Path("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)
        print("Cleaned previous build directory")

def run_lint():
    """Run Ren'Py linting"""
    print("Running lint checks...")
    result = subprocess.run([f"{os.environ['RENPY_SDK']}/renpy.sh", ".", "lint"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Lint failed:\n{result.stdout}\n{result.stderr}")
        return False
    print("Lint checks passed")
    return True

def optimize_assets():
    """Run asset optimization"""
    print("Optimizing assets...")
    try:
        subprocess.run(["python", "tools/optimize_assets.py"], check=True)
        print("Asset optimization complete")
    except subprocess.CalledProcessError:
        print("Asset optimization failed (optional step)")

def build_game(platforms=None, sign=False, clean=False):
    """Build the game for specified platforms"""
    if clean:
        clean_build_directory()
    
    cmd = [f"{os.environ['RENPY_SDK']}/renpy.sh", ".", "distribute"]
    
    if platforms:
        for platform in platforms:
            cmd.extend(["--platform", platform])
    
    if sign:
        cmd.append("--sign")
    
    print(f"Building game with command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def create_build_info():
    """Create build information file"""
    build_info = {
        "build_date": datetime.now().isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        "git_branch": subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip(),
        "framework_version": "0.5.3"
    }
    
    with open("dist/build_info.json", "w") as f:
        import json
        json.dump(build_info, f, indent=2)
    
    print("Created build information file")

def main():
    parser = argparse.ArgumentParser(description="Build Snatchernauts Framework game")
    parser.add_argument("--platforms", nargs="+", choices=["windows", "linux", "mac"], 
                       help="Platforms to build for")
    parser.add_argument("--sign", action="store_true", help="Sign the builds")
    parser.add_argument("--clean", action="store_true", help="Clean build directory first")
    parser.add_argument("--skip-lint", action="store_true", help="Skip lint checks")
    parser.add_argument("--skip-optimize", action="store_true", help="Skip asset optimization")
    
    args = parser.parse_args()
    
    # Check for required environment
    if "RENPY_SDK" not in os.environ:
        print("Error: RENPY_SDK environment variable not set")
        sys.exit(1)
    
    # Run pre-build steps
    if not args.skip_lint and not run_lint():
        print("Build aborted due to lint errors")
        sys.exit(1)
    
    if not args.skip_optimize:
        optimize_assets()
    
    # Build the game
    if build_game(args.platforms, args.sign, args.clean):
        create_build_info()
        print("Build completed successfully!")
        
        # List build outputs
        dist_path = Path("dist")
        if dist_path.exists():
            print("\nBuild outputs:")
            for file in dist_path.glob("*"):
                size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"  {file.name} ({size:.1f} MB)")
    else:
        print("Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Usage Examples**:
```bash
# Build for all platforms
python scripts/build.py

# Build for Windows only
python scripts/build.py --platforms windows

# Clean build with signing
python scripts/build.py --clean --sign

# Quick build (skip optimization and lint)
python scripts/build.py --skip-lint --skip-optimize
```

## Continuous Integration

### GitLab CI Configuration

**`.gitlab-ci.yml` Configuration**:
```yaml
# GitLab CI/CD Pipeline for Snatchernauts Framework

stages:
  - lint
  - test
  - build
  - deploy
  - mirror

variables:
  RENPY_VERSION: "8.1.0"
  GAME_NAME: "YourGameName"

# Cache for faster builds
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - renpy-sdk/

# Lint stage
lint:
  stage: lint
  image: python:3.9
  script:
    - python scripts/setup_ci.py
    - $RENPY_SDK/renpy.sh . lint
  artifacts:
    reports:
      junit: lint-report.xml
    expire_in: 1 week
  only:
    - merge_requests
    - develop
    - main

# Test stage
test_game:
  stage: test
  image: python:3.9
  script:
    - python scripts/setup_ci.py
    - python scripts/run_tests.py
  artifacts:
    reports:
      junit: test-results.xml
    paths:
      - test-coverage/
    expire_in: 1 week
  coverage: '/TOTAL.*\s+(\d+%)$/'
  only:
    - merge_requests
    - develop
    - main

# Build stages for different platforms
build_windows:
  stage: build
  image: python:3.9
  script:
    - python scripts/setup_ci.py
    - python scripts/build.py --platforms windows
  artifacts:
    paths:
      - dist/*-win.zip
    expire_in: 1 month
  only:
    - tags
    - main

build_linux:
  stage: build
  image: python:3.9
  script:
    - python scripts/setup_ci.py
    - python scripts/build.py --platforms linux
  artifacts:
    paths:
      - dist/*-linux.tar.bz2
    expire_in: 1 month
  only:
    - tags
    - main

build_mac:
  stage: build
  image: python:3.9
  script:
    - python scripts/setup_ci.py
    - python scripts/build.py --platforms mac
  artifacts:
    paths:
      - dist/*-mac.zip
    expire_in: 1 month
  only:
    - tags
    - main
  # Note: macOS builds require macOS runners
  tags:
    - macos

# Create release
create_release:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - python scripts/create_release.py
  dependencies:
    - build_windows
    - build_linux
    - build_mac
  only:
    - tags
  when: manual

# Mirror wiki to GitHub
mirror_wiki:
  stage: mirror
  image: alpine/git:latest
  script:
    - git clone --mirror $CI_REPOSITORY_URL temp_repo
    - cd temp_repo
    - git push --mirror https://github.com/yourusername/your-repo.git
  only:
    - main
    - wiki
  when: manual
```

**CI Setup Script** (`scripts/setup_ci.py`):
```python
#!/usr/bin/env python3
"""CI environment setup script"""
import os
import sys
import urllib.request
import tarfile
import zipfile
from pathlib import Path

RENPY_VERSION = os.environ.get("RENPY_VERSION", "8.1.0")
RENPY_URL_TEMPLATE = "https://www.renpy.org/dl/{version}/renpy-{version}-sdk.tar.bz2"

def download_renpy_sdk():
    """Download and extract Ren'Py SDK"""
    sdk_path = Path("renpy-sdk")
    
    if sdk_path.exists():
        print(f"Ren'Py SDK already exists at {sdk_path}")
        return sdk_path
    
    url = RENPY_URL_TEMPLATE.format(version=RENPY_VERSION)
    archive_name = f"renpy-{RENPY_VERSION}-sdk.tar.bz2"
    
    print(f"Downloading Ren'Py SDK {RENPY_VERSION}...")
    urllib.request.urlretrieve(url, archive_name)
    
    print("Extracting Ren'Py SDK...")
    with tarfile.open(archive_name, "r:bz2") as tar:
        tar.extractall()
    
    # Rename extracted directory to standard name
    extracted_dir = Path(f"renpy-{RENPY_VERSION}-sdk")
    if extracted_dir.exists():
        extracted_dir.rename(sdk_path)
    
    os.remove(archive_name)
    print(f"Ren'Py SDK installed at {sdk_path}")
    return sdk_path

def setup_environment():
    """Set up CI environment variables"""
    sdk_path = download_renpy_sdk()
    
    # Set environment variable
    os.environ["RENPY_SDK"] = str(sdk_path.absolute())
    
    # Create CI-specific configuration
    ci_config = '''
# CI-specific configuration
define config.developer = False
define config.debug = False
define config.console = False
define config.autosave_on_quit = False
define config.quit_on_mobile_background = False
'''
    
    with open("game/ci_options.rpy", "w") as f:
        f.write(ci_config)
    
    print("CI environment setup complete")

if __name__ == "__main__":
    setup_environment()
```

### GitHub Actions Configuration

**`.github/workflows/build.yml`**:
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Setup Ren'Py SDK
      run: python scripts/setup_ci.py
    
    - name: Run lint
      run: $RENPY_SDK/renpy.sh . lint

  build:
    needs: lint
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        include:
          - os: ubuntu-latest
            platform: linux
          - os: windows-latest
            platform: windows  
          - os: macos-latest
            platform: mac
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Setup Ren'Py SDK
      run: python scripts/setup_ci.py
      shell: bash
    
    - name: Build game
      run: python scripts/build.py --platforms ${{ matrix.platform }}
      shell: bash
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-${{ matrix.platform }}
        path: dist/

  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Download all artifacts
      uses: actions/download-artifact@v3
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: build-*/*
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Platform-Specific Considerations

### Windows Distribution

**Code Signing** (Optional):
```bash
# Sign Windows executables (requires certificate)
signtool sign /f "certificate.pfx" /p "password" /t "http://timestamp.verisign.com/scripts/timstamp.dll" "YourGame.exe"

# Verify signature
signtool verify /pa "YourGame.exe"
```

**Windows Installer** (Optional):
```nsis
; NSIS installer script (installer.nsi)
!define APPNAME "Your Game Name"
!define VERSION "0.5.3"

Name "${APPNAME}"
OutFile "${APPNAME}-${VERSION}-installer.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"

Section "Install"
    SetOutPath $INSTDIR
    File /r "dist\YourGame-win\*"
    
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\YourGame.exe"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
SectionEnd
```

### macOS Distribution

**Code Signing**:
```bash
# Sign the macOS app bundle
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" "YourGame.app"

# Create signed DMG
hdiutil create -volname "Your Game" -srcfolder "YourGame.app" -ov -format UDZO "YourGame-mac.dmg"
codesign --sign "Developer ID Application: Your Name" "YourGame-mac.dmg"
```

**Notarization** (for macOS 10.15+):
```bash
# Submit for notarization
xcrun altool --notarize-app --primary-bundle-id "com.yourcompany.yourgame" --username "your-email@example.com" --password "@keychain:AC_PASSWORD" --file "YourGame-mac.dmg"

# Check notarization status
xcrun altool --notarization-info "request-id" --username "your-email@example.com" --password "@keychain:AC_PASSWORD"

# Staple the notarization
xcrun stapler staple "YourGame-mac.dmg"
```

### Linux Distribution

**AppImage Creation**:
```bash
# Create AppImage (requires appimagetool)
# Create AppDir structure
mkdir -p YourGame.AppDir/usr/bin
cp -r dist/YourGame-linux/* YourGame.AppDir/usr/bin/

# Create desktop file
cat > YourGame.AppDir/YourGame.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Your Game Name
Exec=YourGame
Icon=yourgame
Categories=Game;
EOF

# Create AppImage
appimagetool YourGame.AppDir YourGame-x86_64.AppImage
```

## Distribution Platforms

### Steam Integration

**Steamworks SDK Integration**:
```python
# Add to game/options.rpy
define config.steam = True
define config.steam_appid = 123456789  # Your Steam App ID

# Steam achievement integration
init python:
    if config.steam:
        try:
            import steam
            steam.initialize()
        except ImportError:
            print("Steam SDK not available")
```

**Steam Upload Script**:
```bash
#!/bin/bash
# Steam content upload script

# Build the game first
python scripts/build.py --platforms windows linux mac

# Upload to Steam using SteamCMD
steamcmd +login $STEAM_USERNAME +run_app_build scripts/steam_build_windows.vdf +quit
steamcmd +login $STEAM_USERNAME +run_app_build scripts/steam_build_linux.vdf +quit
steamcmd +login $STEAM_USERNAME +run_app_build scripts/steam_build_mac.vdf +quit
```

### Itch.io Distribution

**Butler Upload**:
```bash
# Install butler (itch.io upload tool)
# https://itch.io/docs/butler/

# Upload builds to itch.io
butler push dist/YourGame-win.zip yourusername/yourgame:windows
butler push dist/YourGame-linux.tar.bz2 yourusername/yourgame:linux
butler push dist/YourGame-mac.zip yourusername/yourgame:osx

# Check upload status
butler status yourusername/yourgame
```

## Troubleshooting

### Common Build Issues

**Missing Assets**:
```bash
# Find missing image references
grep -r "images/" game/ | grep -v "\.rpyc" | while read line; do
    image=$(echo $line | sed -n 's/.*images\/\([^"]*\).*/\1/p')
    if [ ! -f "game/images/$image" ]; then
        echo "Missing image: game/images/$image"
    fi
done
```

**Build Size Optimization**:
```python
# Add to game/options.rpy to reduce build size
define build.include_i686 = False  # Exclude 32-bit libraries
define build.include_old_themes = False  # Exclude legacy themes
define build.renpy_patterns = [    # Exclude unused Ren'Py files
    "**~", "**/#*", "**/.*", 
    "**.old", "**.new", "**.rpa", "**.rpi"
]
```

**Performance Issues**:
```python
# Add performance monitoring
init python:
    def log_performance():
        fps = renpy.get_fps()
        if fps < 30:
            print(f"Low FPS detected: {fps}")
        
        memory = renpy.get_memory_usage()
        if memory > 500 * 1024 * 1024:  # 500MB
            print(f"High memory usage: {memory / 1024 / 1024:.1f}MB")
    
    # Call periodically
    config.periodic_callbacks.append(log_performance)
```

### Build Environment Issues

**Ren'Py SDK Path Issues**:
```bash
# Verify Ren'Py SDK path
if [ -z "$RENPY_SDK" ]; then
    echo "Error: RENPY_SDK environment variable not set"
    echo "Set it with: export RENPY_SDK=/path/to/renpy-sdk"
    exit 1
fi

if [ ! -f "$RENPY_SDK/renpy.sh" ]; then
    echo "Error: renpy.sh not found in $RENPY_SDK"
    echo "Verify that RENPY_SDK points to the correct directory"
    exit 1
fi
```

**Python Version Compatibility**:
```python
# Check Python compatibility
import sys
if sys.version_info < (3, 8):
    print("Warning: Python 3.8+ recommended for best compatibility")
    print(f"Current version: {sys.version}")

# Check for required modules
required_modules = ['pygame', 'numpy', 'PIL']
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Missing required module: {module}")
```

The build and distribution system provides a comprehensive workflow for creating, testing, and distributing games built with the Snatchernauts Framework, with support for multiple platforms, automated CI/CD pipelines, and various distribution channels.

