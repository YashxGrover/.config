-- Adopted by KiwiDesk on 2026-11-12.
-- The app now manages your settings, rules, and keybindings
-- itself (gui.json); the migrated lines are commented out
-- below as a backup, and recovered keybindings appear in the
-- Keybindings tab. Your custom Lua (event hooks, helpers) is
-- kept active where possible — delete the commented backup
-- once you no longer need it.
-- KiwiDesk configuration
-- Docs: https://github.com/KiwiCanopy/KiwiDesk
--
-- Everyday settings live in the Settings window;
-- this file is for optional custom Lua. Comments
-- only by default — the built-in defaults apply
-- until a line below is uncommented.

-- One value for all gaps (the built-in default):
-- KiwiDesk.set_gap_global(10)

-- Every Space has its own layout; the first
-- argument is the SPACE id (number or name),
-- never a monitor. All Spaces
-- default to "bsp". Modes: bsp | stack |
-- scrolling | monocle | grid | floating
-- KiwiDesk.set_mode(1, "stack")
-- KiwiDesk.set_mode("music", "floating")

-- Windows that should never be tiled:
-- float_rules = { "com.apple.calculator" }

-- Apps KiwiDesk should never manage at all:
-- ignore_rules = { "eu.exelban.Stats" }

-- Send apps to fixed Spaces:
-- app_rules = {
--   ["com.spotify.client"] = "music"
-- }

-- Load a saved profile per macOS Desktop
-- (the Mission Control number):
-- KiwiDesk.bind_profile_to_desktop(
--     2, "Creator Studio")

-- Keybindings:
-- KiwiDesk.bind("cmd+alt+left", function()
--     KiwiDesk.focus("left")

-- end)
-- KiwiDesk.bind("control+option+b", function()
--   KiwiDesk.exec(os.getenv("HOME") .. "/.config/sketchybar/plugins/mode_sketchybar.sh")
-- end, { desc = "SketchyBar mode" })

-- KiwiDesk.bind("control+option+n", function()
--   KiwiDesk.exec(os.getenv("HOME") .. "/.config/sketchybar/plugins/mode_macos.sh")
-- end, { desc = "macOS menu bar mode" })
