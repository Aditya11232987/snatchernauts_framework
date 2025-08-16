# Build and Distribution

**Part II: Core Development - Chapter 9**

*Comprehensive guide to professional build processes, automated deployment pipelines, and multi-platform distribution strategies for games created with the Snatchernauts Framework.*

---

## Chapter Overview

This chapter provides complete coverage of the build and distribution pipeline for Snatchernauts Framework games, from local development workflows to production deployment across multiple platforms. The framework extends Ren'Py's build system with sophisticated automation tools, continuous integration pipelines, and professional distribution strategies.

The build system is designed for scalability and maintainability, supporting everything from solo indie development to team-based production environments. Every aspect is optimized for efficiency, reliability, and cross-platform compatibility.

**What makes this build system comprehensive:**
- **Professional Workflows**: Industry-standard development and deployment practices
- **Automated Pipelines**: CI/CD integration with GitLab, GitHub, and other platforms
- **Multi-Platform Support**: Native builds for Windows, macOS, Linux, and mobile platforms
- **Quality Assurance**: Automated testing, linting, and performance monitoring
- **Production Deployment**: Professional distribution to Steam, itch.io, and other platforms

**By the end of this chapter, you will master:**
- Complete development workflow setup and optimization
- Advanced build configuration and customization techniques
- Automated testing and quality assurance pipelines
- Multi-platform deployment and distribution strategies
- Performance optimization and troubleshooting methodologies
- Professional release management and version control
- Platform-specific signing, notarization, and certification processes
- Advanced CI/CD pipeline configuration and maintenance

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

## Advanced Build Configurations

### Custom Build Profiles

The framework supports multiple build profiles for different deployment scenarios:

```python
# File: game/build_profiles.rpy

# Development build profile
define BUILD_PROFILES = {
    "development": {
        "debug": True,
        "console": True,
        "developer": True,
        "encrypt_data": False,
        "include_source": True,
        "optimization_level": 0
    },
    
    # Testing/QA build profile
    "testing": {
        "debug": False,
        "console": True,
        "developer": False,
        "encrypt_data": False,
        "include_source": False,
        "optimization_level": 1,
        "enable_analytics": True,
        "crash_reporting": True
    },
    
    # Production release profile
    "production": {
        "debug": False,
        "console": False,
        "developer": False,
        "encrypt_data": True,
        "include_source": False,
        "optimization_level": 2,
        "enable_analytics": True,
        "crash_reporting": True,
        "anti_tamper": True
    },
    
    # Demo/preview build profile
    "demo": {
        "debug": False,
        "console": False,
        "developer": False,
        "encrypt_data": True,
        "include_source": False,
        "optimization_level": 2,
        "demo_mode": True,
        "time_limit": 3600,  # 1 hour demo
        "content_restriction": "demo"
    }
}

# Apply build profile configuration
init python:
    import os
    
    def apply_build_profile(profile_name):
        """Apply specific build profile settings"""
        profile = BUILD_PROFILES.get(profile_name, BUILD_PROFILES["development"])
        
        # Apply core settings
        config.debug = profile.get("debug", False)
        config.console = profile.get("console", False)
        config.developer = profile.get("developer", False)
        
        # Apply build settings
        build.encrypt_data = profile.get("encrypt_data", False)
        
        # Apply optimization settings
        optimization = profile.get("optimization_level", 0)
        if optimization >= 1:
            # Enable basic optimizations
            config.optimize_gl = True
            config.gl_resize = True
        if optimization >= 2:
            # Enable aggressive optimizations
            config.gl_clear_alpha = False
            config.hw_video = True
            build.include_update = False
        
        # Apply demo restrictions if applicable
        if profile.get("demo_mode", False):
            store.demo_mode = True
            store.demo_time_limit = profile.get("time_limit", 1800)
        
        print(f"Applied build profile: {profile_name}")
    
    # Auto-apply profile based on environment
    profile = os.environ.get("BUILD_PROFILE", "development")
    apply_build_profile(profile)
```

### Automated Quality Assurance

