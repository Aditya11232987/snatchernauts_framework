<!-- Ready-to-paste into itch.io page description. Replace image URLs in {{ ... }} after uploading to itch.io. -->

<p align="center">
  <img src="{{BANNER_URL}}" alt="Snatchernauts Framework" style="max-width: 900px; width: 100%; height: auto; image-rendering: -webkit-optimize-contrast;" />
</p>

<h2 align="center" style="margin:0; padding:0; font-family: monospace; font-size: 14px; letter-spacing: 0.5px;">Retro‑cinematic, interactive visual novels — powered by Ren'Py 8.4</h2>

<p align="center" style="margin: 8px 0 0;">
  <!-- Upload marketing/itchio/snatchernauts-overview.gif and paste its hosted URL below -->
  <img src="{{OVERVIEW_GIF_URL}}" alt="Animated overview of room exploration, context menu, and CRT/bloom effects" style="max-width: 900px; width: 100%; height: auto; image-rendering: -webkit-optimize-contrast; border-radius: 3px;" />
</p>

<hr/>

<h3>What is Snatchernauts?</h3>
<p>
Snatchernauts is a modern Ren'Py 8.4.x framework for interactive point‑and‑click exploration that brings the energy of Kojima‑era classics — <i>Snatcher</i>, <i>Policenauts</i> — to contemporary visual novels. It focuses on tactile room interaction, contextual action menus, and tasteful CRT/Bloom overlays — all driven by a clean API and centralized gameplay hooks.
</p>

<ul>
  <li>🎯 Pixel‑accurate hotspots — click only where the image is opaque</li>
  <li>🧭 Keyboard/gamepad navigation across in‑room objects</li>
  <li>🗂️ Contextual menus — Examine, Use, Talk, custom actions</li>
  <li>🧩 Centralized lifecycle hooks for gameplay logic</li>
  <li>🕶️ CRT, bloom, and letterbox effects for retro‑cinematic feel</li>
  <li>🧰 Clean helper APIs: room, ui, interactions, display</li>
</ul>

<h3>Screenshots</h3>
<p>
  <!-- Upload these from Wiki/screenshots/ then paste their hosted URLs below -->
  <img src="https://img.itch.zone/aW1hZ2UvMzc5MzY3My8yMjcwODEzMi5wbmc=/original/ZaVU34.png
  " alt="Room exploration (shot1.png)" style="max-width: 100%; height: auto;" />
</p>
<p>
  <img src="https://img.itch.zone/aW1hZ2UvMzc5MzY3My8yMjcwODEzMy5wbmc=/original/8BOTeL.png" alt="Action menu and overlays (shot2.png)" style="max-width: 100%; height: auto;" />
</p>
<p>
  <img src="https://img.itch.zone/aW1hZ2UvMzc5MzY3My8yMjcwODEzMS5wbmc=/original/rY7TZU.png" alt="CRT/Bloom effects (shot3.png)" style="max-width: 100%; height: auto;" />
</p>
<p>
  <img src="https://img.itch.zone/aW1hZ2UvMzc5MzY3My8yMjcwODEzNC5wbmc=/original/Ov7j05.png" alt="Contextual interactions (shot4.png)" style="max-width: 100%; height: auto;" />
</p>

<h3>Who is this for?</h3>
<p>
Developers who want their visual novels to feel more tactile and exploratory without fighting their UI. If you like the aesthetic and interaction of classic adventure games and want it in a modern Ren'Py workflow, this is for you.
</p>

<h3>How it works</h3>
<ul>
  <li>Coordinator: <code>game/script.rpy</code> boots overlays and enters the exploration loop</li>
  <li>Public APIs: <code>game/api/*.rpy</code> for rooms, display/effects, UI, interactions</li>
  <li>Logic Layer: write hooks in <code>game/logic/game_logic.rpy</code> (plus optional per‑room handlers)</li>
  <li>UI Layer: screens in <code>game/ui/</code> compose descriptions, menus, overlays</li>
  <li>Effects: <code>game/shaders/</code> and <code>game/overlays/</code> for CRT/Bloom/Letterbox</li>
</ul>

<h3>Quick start</h3>
<ol>
  <li>Install Ren'Py 8.4.x and set your SDK path (e.g. <code>RENPY_SDK=~/renpy-8.4.1-sdk</code>).</li>
  <li>Run the project: <code>$RENPY_SDK/renpy.sh .</code></li>
  <li>Optional lint: <code>make lint</code> or <code>$RENPY_SDK/renpy.sh . lint</code></li>
  <li>Build via Ren’Py Launcher → Build &amp; Distribute.</li>
</ol>

<h3>Controls</h3>
<ul>
  <li>A/Enter/Space — interact (open action menu)</li>
  <li>Arrow keys / WASD — navigate objects</li>
  <li>Esc/B — cancel</li>
  <li>Mouse — hover/click objects</li>
</ul>

<h3>Open source</h3>
<p>
MIT licensed. See repository for details.
</p>

<hr/>

<h3>Notes for itch.io</h3>
<ul>
  <li>Upload images (banner/logo, screenshots) to this page and copy their hosted URLs into the placeholders above.</li>
  <li>If your account has Custom CSS enabled, you can paste theme.css (from this repo) into the Theme editor for a compact, monospace look matching the project’s style.</li>
</ul>

