# Troubleshooting

Nothing happens on interact
- Ensure your per‑room handler returns True when you handle an action; otherwise defaults may run.

Weird colors or artifacts
- Toggle CRT off (`c`) or reset vignette controls. Some GPUs need different defaults.

Builds fail in CLI
- Use the Ren’Py Launcher for packaging; the headless CLI does not provide a `distribute` command.

Logs are noisy
- Use the debug overlay to toggle logging level/features.

