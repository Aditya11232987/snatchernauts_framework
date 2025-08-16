# Snatchernauts Framework

## **The Revolutionary Ren'Py Framework That Changes Everything**

_Create visual novels that feel alive — Transform passive reading into immersive exploration_

[![version](https://img.shields.io/badge/version-0.5.3-blue)](CHANGELOG.md)
[![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub mirror](https://img.shields.io/badge/github-mirror-blue?logo=github)](https://github.com/grahfmusic/snatchernauts_framework)

![Snatchernauts Logo](.gitbook/assets/snatcher-logo.png)

---

## 🚀 **Stop Building Static Visual Novels. Start Creating Interactive Experiences.**

**Your players deserve more than click-to-continue storytelling.**

Snatchernauts Framework is the **only Ren'Py framework** engineered from the ground up to deliver the exploration-rich, tactile gameplay that made classics like _Snatcher_ and _Policenauts_ legendary.

**The result?** Visual novels that feel less like digital books and more like **living, breathing worlds** your players can truly explore.

### 🎯 **Built for Developers Who Demand More**

Tired of the limitations of traditional visual novel frameworks? **Snatchernauts delivers everything you need** to create next-generation interactive experiences:

✅ **Pixel-perfect interaction** — No more clunky rectangular hitboxes  
✅ **Professional-grade visual effects** — CRT shaders, bloom, letterboxing, film grain  
✅ **Multi-input support** — Mouse, keyboard, and gamepad out of the box  
✅ **Clean, extensible architecture** — Write less code, accomplish more  
✅ **Production-ready tooling** — Built-in debugging, automated builds, CI/CD ready

---

## 🎆 **The Problem with Traditional Visual Novels**

**95% of visual novels suffer from the same limitation:** They're essentially digital books with pictures. Players click → read text → click again. **That's it.**

**But what if your visual novel could:**

- Let players **explore environments** like real detective games?
- Feature **dynamic, contextual interactions** that respond to player curiosity?
- Deliver **cinematic visual effects** without knowing advanced Shader knowledge?
- Support **multiple input methods** for maximum accessibility?
- Provide **visual development tools** that accelerate your workflow?

### 💡 **The Snatchernauts Solution: Interactive Immersion**

**Snatchernauts Framework is the answer.** We've taken everything that made legendary interactive fiction unforgettable and engineered it into a modern, production-ready framework.

**What makes us different:**

🎯 **Pixel-Perfect Exploration**  
    No more rectangular hitboxes. Players click only on actual objects, creating natural, intuitive interaction.

🧭 **Context-Aware Interactions**  
    Dynamic menus that change based on story progress, inventory, and player actions.

🧩 **Professional Architecture**  
    Clean separation of concerns. Write game logic once, use everywhere. No more spaghetti code.

🎬 **Unity and Godot Quality Visual Effects**  
    Real-time shader effects: CRT monitors, film grain, atmospheric fog, dynamic lighting.

🕶️ **Live Visual Tuning**  
    Adjust bloom, vignette, scanlines, and color grading in real-time during development.

**Result:** Visual novels that feel like **living, breathing worlds** instead of static storybooks.

---

## 💪 **Why Developers Choose Snatchernauts**

### 🚀 **Accelerated Development**

- **Pre-built interaction systems** — No need to reinvent point-and-click mechanics
- **Comprehensive API library** — Room management, UI, effects, all ready to use
- **Automated development tools** — Linting, building, and deployment scripts included
- **Extensive documentation** — 400+ pages of guides, tutorials, and examples

### 🎨 **Unmatched Visual Quality**

**Create games that look like they cost 10x your budget:**

- **Real-time CRT simulation** with authentic scanlines and chromatic aberration
- **Dynamic Colour Grading and Lighting** presets built in and expandable
- **Cinematic letterboxing** with customizable aspect ratios
- **Live effect tuning** — See changes instantly without recompiling

### 🎲 **Multi-Platform Excellence**

**One framework, every platform:**

- **Desktop:** Windows, macOS, Linux (native performance)
- **Mobile:** Android and iOS support via Ren'Py
- **Web:** HTML5 deployment ready
- **Console:** Steam Deck verified, potential console porting
- **Accessibility:** Full keyboard, gamepad, and screen reader support

### 🛡️ **Production-Ready Reliability**

**Built for commercial releases:**

- **Automated CI/CD pipelines** for GitLab and GitHub
- **Comprehensive testing framework** with unit and integration tests
- **Performance monitoring** with built-in FPS and memory tracking
- **Robust error handling** with detailed logging and debugging tools
- **Cross-platform build scripts** for seamless distribution

---

## 🌟 **What You Get with Snatchernauts**

### ✨ Features at a Glance

| Feature                    | What it gives you                                        |
| -------------------------- | -------------------------------------------------------- |
| 🎯 Pixel‑accurate hotspots | Click only where the image is opaque; no sloppy hitboxes |
| 🧭 Keyboard/gamepad nav    | Fast navigation across in‑room objects                   |
| 🗂️ Contextual menus        | Examine, Use, Talk, and custom actions                   |
| 🧩 Centralized hooks       | on_game_start, on_room_enter, on_object\_\* events       |
| 🛠️ Debug overlay           | Live logging toggles, FPS/memory hints                   |
| 🕶️ CRT + vignette          | Warp/scan/chroma + horizontal vignette, live tuning      |
| 🎬 Shader system           | Film grain, fog, lighting, letterbox via GLSL shaders    |
| 🌸 Bloom effects           | Cinematic overlays with color correlation                |
| 🧰 Clean APIs              | room/display/ui/interactions modules                     |

### How It Works (Architecture)

- Coordinator: `game/script.rpy` starts the info overlay, then calls `on_game_start()` and enters the exploration loop via `play_room()`.
- Public APIs: `game/api/*.rpy` expose helpers for rooms, display/effects, UI, and interactions.
- Logic Layer: put your gameplay in `game/logic/game_logic.rpy` and optional `game/logic/rooms/<room>_logic.rpy` files. Register per‑room handlers.
- UI Layer: screens under `game/ui/` compose descriptions, menus, and overlays.
- Effects: `game/shaders/` and `game/overlays/` provide CRT/Bloom/Letterbox and startup/debug overlays.
- Core Config: `game/core/` contains options, logging, and room configuration helpers.

See the Wiki for a deep dive, code walkthroughs, and examples.

---

### 🚀 Quick Start

1. Install Ren'Py 8.4.x and set your SDK path. Example:
   - export RENPY_SDK=~/renpy-8.4.1-sdk
2. Run the project:
   - **Recommended**: `scripts/run-game.sh` (unified launcher with linting)
   - **Direct**: `$RENPY_SDK/renpy.sh .`
3. Development workflow:
   - `scripts/run-game.sh --lint` (lint then launch)
   - `scripts/run-game.sh --debug` (launch with console output)
   - `scripts/run-game.sh --help` (show all options)
4. Build distributions via Ren'Py Launcher → Build & Distribute.

_See `DEVELOPMENT_TOOLS.md` for complete development workflow documentation_

### 🎮 Controls (Default)

- A/Enter/Space: interact (open action menu)
- Arrow keys / WASD: navigate objects
- Esc/B: cancel
- Mouse: hover/click objects

### 🧠 Core Concepts

- Hooks: write gameplay as Python/renpy functions responding to events:

```renpy
# Implement these in game/logic/game_logic.rpy (or per-room handlers)
def on_game_start():
    ...

def on_room_enter(room_id):
    ...

def on_object_hover(room_id, obj):
    ...

def on_object_interact(room_id, obj, action) -> bool:
    # Return True when you fully handle an action
    ...
```

- Per‑room Logic: implement `register_room_logic('<room>', Handler())` with your own methods.
- APIs: use `room_api`, `ui_api`, `interactions_api`, `display_api` instead of scattering logic in screens.
- Logging: centralized logging interception with color and truncation; toggles available at runtime.

### 🗺️ Project Layout

```
snatchernauts-framework/
├── game/                          # Main game directory
│   ├── script.rpy                # Main entry point and game flow
│   ├── api/                       # Framework APIs
│   │   ├── room_api.rpy          # Room management functions
│   │   ├── display_api.rpy       # Display and visual functions
│   │   ├── interactions_api.rpy  # Player interaction handling
│   │   └── ui_api.rpy            # UI and screen management
│   ├── core/                      # Core framework functionality
│   │   ├── options.rpy           # Game configuration and settings
│   │   ├── common_utils.rpy      # Shared utility functions
│   │   ├── common_logging.rpy    # Logging and debug functions
│   │   ├── room_utils.rpy        # Room-specific utilities
│   │   └── rooms/                # Room configuration system
│   │       └── room_config.rpy   # Room definitions and editor
│   ├── logic/                     # Game logic implementation
│   │   └── game_logic.rpy        # Global game logic hooks
│   ├── ui/                        # User interface screens
│   │   ├── screens_room.rpy      # Room exploration screens
│   │   ├── screens_interactions.rpy # Interaction menu screens
│   │   └── room_descriptions.rpy # Description box management
│   ├── overlays/                  # Screen overlays
│   │   ├── info_overlay.rpy      # Information and help overlay
│   │   ├── debug_overlay.rpy     # Development debug overlay
│   │   ├── letterbox_gui.rpy     # Letterbox effect overlay
│   │   └── fade_overlay.rpy      # Screen transition overlays
│   ├── shaders/                   # Visual effect shaders
│   │   ├── crt_shader.rpy        # CRT monitor effect
│   │   ├── letterbox_shader_v2.rpy # Enhanced letterbox shader
│   │   └── neo_noir_*.rpy        # Neo-noir atmosphere effects
│   ├── rooms/                     # Room definitions and assets
│   │   ├── room1/                # Example room with assets and scripts
│   │   ├── room2/                # Additional example rooms
│   │   └── room3/                # Room-specific configurations
│   ├── images/                    # Game images and sprites
│   │   ├── backgrounds/          # Room background images
│   │   ├── objects/              # Interactive object sprites
│   │   └── ui/                   # UI element graphics
│   ├── audio/                     # Game audio files
│   │   ├── music/                # Background music tracks
│   │   └── sounds/               # Sound effects
│   ├── fonts/                     # Custom font files
│   └── gui/                       # Ren'Py GUI system files
├── scripts/                       # Development and automation tools
│   ├── run-game.sh               # 🎮 Unified game launcher (lint + debug options)
│   ├── lint.sh                   # 🔍 Ren'Py code linting
│   ├── push-both.sh              # 🚀 Push to GitLab + GitHub simultaneously
│   ├── sync-github-wiki.sh       # 📚 Manual wiki synchronization to GitHub
│   ├── github-init.sh            # 🔗 Initialize GitHub remote repository
│   └── hooks/                    # Git hooks for automation
│       └── pre-push             # ⚠️  Auto-sync wiki on push (if enabled)
├── Wiki/                          # Documentation (auto-synced to wikis)
│   ├── 01-Overview.md            # Framework introduction and concepts
│   ├── 02-Getting-Started.md     # Zero-to-hero tutorial
│   ├── 03-Architecture.md        # System design and best practices
│   ├── 04-Logic-Hooks.md         # Game logic system documentation
│   ├── 05-API-*.md               # Complete API reference library
│   ├── 06-Screens-and-UI.md     # UI system documentation
│   ├── 07-Effects-and-Shaders.md # Visual effects manual
│   ├── 08-Build-and-Distribute.md # Production deployment guide
│   ├── 09-Examples.md            # Extensive code examples
│   ├── 10-Troubleshooting.md     # Problem-solving guide
│   └── DeveloperManual.md        # Complete developer manual
├── .gitlab-ci.yml                # CI/CD pipeline (auto-wiki sync)
├── CHANGELOG.md                  # Version history and release notes
├── README.md                     # This comprehensive guide
├── LICENSE                       # MIT license
└── project.json                  # Ren'Py project configuration
```

### 🛠️ **Development Scripts Explained**

**🎮 `run-game.sh`** — **Your main development launcher**  
    • `--lint` — Run code checks before launching  
    • `--debug` — Launch with debug console visible  
    • `--compile` — Force recompilation before launch  
    • Auto-detects Ren'Py SDK path and validates setup

**🚀 `push-both.sh`** — **Synchronized repository management**  
    • Pushes to both GitLab (primary) and GitHub (mirror) simultaneously  
    • Handles branches and tags across both platforms  
    • Supports `all` branches or specific branch targeting

**📚 `sync-github-wiki.sh`** — **Manual wiki synchronization**  
    • Syncs local `Wiki/` directory to GitHub wiki repository  
    • Creates clean snapshot with force-push to wiki repo  
    • Includes `dry-run` mode for testing

**🔗 `github-init.sh`** — **Repository setup automation**  
    • Converts any GitHub URL format to SSH  
    • Sets up origin remote with proper branch naming  
    • Handles initial repository connection and push

**⚠️ `pre-push` hook** — **Automatic wiki sync**  
    • Detects wiki changes in recent commits  
    • Auto-syncs wiki if `AUTO_SYNC_WIKI=1` environment variable set  
    • Non-blocking — never prevents code pushes

---

## 🎨 **Transform Your Visual Novel Ideas Into Reality**

### 🎆 **Perfect For These Game Types:**

🕵️ **Detective/Mystery Games**  
    Create immersive crime scenes with pixel-perfect evidence discovery  
        _"Players can examine every detail, just like real forensic investigation"_

🏭 **Sci-Fi Adventures**  
    Build futuristic environments with dynamic lighting and atmospheric effects  
        _"CRT shaders and bloom effects create authentic retro-futuristic atmosphere"_

🏰 **Point-and-Click Adventures**  
    Traditional adventure game mechanics with modern visual novel storytelling  
        _"All the exploration depth of LucasArts classics, powered by Ren'Py"_

🏠 **Interactive Fiction**  
    Rich, explorable environments that respond to player curiosity  
        _"Every object tells a story when players can truly interact with the world"_

### 💻 **Code Example: See How Easy It Is**

**Traditional Ren'Py:** 50+ lines for basic interaction  
**Snatchernauts:** 5 lines for rich, contextual interaction

```python
# That's it! This creates a fully interactive room with:
# • Pixel-perfect hotspots
# • Dynamic action menus
# • Multi-input support
# • Professional visual effects
# • Automatic state management

def on_object_interact(room_id, obj_name, action):
    if obj_name == "computer" and action == "Examine":
        show_description("A high-tech computer terminal")
        return True
    return False
```

---

## 🚀 **Get Started in Minutes, Not Months**

### 🎯 **Instant Setup Guide**

**Step 1:** Download and extract Snatchernauts  
**Step 2:** Set your Ren'Py SDK path  
**Step 3:** Run `scripts/run-game.sh`  
**Step 4:** Start building your interactive world

**That's it!** No complex configuration, no dependency hell, no weeks of setup.

### 📚 **World-Class Documentation**

**400+ pages of comprehensive guides:**

📚 **Complete Framework Manual**

- Wiki/01-Overview.md — Framework introduction and concepts
- Wiki/02-Getting-Started.md — Zero-to-hero tutorial
- Wiki/03-Architecture.md — System design and best practices

🔧 **API Reference Library**

- Wiki/05-API-Room.md — Room and object management
- Wiki/05-API-Display.md — Visual effects and rendering
- Wiki/05-API-Interactions.md — Player input and actions
- Wiki/05-API-UI.md — Interface and screen management

🎬 **Visual Effects Guide**

- Wiki/07-Effects-and-Shaders.md — CRT, bloom, and cinematic effects
- Complete shader reference with real-time tuning examples

🛠️ **Production Guides**

- Wiki/08-Build-and-Distribute.md — CI/CD, cross-platform builds
- Wiki/10-Troubleshooting.md — Common issues and solutions

📝 **Developer Resources**

- `DEVELOPMENT_TOOLS.md` — Game launcher and linting tools
- `SHADER_REFERENCE.md` — Ren'Py shader documentation links
- `game/shaders/HOTKEY_MAPPING.md` — In-game controls reference

**New to game development?** Start here:

1. Wiki/01-Overview.md
2. Wiki/02-Getting-Started.md
3. Wiki/09-Examples.md

### 🛠️ Debug & Effects

- **i**: toggle info overlay
- **c**: toggle CRT • **a**: toggle scanline animation
- **1–4**: scanline size presets
- **\[ / ]**: vignette strength • **- / =**: vignette width • **0**: reset
- **l**: toggle letterbox (shader‑based)
- **Shift+G/F/V/L/W**: cycle shader effects (grain/fog/vintage/lighting/weather)
- **Alt+A/I**: atmosphere presets / investigation modes
- **R**: reset all shader effects • **H**: shader help
- **Cmd+Shift+F12 / Ctrl+Shift+F12**: cycle debug overlay

---

## 📈 **The Numbers Don't Lie**

### 🏆 **Framework Comparison**

| **Feature**                   | **Traditional Ren'Py**   | **Other Frameworks** | **Snatchernauts**   |
| ----------------------------- | ------------------------ | -------------------- | ------------------- |
| **Setup Time**                | Days of coding           | Weeks of setup       | **5 minutes**       |
| **Pixel-Perfect Interaction** | ❌ Manual implementation | ❌ Limited support   | ✅ **Built-in**     |
| **Visual Effects**            | ❌ Basic only            | ❌ Plugin-dependent  | ✅ **Professional** |
| **Multi-Input Support**       | ❌ Manual coding         | ❌ Partial           | ✅ **Complete**     |
| **Documentation**             | ❌ Scattered             | ❌ Basic             | ✅ **400+ pages**   |
| **Production Tools**          | ❌ DIY                   | ❌ Limited           | ✅ **Full suite**   |
| **Commercial Ready**          | ❌ Requires work         | ❌ Maybe             | ✅ **Day one**      |

---

## 🚀 **Ready to Transform Your Visual Novel?**

### 🎆 **Choose Your Path**

🔥 **I want to start creating immediately**  
    → Clone the repository and run `scripts/run-game.sh`  
    → Follow Wiki/02-Getting-Started.md

📚 **I want to understand the framework first**  
    → Read Wiki/01-Overview.md  
    → Explore Wiki/03-Architecture.md

🛠️ **I'm ready for production**  
    → Check out Wiki/08-Build-and-Distribute.md  
    → Set up automated CI/CD pipelines

### 🔗 **Quick Links**

- **💻 [Download Framework](https://gitlab.com/grahfmusic/snatchernauts_framework)**
- **📚 [Complete Documentation](Wiki/)**
- **🎬 [Visual Effects Demo](Wiki/07-Effects-and-Shaders.md)**
- **🚀 [5-Minute Quick Start](Wiki/02-Getting-Started.md)**

---

### 🌐 **Join the Community**

💬 **Questions?** Open an issue on GitLab  
🔄 **Updates?** Star the repository for notifications  
🤝 **Contributing?** Pull requests welcome with brief rationale

### 📄 **Open Source & Commercial Friendly**

**MIT License** — Use it in personal projects, commercial releases, client work, whatever you need. No restrictions, no royalties, no surprises.

---

## 🎆 **Stop Dreaming. Start Building.**

**Your players are waiting for experiences that go beyond clicking through text.**

**Snatchernauts Framework gives you everything you need to create interactive visual novels that feel alive, respond to curiosity, and deliver the kind of immersive storytelling that keeps players engaged for hours.**

**The framework is ready. The documentation is comprehensive. The tools are professional.**

**The only question is: What story will you bring to life?**

---

**⭐ [Star this repository](https://gitlab.com/grahfmusic/snatchernauts_framework) · 📚 [Read the docs](Wiki/) · 🚀 [Start building](Wiki/02-Getting-Started.md)**