**Comprehensive Testing Suite**:

```python
# File: scripts/run_tests.py

import unittest
import subprocess
import json
import sys
from pathlib import Path

class FrameworkTestSuite:
    """Comprehensive test suite for framework games"""
    
    def __init__(self, game_path="."):
        self.game_path = Path(game_path)
        self.test_results = {
            "lint": None,
            "syntax": None,
            "assets": None,
            "functionality": None,
            "performance": None
        }
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("Running comprehensive test suite...")
        
        # 1. Lint tests
        self.test_results["lint"] = self.test_lint()
        
        # 2. Syntax validation
        self.test_results["syntax"] = self.test_syntax()
        
        # 3. Asset validation
        self.test_results["assets"] = self.test_assets()
        
        # 4. Functionality tests
        self.test_results["functionality"] = self.test_functionality()
        
        # 5. Performance tests
        self.test_results["performance"] = self.test_performance()
        
        return self.generate_report()
    
    def test_lint(self):
        """Run Ren'Py lint checks"""
        print("Running lint tests...")
        try:
            result = subprocess.run(
                [f"{os.environ['RENPY_SDK']}/renpy.sh", ".", "lint"],
                capture_output=True, text=True, cwd=self.game_path
            )
            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_syntax(self):
        """Validate Python/Ren'Py syntax in all files"""
        print("Testing syntax validation...")
        errors = []
        
        # Test all .rpy files
        for rpy_file in self.game_path.glob("game/**/*.rpy"):
            try:
                with open(rpy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic syntax checks
                if 'init python:' in content:
                    # Extract Python blocks for syntax checking
                    python_blocks = self.extract_python_blocks(content)
                    for block_num, block in enumerate(python_blocks):
                        try:
                            compile(block, f"{rpy_file}:block_{block_num}", 'exec')
                        except SyntaxError as e:
                            errors.append(f"{rpy_file}:block_{block_num}: {e}")
                            
            except Exception as e:
                errors.append(f"{rpy_file}: {e}")
        
        return {
            "passed": len(errors) == 0,
            "errors": errors,
            "files_checked": len(list(self.game_path.glob("game/**/*.rpy")))
        }
    
    def test_assets(self):
        """Validate all game assets"""
        print("Testing asset validation...")
        issues = []
        
        # Check for missing images
        image_references = self.find_image_references()
        for ref in image_references:
            image_path = self.game_path / "game" / "images" / ref
            if not image_path.exists():
                issues.append(f"Missing image: {ref}")
        
        # Check for missing audio
        audio_references = self.find_audio_references()
        for ref in audio_references:
            audio_path = self.game_path / "game" / "audio" / ref
            if not audio_path.exists():
                issues.append(f"Missing audio: {ref}")
        
        # Check asset optimization
        oversized_assets = self.find_oversized_assets()
        for asset, size in oversized_assets:
            issues.append(f"Large asset ({size:.1f}MB): {asset}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "image_refs_checked": len(image_references),
            "audio_refs_checked": len(audio_references)
        }
    
    def test_functionality(self):
        """Test core framework functionality"""
        print("Testing functionality...")
        functionality_tests = []
        
        # Test room system
        room_test = self.test_room_system()
        functionality_tests.append(room_test)
        
        # Test logic hooks
        hooks_test = self.test_logic_hooks()
        functionality_tests.append(hooks_test)
        
        # Test save/load system
        save_test = self.test_save_load()
        functionality_tests.append(save_test)
        
        all_passed = all(test["passed"] for test in functionality_tests)
        
        return {
            "passed": all_passed,
            "tests": functionality_tests
        }
    
    def test_performance(self):
        """Run performance benchmarks"""
        print("Testing performance...")
        
        # Measure build size
        build_size = self.measure_build_size()
        
        # Test memory usage patterns
        memory_test = self.test_memory_usage()
        
        # Test startup time
        startup_test = self.test_startup_time()
        
        return {
            "passed": True,  # Performance tests are informational
            "build_size_mb": build_size,
            "memory_test": memory_test,
            "startup_test": startup_test
        }
    
    def extract_python_blocks(self, content):
        """Extract Python code blocks from Ren'Py files"""
        blocks = []
        lines = content.split('\n')
        in_python_block = False
        current_block = []
        indent_level = 0
        
        for line in lines:
            if 'init python:' in line or line.strip().startswith('python:'):
                in_python_block = True
                indent_level = len(line) - len(line.lstrip())
                continue
            
            if in_python_block:
                line_indent = len(line) - len(line.lstrip())
                if line.strip() and line_indent <= indent_level and not line.startswith(' '):
                    # End of Python block
                    if current_block:
                        blocks.append('\n'.join(current_block))
                        current_block = []
                    in_python_block = False
                else:
                    current_block.append(line)
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def find_image_references(self):
        """Find all image references in game files"""
        import re
        references = set()
        
        for rpy_file in self.game_path.glob("game/**/*.rpy"):
            try:
                with open(rpy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find image references
                patterns = [
                    r'"images/([^"]+)"',
                    r"'images/([^']+)'",
                    r'show\s+([^\s]+)',
                    r'scene\s+([^\s]+)'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    references.update(matches)
                    
            except Exception:
                continue
        
        return list(references)
    
    def find_audio_references(self):
        """Find all audio references in game files"""
        import re
        references = set()
        
        for rpy_file in self.game_path.glob("game/**/*.rpy"):
            try:
                with open(rpy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find audio references
                patterns = [
                    r'"audio/([^"]+)"',
                    r"'audio/([^']+)'",
                    r'play\s+music\s+"([^"]+)"',
                    r'play\s+sound\s+"([^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    references.update(matches)
                    
            except Exception:
                continue
        
        return list(references)
    
    def find_oversized_assets(self, max_size_mb=10):
        """Find assets larger than specified size"""
        oversized = []
        
        # Check images
        for img_file in self.game_path.glob("game/images/**/*"):
            if img_file.is_file():
                size_mb = img_file.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    oversized.append((str(img_file.relative_to(self.game_path)), size_mb))
        
        # Check audio
        for audio_file in self.game_path.glob("game/audio/**/*"):
            if audio_file.is_file():
                size_mb = audio_file.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    oversized.append((str(audio_file.relative_to(self.game_path)), size_mb))
        
        return oversized
    
    def test_room_system(self):
        """Test room system functionality"""
        # This would need to run actual game code
        # For now, check that room definitions exist
        try:
            room_files = list(self.game_path.glob("game/rooms/**/config.rpy"))
            return {
                "name": "room_system",
                "passed": len(room_files) > 0,
                "rooms_found": len(room_files)
            }
        except Exception as e:
            return {"name": "room_system", "passed": False, "error": str(e)}
    
    def test_logic_hooks(self):
        """Test logic hook system"""
        # Check for logic hook implementations
        hook_files = list(self.game_path.glob("game/logic/**/*logic.rpy"))
        return {
            "name": "logic_hooks",
            "passed": len(hook_files) > 0,
            "logic_files_found": len(hook_files)
        }
    
    def test_save_load(self):
        """Test save/load system"""
        # Basic check for save/load related code
        save_references = 0
        
        for rpy_file in self.game_path.glob("game/**/*.rpy"):
            try:
                with open(rpy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'persistent.' in content or 'save(' in content or 'load(' in content:
                        save_references += 1
            except Exception:
                continue
        
        return {
            "name": "save_load",
            "passed": save_references > 0,
            "save_references": save_references
        }
    
    def measure_build_size(self):
        """Estimate build size by measuring game directory"""
        total_size = 0
        for file_path in self.game_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    def test_memory_usage(self):
        """Estimate memory usage based on assets"""
        # This is a rough estimate
        image_size = sum(
            f.stat().st_size for f in self.game_path.glob("game/images/**/*")
            if f.is_file()
        )
        
        audio_size = sum(
            f.stat().st_size for f in self.game_path.glob("game/audio/**/*")
            if f.is_file()
        )
        
        return {
            "estimated_image_memory_mb": image_size / (1024 * 1024),
            "estimated_audio_memory_mb": audio_size / (1024 * 1024),
            "estimated_total_mb": (image_size + audio_size) / (1024 * 1024)
        }
    
    def test_startup_time(self):
        """Test estimated startup time based on asset count"""
        image_count = len(list(self.game_path.glob("game/images/**/*")))
        audio_count = len(list(self.game_path.glob("game/audio/**/*")))
        script_count = len(list(self.game_path.glob("game/**/*.rpy")))
        
        # Rough estimate based on asset counts
        estimated_startup_ms = (image_count * 2) + (audio_count * 5) + (script_count * 3)
        
        return {
            "estimated_startup_ms": estimated_startup_ms,
            "asset_counts": {
                "images": image_count,
                "audio": audio_count,
                "scripts": script_count
            }
        }
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len([r for r in self.test_results.values() if r is not None])
        passed_tests = len([r for r in self.test_results.values() if r and r.get("passed")])
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save report
        with open(self.game_path / "test-results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return report

if __name__ == "__main__":
    import os
    from datetime import datetime
    
    # Run tests
    tester = FrameworkTestSuite()
    report = tester.run_all_tests()
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"  Total tests: {report['summary']['total_tests']}")
    print(f"  Passed: {report['summary']['passed_tests']}")
    print(f"  Success rate: {report['summary']['success_rate']:.1f}%")
    
    # Exit with error code if tests failed
    if report['summary']['success_rate'] < 100:
        sys.exit(1)
```

