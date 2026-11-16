import AppKit
import ApplicationServices

let bar = "/opt/homebrew/bin/sketchybar"
func setHidden(_ hidden: Bool) {
    let p = Process()
    p.executableURL = URL(fileURLWithPath: bar)
    p.arguments = ["--bar", hidden ? "hidden=on" : "hidden=off", hidden ? "topmost=off" : "topmost=on"]
    try? p.run()
    p.waitUntilExit()
}

// Existing Accessibility permission improves open-menu detection; never request it.
func menuIsOpen() -> Bool {
    guard AXIsProcessTrusted() else { return false }
    var element: CFTypeRef?
    let system = AXUIElementCreateSystemWide()
    guard AXUIElementCopyAttributeValue(system, kAXFocusedUIElementAttribute as CFString, &element) == .success,
          let element = element, CFGetTypeID(element) == AXUIElementGetTypeID() else { return false }
    var current = unsafeBitCast(element, to: AXUIElement.self)
    for _ in 0..<8 {
        var role: CFTypeRef?
        AXUIElementCopyAttributeValue(current, kAXRoleAttribute as CFString, &role)
        if let role = role as? String, [kAXMenuRole, kAXMenuItemRole].contains(role) { return true }
        var parent: CFTypeRef?
        guard AXUIElementCopyAttributeValue(current, kAXParentAttribute as CFString, &parent) == .success,
              let parent = parent, CFGetTypeID(parent) == AXUIElementGetTypeID() else { break }
        current = unsafeBitCast(parent, to: AXUIElement.self)
    }
    return false
}

let initial = NSEvent.mouseLocation
let screen = NSScreen.screens.first(where: { $0.frame.contains(initial) }) ?? NSScreen.main
let started = ProcessInfo.processInfo.systemUptime
var deadline = started + 2
var lastPoint = initial
var engaged = false
var lastClickTime = started - CGEventSource.secondsSinceLastEventType(.combinedSessionState, eventType: .leftMouseDown)
setHidden(true)
defer { setHidden(false) }
while true {
    Thread.sleep(forTimeInterval: 0.05)
    let now = ProcessInfo.processInfo.systemUptime
    let point = NSEvent.mouseLocation
    let inBar = screen.map { $0.frame.contains(point) && point.y >= $0.frame.maxY - 38 } ?? false
    let moved = hypot(point.x - lastPoint.x, point.y - lastPoint.y) > 2
    let clickTime = now - CGEventSource.secondsSinceLastEventType(.combinedSessionState, eventType: .leftMouseDown)
    let clicked = clickTime > lastClickTime + 0.02
    if clicked { lastClickTime = clickTime }
    if now - started > 0.15 && inBar && (moved || clicked) { engaged = true }
    if (engaged && inBar) || menuIsOpen() || CGEventSource.buttonState(.combinedSessionState, button: .left) {
        deadline = now + 2
    }
    lastPoint = point
    if now >= deadline { break }
}
