import AppKit

// NSWorkspace targets the visible desktop on a screen, not KiwiDesk Spaces.
let app = NSApplication.shared
app.setActivationPolicy(.accessory)
app.activate(ignoringOtherApps: true)
let panel = NSOpenPanel()
panel.title = "Wallpaper for this macOS desktop"
panel.message = "Switch to the desktop you want first. Disable ‘Show on all Spaces’ in Wallpaper settings."
panel.allowedFileTypes = ["jpg", "jpeg", "png", "heic", "webp", "tiff"]
panel.allowsMultipleSelection = false
if panel.runModal() == .OK, let url = panel.url, let screen = NSScreen.main {
    do {
        try NSWorkspace.shared.setDesktopImageURL(url, for: screen, options: [
            .imageScaling: NSImageScaling.scaleProportionallyUpOrDown.rawValue,
            .allowClipping: true
        ])
    } catch {
        let alert = NSAlert(error: error)
        alert.runModal()
        exit(1)
    }
}