### Advanced Deployment Strategies

**Blue-Green Deployment System**:

```python
# File: scripts/deploy_system.py

class BlueGreenDeployment:
    """Blue-green deployment system for zero-downtime updates"""
    
    def __init__(self, config):
        self.config = config
        self.environments = {
            'blue': config['blue_environment'],
            'green': config['green_environment']
        }
        self.current_active = self.get_active_environment()
    
    def deploy_new_version(self, version, artifacts_path):
        """Deploy new version using blue-green strategy"""
        # Determine target environment (opposite of current active)
        target_env = 'green' if self.current_active == 'blue' else 'blue'
        
        print(f"Deploying version {version} to {target_env} environment")
        
        # 1. Deploy to inactive environment
        self.deploy_to_environment(target_env, artifacts_path)
        
        # 2. Run health checks
        if not self.health_check(target_env):
            print(f"Health check failed for {target_env}, aborting deployment")
            return False
        
        # 3. Run smoke tests
        if not self.smoke_tests(target_env):
            print(f"Smoke tests failed for {target_env}, aborting deployment")
            return False
        
        # 4. Switch traffic to new environment
        self.switch_traffic(target_env)
        
        # 5. Update active environment tracking
        self.set_active_environment(target_env)
        
        print(f"Successfully deployed version {version}")
        return True
    
    def rollback(self):
        """Rollback to previous environment"""
        previous_env = 'green' if self.current_active == 'blue' else 'blue'
        
        print(f"Rolling back from {self.current_active} to {previous_env}")
        
        # Switch traffic back
        self.switch_traffic(previous_env)
        self.set_active_environment(previous_env)
        
        print("Rollback completed")
    
    def deploy_to_environment(self, env, artifacts_path):
        """Deploy artifacts to specific environment"""
        env_config = self.environments[env]
        
        # Upload build artifacts
        self.upload_artifacts(env_config, artifacts_path)
        
        # Update environment configuration
        self.update_environment_config(env_config)
        
        # Restart services
        self.restart_services(env_config)
    
    def health_check(self, env):
        """Perform health check on environment"""
        env_config = self.environments[env]
        
        # Check service status
        if not self.check_service_status(env_config):
            return False
        
        # Check application endpoints
        if not self.check_application_health(env_config):
            return False
        
        return True
    
    def smoke_tests(self, env):
        """Run smoke tests against environment"""
        env_config = self.environments[env]
        
        # Run basic functionality tests
        test_results = self.run_basic_tests(env_config)
        
        return all(test['passed'] for test in test_results)
```

