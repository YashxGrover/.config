# Bar implementation status

The current bar is 48 px, with SF Pro labels at 14 pt and an opaque background.
Desktop symbols are Book, Globe, Terminal and House; only the active desktop shows its name.
Music sits left of the notch and the next calendar event sits right of it.
The current Kiwi Space number cycles Spaces on click. CPU/GPU/RAM/SSD widgets are absent.
Five app icons can appear at once; additional apps remain in the window popup, reached with +N.

## Helpers

Run `bash ~/.config/workflow/build_helpers.sh` after a fresh checkout or moving to a different Mac.
This compiles the CoreAudio output selector and generates the desktop symbol images.
The theme picker regenerates the symbol colors whenever a palette changes.

Network rates use the default network interface byte counters, including Ethernet or VPN if that is the default route. They are total interface traffic, not a speed test.
Sampling runs once per second while the Wi-Fi popup is open and stops when it closes.
Volume click lists audio outputs; selecting one changes only the default output device.

## Validation

Swift helpers compile. Python syntax checks, shell syntax checks and bar rendering tests pass.
Live layout, network counters, Calendar permissions and audio switching still require a real Mac session.
Spotify title and play/pause are implemented. ByTune is intentionally deferred. An optional external-provider contract in sketchybar/media.json supports adding browser or other app media later; see sketchybar/MEDIA.md.
No live reload was requested during the latest code-only work.

Calendar data uses explicit record separators, filters past start times, caches for 60 seconds and labels tomorrow. App icons remember the last focused window and cycle on repeated clicks. KiwiDesk events trigger immediate updates, with a ten-second recovery poll. Theme selection presents the four agreed palettes first.
