# Mac setup handoff for a fresh chat

Use this note as project context. The user can now open/control the Mac, so continue with live verification rather than treating this as code-only work. Start by reading current files and observing the Mac; some settings below are written to disk but have not been confirmed live. Do not re-ask settled preferences unless live behavior proves they conflict.

## User's goal

Build a personal macOS setup inspired by Linkarzu's dotfiles, while using **KiwiDesk instead of Yabai** and retaining the user's own workflow. Do not copy the whole Linkarzu repository: it contains many unrelated and machine-specific configs. The local reference repo is:

`/Users/yash/Downloads/Dotfiles/dotfiles-latest-learn-`

Current project/workspace:

`/Users/yash/.config`

## Decisions already made

### Window management and spaces

- Four macOS desktops/profiles: **Study, Browse, Create, Personal**.
- Four KiwiDesk spaces in each profile; the four saved profile configs currently start every KiwiDesk space in **Monocle**.
- User switches spaces with keys and changes the layout manually. Layout cycling is **Control + comma** / **Control + period**. Layout choices discussed: Stack, BSP, Grid, Track, Scrolling, Monocle. The chosen layout should persist until changed.
- App assignments are profile-specific. See `KiwiDesk/profiles/{Study,Browse,Create,Personal}.json`.
- Saved gaps: 48 px top, 8 px on the other edges, and 8 px inner horizontal/vertical gaps.
- Current `KiwiDesk/gui.json` has float rules for Finder, Calculator, Archive Utility, and System Settings; `float_placement` is `keep` in the four profiles. Do not assume windows will be centered by the manager.
- Important discovered mismatch: `KiwiDesk/gui.json` still has Option+5/6/7 bindings to macOS desktops 5–7 even though the agreed plan was four desktops. Review and correct if the user confirms these are unwanted; inspect live Mission Control before deleting/rewriting anything.
- Root/global `app_rules` is empty on purpose; routes are saved per profile.

### Keyboard workflow

- Right Option is intended to act as the held shortcut layer, implemented in Karabiner. Current generated rule is in `karabiner/karabiner.json`; actual behavior was not verified in the prior session.
- Karabiner-Elements is the active Right Option shortcut mapper; Right Option+O was verified live on 2026-11-16.
- Shortcut catalog: `workflow/SHORTCUTS.md`; mappings are implemented by `workflow/action.py` and `workflow/config.json`. User expects focus/app launch behavior across desktops, and a few apps should focus an existing window before opening a new one.
- Settled examples in the catalog include Right Option+p Crest, b Phi, h Helium, y Edge, r Safari, t Kitty, o Obsidian, c VS Code, g GitHub Desktop, x Xcode, v Discord, n NaturalReader, m Spotify, f Finder, z System Settings; groups use i+number (AI), j+number (study), k+number (documents), u+number (utilities). Check actual mappings before changing.
- Layout cycle bindings are **Control + comma/period**. Existing additional KiwiDesk bindings include directional focus, maximize, float, sticky, pocket, desktop/space navigation, and some app launchers.

### SketchyBar

- User's target is a 48 px, opaque, polished bar that fully covers the native menu bar, including on hover; notch-aware.
- Apple icon temporarily reveals the native menu bar, then returns to the custom bar after about two seconds.
- Left side: Apple icon, active app icon/name, macOS desktop symbols (Book, Globe, Terminal, House; active desktop label), and only the active KiwiDesk space indicator (not all Kiwi spaces at once).
- Near the notch: song title only (Spotify; ByTune intentionally deferred) and upcoming event name/time.
- Right side: Wi-Fi with current download/upload traffic, volume with click-to-select output device, battery, date/time. CPU/GPU/RAM/SSD widgets were removed from the bar; no SSD segment.
- Four palettes in appearance UI: Tokyo Night, Rose Pine Dawn, Gruvbox Retro, Cyberpunk.
- Main files: `sketchybar/sketchybarrc`, `sketchybar/plugins/`, `sketchybar/colors.sh`, `sketchybar/icons.sh`, `appearance/`.
- Code and helper compilation were previously checked, but live behavior (menu bar hide/reveal, popovers, audio selection, calendar permission, network samples and Kiwi event updates) still needs to be checked on the Mac.

### Kitty system dashboard / btop