### Release Management System

**Automated Release Pipeline**:

```python
# File: scripts/release_manager.py

import semver
import subprocess
import json
from datetime import datetime
from pathlib import Path

class ReleaseManager:
    """Comprehensive release management system"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.config = self.load_release_config()
        self.changelog_path = self.project_path / "CHANGELOG.md"
    
    def create_release(self, version_type="patch", pre_release=False):
        """Create a new release with automated versioning"""
        current_version = self.get_current_version()
        new_version = self.bump_version(current_version, version_type, pre_release)
        
        print(f"Creating release {new_version}")
        
        # 1. Update version in configuration files
        self.update_version_files(new_version)
        
        # 2. Update changelog
        self.update_changelog(new_version)
        
        # 3. Run pre-release checks
        if not self.pre_release_checks():
            print("Pre-release checks failed, aborting release")
            return False
        
        # 4. Create git tag
        self.create_git_tag(new_version)
        
        # 5. Build release artifacts
        artifacts = self.build_release_artifacts(new_version)
        
        # 6. Create release notes
        release_notes = self.generate_release_notes(new_version)
        
        # 7. Create platform releases
        self.create_platform_releases(new_version, artifacts, release_notes)
        
        # 8. Update distribution channels
        self.update_distribution_channels(new_version, artifacts)
        
        print(f"Release {new_version} created successfully")
        return True
    
    def bump_version(self, current, version_type, pre_release=False):
        """Bump version according to semantic versioning"""
        if version_type == "major":
            new_version = semver.bump_major(current)
        elif version_type == "minor":
            new_version = semver.bump_minor(current)
        elif version_type == "patch":
            new_version = semver.bump_patch(current)
        else:
            raise ValueError(f"Invalid version type: {version_type}")
        
        if pre_release:
            new_version = f"{new_version}-beta.{self.get_beta_number(new_version)}"
        
        return new_version
    
    def update_version_files(self, version):
        """Update version in all relevant files"""
        version_files = [
            ("game/options.rpy", f'define build.version = "{version}"'),
            ("setup.py", f'version="{version}"'),
            ("package.json", f'"version": "{version}"')
        ]
        
        for file_path, version_line in version_files:
            full_path = self.project_path / file_path
            if full_path.exists():
                self.update_version_in_file(full_path, version_line)
    
    def update_changelog(self, version):
        """Update changelog with new version"""
        if not self.changelog_path.exists():
            self.create_initial_changelog()
        
        # Get changes since last release
        changes = self.get_changes_since_last_release()
        
        # Update changelog
        new_entry = self.format_changelog_entry(version, changes)
        self.prepend_to_changelog(new_entry)
    
    def pre_release_checks(self):
        """Run comprehensive pre-release checks"""
        checks = [
            ("lint_check", self.run_lint_check),
            ("test_suite", self.run_test_suite),
            ("security_scan", self.run_security_scan),
            ("performance_check", self.run_performance_check),
            ("compatibility_check", self.run_compatibility_check)
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"Running {check_name}...")
            if not check_func():
                print(f"❌ {check_name} failed")
                all_passed = False
            else:
                print(f"✅ {check_name} passed")
        
        return all_passed
    
    def build_release_artifacts(self, version):
        """Build all release artifacts"""
        print("Building release artifacts...")
        
        # Run build script with production profile
        result = subprocess.run([
            "python", "scripts/build.py",
            "--profile", "production",
            "--version", version,
            "--platforms", "windows", "linux", "mac"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Build failed: {result.stderr}")
            return None
        
        # Collect built artifacts
        artifacts = {
            "windows": list(Path("dist").glob(f"*{version}*win*")),
            "linux": list(Path("dist").glob(f"*{version}*linux*")),
            "mac": list(Path("dist").glob(f"*{version}*mac*"))
        }
        
        return artifacts
    
    def generate_release_notes(self, version):
        """Generate comprehensive release notes"""
        # Get changes from changelog
        changelog_content = self.get_changelog_for_version(version)
        
        # Get commit messages since last release
        commits = self.get_commits_since_last_release()
        
        # Generate structured release notes
        release_notes = f"""
# Release {version}

Released on {datetime.now().strftime('%B %d, %Y')}

## Changes

{changelog_content}

## Technical Details

- Framework Version: {self.get_framework_version()}
- Ren'Py Version: {self.get_renpy_version()}
- Build Date: {datetime.now().isoformat()}
- Supported Platforms: Windows, macOS, Linux

## Download Links

- [Windows](./download/windows)
- [macOS](./download/mac)
- [Linux](./download/linux)

## Known Issues

{self.get_known_issues()}

## Installation Instructions

{self.get_installation_instructions()}
"""
        
        return release_notes
    
    def create_platform_releases(self, version, artifacts, release_notes):
        """Create releases on various platforms"""
        platforms = {
            "github": self.create_github_release,
            "gitlab": self.create_gitlab_release,
            "steam": self.create_steam_release,
            "itch": self.create_itch_release
        }
        
        for platform_name, create_func in platforms.items():
            if self.config.get(f"enable_{platform_name}", False):
                try:
                    create_func(version, artifacts, release_notes)
                    print(f"✅ Created {platform_name} release")
                except Exception as e:
                    print(f"❌ Failed to create {platform_name} release: {e}")
```

