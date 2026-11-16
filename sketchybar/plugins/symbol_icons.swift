import AppKit
let args = CommandLine.arguments
if args.count != 4 { exit(1) }
let directory = URL(fileURLWithPath: args[1], isDirectory: true)
try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
func color(_ input: String) -> NSColor {
    let value = UInt64(input.replacingOccurrences(of: "0x", with: ""), radix: 16) ?? 0xFFFFFFFF
    return NSColor(srgbRed: CGFloat((value >> 16) & 255) / 255, green: CGFloat((value >> 8) & 255) / 255, blue: CGFloat(value & 255) / 255, alpha: 1)
}
let symbols: [(String,String)] = [
    ("desktop1","book.closed"),("desktop2","globe"),
    ("desktop3","terminal"),("desktop4","house")
]
for (name, symbol) in symbols {
    guard let image = NSImage(systemSymbolName: symbol, accessibilityDescription: nil)?.withSymbolConfiguration(NSImage.SymbolConfiguration(pointSize: 22, weight: .regular)) else {
        fputs("Missing symbol: \(symbol)\n", stderr); exit(1)
    }
    guard let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 32, pixelsHigh: 32, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0), let context = NSGraphicsContext(bitmapImageRep: rep) else { exit(1) }
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    let scale = min(28 / image.size.width, 24 / image.size.height)
    let width = image.size.width * scale, height = image.size.height * scale
    image.draw(in: NSRect(x: (32-width)/2, y: (32-height)/2, width: width, height: height))
    color(name.hasPrefix("desktop") ? args[2] : args[3]).setFill()
    NSRect(x:0, y:0, width:32, height:32).fill(using:.sourceAtop)
    NSGraphicsContext.restoreGraphicsState()
    guard let data = rep.representation(using: .png, properties: [:]) else { exit(1) }
    try data.write(to: directory.appendingPathComponent(name+".png"), options: .atomic)
}