- Kitty is installed; `kitty/kitty.conf` uses MesloLGM Nerd Font at 14 pt and includes `kitty/current-theme.conf`.
- A custom Python dashboard exists as fallback: `kitty/system_monitor.py`.
- `kitty/open-system-monitor.sh` opens btop if `btop` is available; otherwise it launches that Python fallback.
- A Catppuccin-Mocha btop config/theme are prepared at `btop/btop.conf` and `btop/themes/Yash-Mocha.theme`.
- `btop` installation was attempted using Homebrew but failed in the prior agent environment because writes under `/opt/homebrew` and Homebrew cache/lock directories were denied. This may be a session sandbox issue; user can now open the Mac. First try `brew install btop` in a normal Terminal session. Do not recursively change Homebrew ownership or use broad `sudo chown` as a workaround without reviewing the actual `brew doctor` result.
- To open after install: `~/.config/kitty/open-system-monitor.sh`. The launcher has not been successfully opened/visually checked from the previous agent session.
- btop can show CPU, memory, disks, network and processes with graphs. Apple GPU utilization/temperature may not be available without privileged sampling; do not promise an unverified GPU percentage.

### Themes and wallpaper

- `appearance/appearance.py` and `appearance/palettes.json` provide palette switching across SketchyBar, Kitty and KiwiDesk; selected Linkarzu palette data was imported safely, not its hard-coded scripts.
- Four finished 6K wallpapers, per macOS desktop assignment, and live persistence are **not complete**. User previously wanted distinct wallpapers matching the four themes. MacOS desktops are separate from KiwiDesk spaces.

## Linkarzu Yabai comparison already established

The Yabai reference files are `yabai/yabairc`, `yabai/yabai_env.sh`, `yabai/positions/*`, `yabai/update_border_color.sh`, `yabai/yabai_restart.sh`, plus `skhd/skhdrc`.

Linkarzu's active setup includes:

- Stack as global default; selected spaces use BSP, including one mirrored BSP space.
- Space labels up to 10, a catch-all route to desk1, many app-specific routes, plus display-count-aware assignments for OBS/streaming/projector workflows.
- Per-resolution and per-display padding, 2 px window gap, 0.5 split ratio, `second_child` insertion, persistent zoom, no window animations, and Fn-modified mouse move/resize with drop-to-swap.
- Rules to leave selected apps unmanaged and put apps in below/above sublayers; normalized sublayer behavior.
- Yabai signals that update SketchyBar on focus/create/close, plus a border script that displays a green border only for BSP with multiple standard windows.
- SKHD shortcuts for directional focus/swap, moving windows across spaces/displays, and many unrelated media/OBS/session actions.

Your KiwiDesk config covers core tiling, manual layout switching, per-profile app routing, floating, sticky/pocket, directional focus, desktop/space movement, and KiwiDesk-to-bar integration. It does **not** exactly match Yabai's below/above sublayers, per-resolution display padding, mirrored BSP default, dynamic BSP borders, or all SKHD directional window swaps/cross-display actions. These are feature differences, not necessarily requirements for the user's one-screen/normal app workflow. Yabai's scratchpad examples and opacity effects in this checkout are commented/disabled, so they are not active missing features. The Kitty position helper appears inactive in this checkout because the Kitty ID assignment is commented and then tested for emptiness.

## Other current facts to retain

- `~/.config/nvim` is a symlink to `/Users/yash/Downloads/Dotfiles/dotfiles-latest-learn-/neovim/lazyvim`; `nvim` and `lazygit` are installed.
- `tmux`, `sesh`, `fastfetch`, `btop`, `zoxide`, `yazi`, and `starship` were not found on PATH in the prior audit.
- There was no `~/.zshrc` in the prior audit.
- Do not claim every Linkarzu feature is implemented. The user's current setup is a selective adaptation, with KiwiDesk replacing Yabai.

## Next session: recommended order

1. Have the user open the Mac; inspect actual active desktop count and KiwiDesk state/profile bindings. Resolve the stale Option+5/6/7 keys if they are not wanted, without changing unrelated shortcuts.
2. In a normal Terminal session, try `brew install btop`; if it fails, inspect `brew doctor`/permissions safely. Then run the Kitty launcher and visually verify btop and its theme.
3. Verify the remaining Karabiner shortcuts against `workflow/SHORTCUTS.md`.
4. Reload/inspect KiwiDesk and SketchyBar live; check app routing, all four profiles, Monocle startup, layout persistence, float behavior, bar coverage and notch placement.
5. Only after live findings, discuss optional Yabai-inspired parity features (display-adaptive gaps, dynamic BSP borders, directional swaps, sublayer rules). Do not migrate Yabai itself unless user changes the explicit KiwiDesk choice.
6. Continue wallpaper/theme assignment after the bar and window manager are stable.