### Advanced Monitoring and Analytics

**Production Monitoring System**:

```python
# File: game/systems/monitoring.rpy

init python:
    import json
    import time
    import threading
    from datetime import datetime
    
    class ProductionMonitor:
        """Production monitoring and analytics system"""
        
        def __init__(self):
            self.metrics = {
                "performance": [],
                "errors": [],
                "user_actions": [],
                "system_info": {}
            }
            self.monitoring_enabled = persistent.analytics_enabled
            self.last_heartbeat = time.time()
        
        def initialize(self):
            """Initialize monitoring system"""
            if not self.monitoring_enabled:
                return
            
            # Collect system information
            self.collect_system_info()
            
            # Start performance monitoring
            self.start_performance_monitoring()
            
            # Register error handlers
            self.register_error_handlers()
        
        def collect_system_info(self):
            """Collect system information for analytics"""
            import platform
            import sys
            
            self.metrics["system_info"] = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": sys.version,
                "renpy_version": renpy.version(),
                "screen_resolution": f"{config.screen_width}x{config.screen_height}",
                "renderer": renpy.get_renderer_info(),
                "game_version": config.version,
                "session_start": datetime.now().isoformat()
            }
        
        def start_performance_monitoring(self):
            """Start performance monitoring thread"""
            def monitor_performance():
                while self.monitoring_enabled:
                    try:
                        fps = renpy.get_fps()
                        memory = self.get_memory_usage()
                        
                        self.metrics["performance"].append({
                            "timestamp": time.time(),
                            "fps": fps,
                            "memory_mb": memory,
                            "current_screen": renpy.get_screen()
                        })
                        
                        # Keep only recent metrics
                        if len(self.metrics["performance"]) > 1000:
                            self.metrics["performance"] = self.metrics["performance"][-500:]
                        
                        time.sleep(5)  # Monitor every 5 seconds
                        
                    except Exception as e:
                        self.log_error("performance_monitor", str(e))
                        break
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=monitor_performance, daemon=True)
            monitor_thread.start()
        
        def register_error_handlers(self):
            """Register global error handlers"""
            def error_handler(exception):
                self.log_error("unhandled_exception", str(exception))
            
            # This would need to integrate with Ren'Py's error handling
            # Implementation depends on specific error handling mechanisms
        
        def log_error(self, error_type, error_message, context=None):
            """Log error with context information"""
            error_entry = {
                "timestamp": time.time(),
                "type": error_type,
                "message": error_message,
                "context": context or {},
                "current_screen": getattr(renpy, 'get_screen', lambda: 'unknown')(),
                "game_state": self.get_game_state_snapshot()
            }
            
            self.metrics["errors"].append(error_entry)
            
            # Also log to console for debugging
            print(f"[ERROR] {error_type}: {error_message}")
        
        def track_user_action(self, action_type, action_data=None):
            """Track user action for analytics"""
            if not self.monitoring_enabled:
                return
            
            action_entry = {
                "timestamp": time.time(),
                "type": action_type,
                "data": action_data or {},
                "session_time": time.time() - self.last_heartbeat
            }
            
            self.metrics["user_actions"].append(action_entry)
        
        def get_memory_usage(self):
            """Get current memory usage in MB"""
            try:
                import psutil
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            except ImportError:
                # Fallback if psutil not available
                return 0
        
        def get_game_state_snapshot(self):
            """Get snapshot of current game state"""
            return {
                "current_room": getattr(store, 'current_room_id', 'unknown'),
                "player_progress": getattr(store, 'player_progress', {}),
                "session_duration": time.time() - self.last_heartbeat
            }
        
        def send_analytics(self):
            """Send analytics data to remote service"""
            if not self.monitoring_enabled or not config.analytics_endpoint:
                return
            
            try:
                # Prepare analytics payload
                payload = {
                    "game_id": config.game_id,
                    "version": config.version,
                    "session_id": persistent.session_id,
                    "metrics": self.metrics,
                    "timestamp": time.time()
                }
                
                # Send to analytics service
                # Implementation would depend on chosen analytics service
                self.send_to_analytics_service(payload)
                
            except Exception as e:
                print(f"Analytics upload failed: {e}")
        
        def generate_local_report(self):
            """Generate local analytics report"""
            report = {
                "summary": {
                    "session_duration": time.time() - self.last_heartbeat,
                    "total_errors": len(self.metrics["errors"]),
                    "total_actions": len(self.metrics["user_actions"]),
                    "average_fps": self.calculate_average_fps(),
                    "peak_memory": self.calculate_peak_memory()
                },
                "detailed_metrics": self.metrics
            }
            
            # Save report locally
            report_path = Path("analytics_report.json")
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            
            return report
    
    # Initialize global monitor
    production_monitor = ProductionMonitor()
```

