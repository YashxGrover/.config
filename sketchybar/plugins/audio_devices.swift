import Foundation
import CoreAudio
func address(_ selector: AudioObjectPropertySelector, _ scope: AudioObjectPropertyScope = kAudioObjectPropertyScopeGlobal) -> AudioObjectPropertyAddress {
    AudioObjectPropertyAddress(mSelector: selector, mScope: scope, mElement: kAudioObjectPropertyElementMain)
}
func string(_ id: AudioObjectID, _ selector: AudioObjectPropertySelector) -> String {
    var a = address(selector); var size = UInt32(MemoryLayout<UnsafeRawPointer?>.size); var result: UnsafeRawPointer?
    guard AudioObjectGetPropertyData(id, &a, 0, nil, &size, &result) == noErr else { return "" }
    guard let result = result else { return "" }
    return Unmanaged<CFString>.fromOpaque(result).takeUnretainedValue() as String
}
func fail(_ message: String) -> Never { fputs(message + "\n", stderr); exit(1) }
var a = address(kAudioHardwarePropertyDevices); var size: UInt32 = 0
let system = AudioObjectID(kAudioObjectSystemObject)
guard AudioObjectGetPropertyDataSize(system, &a, 0, nil, &size) == noErr else { fail("Cannot enumerate audio devices") }
var ids = [AudioDeviceID](repeating: 0, count: Int(size) / MemoryLayout<AudioDeviceID>.size)
let status = ids.withUnsafeMutableBytes { AudioObjectGetPropertyData(system, &a, 0, nil, &size, $0.baseAddress!) }
guard status == noErr else { fail("Cannot read audio devices") }
var da = address(kAudioHardwarePropertyDefaultOutputDevice); var current = AudioDeviceID(0); var ds = UInt32(MemoryLayout<AudioDeviceID>.size)
AudioObjectGetPropertyData(system, &da, 0, nil, &ds, &current)
var devices: [[String: Any]] = []
for id in ids {
    var streams = address(kAudioDevicePropertyStreams, kAudioDevicePropertyScopeOutput); var bytes: UInt32 = 0
    guard AudioObjectGetPropertyDataSize(id, &streams, 0, nil, &bytes) == noErr, bytes > 0 else { continue }
    devices.append(["id": id, "uid": string(id, kAudioDevicePropertyDeviceUID), "name": string(id, kAudioObjectPropertyName), "selected": id == current])
}
if CommandLine.arguments.count == 3 && CommandLine.arguments[1] == "select" {
    guard let device = devices.first(where: { $0["uid"] as? String == CommandLine.arguments[2] }), let id = device["id"] as? AudioDeviceID else { fail("Audio device disconnected") }
    var selected = id
    guard AudioObjectSetPropertyData(system, &da, 0, nil, UInt32(MemoryLayout<AudioDeviceID>.size), &selected) == noErr else { fail("Cannot select audio output") }
} else {
    let data = try JSONSerialization.data(withJSONObject: devices, options: [.sortedKeys])
    print(String(decoding: data, as: UTF8.self))
}
