# Shared appearance

Click Style in SketchyBar for 17 palettes, the native accent picker, or a local wallpaper file picker.

Run `python3 ~/.config/appearance/appearance.py menu` to open the controls manually.
Run `python3 ~/.config/appearance/appearance.py apply catppuccin-mocha` to apply a palette.
Run `python3 ~/.config/appearance/appearance.py restore` to restore the original SketchyBar and Kitty files.

Palettes are imported as data from the local Linkarzu checkout; its scripts and hardcoded paths are not executed.

SketchyBar reloads its generated colors. New Kitty windows read the generated theme. KiwiDesk receives live IPC color changes without restarting. Keep those through KiwiDesk or ask ChatGPT to keep them. SketchyBar and Kitty file changes persist immediately; first originals are retained in originals/. Restore covers those files only, not KiwiDesk.

## Wallpaper

Switch to the intended macOS Mission Control desktop first and turn off Show on all Spaces in Wallpaper settings. The helper uses NSWorkspace on the current screen. Per-desktop persistence requires live verification on this macOS version. It cannot address inactive desktops by number. KiwiDesk internal Spaces are separate and do not have independent native wallpapers.

Compile with `swiftc ~/.config/appearance/wallpaper.swift -o ~/.config/appearance/wallpaper` if needed.

## Scope

Integrated: SketchyBar, KiwiDesk colors, Kitty. Other apps and Neovim are unchanged. Existing bar widgets and shortcuts are preserved. No wallpaper database edits, downloads, or app restarts.