---

## Recommended Learning Path

### Phase 1: Basic Build Setup
- [ ] Set up development environment with proper SDK paths
- [ ] Configure basic build profiles for different deployment scenarios
- [ ] Implement automated linting and basic quality checks
- [ ] Create simple build scripts for local development

### Phase 2: Advanced Build Configuration
- [ ] Implement comprehensive testing suite with asset validation
- [ ] Set up multi-platform build automation
- [ ] Configure continuous integration pipelines
- [ ] Implement asset optimization and performance monitoring

### Phase 3: Professional Deployment
- [ ] Set up blue-green deployment strategies
- [ ] Implement automated release management
- [ ] Configure platform-specific signing and distribution
- [ ] Set up production monitoring and analytics

### Phase 4: Enterprise Operations
- [ ] Implement advanced security measures and code protection
- [ ] Set up comprehensive disaster recovery procedures
- [ ] Develop advanced performance optimization strategies
- [ ] Create enterprise-grade monitoring and alerting systems

---

## Next Steps

Having mastered the build and distribution system, you now have the tools to professionally deploy and maintain Snatchernauts Framework games across multiple platforms. The next chapters will provide detailed API references and advanced development techniques:

- **Chapter 10: API Reference - Room System** - Complete technical reference for room management APIs
- **Chapter 11: API Reference - Interaction System** - Detailed interaction and logic hook APIs
- **Chapter 12: API Reference - Display System** - Visual effects and UI management APIs
- **Chapter 13: API Reference - UI System** - Screen and interface component APIs
- **Chapter 14: Developer Manual** - Advanced development techniques and framework customization
- **Chapter 15: Troubleshooting Guide** - Comprehensive problem-solving and optimization strategies

The build and distribution system provides a complete, professional-grade workflow that scales from indie development to enterprise deployment, ensuring your games reach players reliably across all platforms.

---

**Continue to:** [Chapter 10: API Reference - Room System](10-API-Room)

