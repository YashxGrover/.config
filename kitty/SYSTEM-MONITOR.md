# Kitty system monitor

Run `~/.config/kitty/open-system-monitor.sh` to open a separate Kitty window with a live macOS dashboard. It opens `btop` when installed and otherwise uses the included Python fallback. The `btop` settings and Catppuccin Mocha theme are ready in `~/.config/btop/`.

The fallback shows CPU load and logical core count, used/total/compressed memory, root disk usage, battery state, Mac model/chip/GPU, uptime, default-route network throughput, and top processes by CPU with RSS memory. Press `q` to close it and `r` to refresh immediately. `btop` adds its richer interactive graphs, sorting, and process controls.

macOS does not provide ordinary unprivileged tools with reliable Apple GPU utilization and temperature readings. The dashboard shows the GPU model and calls this limitation out rather than inventing a load percentage. Network speed is measured as traffic on the default interface, not as an internet speed test.

`btop` could not be installed from this session because Homebrew's cache and `/opt/homebrew` are not writable here. Run `brew install btop` in your Mac's Terminal; the launcher will switch to it automatically. The display can take a few seconds to populate hardware details on first fallback launch because `system_profiler` supplies the model information.
