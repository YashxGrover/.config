#!/usr/bin/env python3
"""Small, dependency-free macOS system dashboard for Kitty."""

from __future__ import annotations

import curses
import json
import re
import socket
import subprocess
import time
from collections import deque
from datetime import datetime


BG = "#1e1e2e"
FG = "#cdd6f4"
MUTED = "#a6adc8"
CYAN = "#74c7ec"
GREEN = "#a6e3a1"
YELLOW = "#f9e2af"
PURPLE = "#cba6f7"
RED = "#f38ba8"
CPU_HISTORY: deque[float] = deque(maxlen=60)
NET_HISTORY: deque[float] = deque(maxlen=60)


def command(*args: str, timeout: float = 2.0) -> str:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def system_info() -> dict[str, str]:
    hardware = command("system_profiler", "SPHardwareDataType", "-json", timeout=8)
    displays = command("system_profiler", "SPDisplaysDataType", "-json", timeout=8)
    info: dict[str, str] = {
        "host": socket.gethostname().split(".")[0],
        "os": command("sw_vers", "-productVersion") or "macOS",
        "cores": command("sysctl", "-n", "hw.ncpu") or "?",
        "memory": "?",
        "chip": "Apple silicon / CPU",
        "gpu": "GPU details unavailable",
    }
    try:
        info["memory"] = f"{int(command('sysctl', '-n', 'hw.memsize')) // (1024**3)} GiB"
    except ValueError:
        pass
    try:
        hw = json.loads(hardware).get("SPHardwareDataType", [{}])[0]
        info["chip"] = hw.get("chip_type") or hw.get("cpu_type") or info["chip"]
    except (ValueError, TypeError, IndexError, AttributeError):
        pass
    try:
        gpu = json.loads(displays).get("SPDisplaysDataType", [{}])[0]
        info["gpu"] = gpu.get("sppci_model") or gpu.get("_name") or info["gpu"]
    except (ValueError, TypeError, IndexError, AttributeError):
        pass
    return info


def memory_stats() -> tuple[int, int, int]:
    """Return used, total, and compressed memory in bytes from vm_stat."""
    total_text = command("sysctl", "-n", "hw.memsize")
    vm = command("vm_stat")
    try:
        total = int(total_text)
        page = int(command("pagesize") or "4096")
    except ValueError:
        return 0, 0, 0
    values: dict[str, int] = {}
    for line in vm.splitlines():
        match = re.match(r"([^:]+):\s*([0-9.]+)", line)
        if match:
            values[match.group(1)] = int(float(match.group(2)))
    free = sum(values.get(key, 0) for key in ("Pages free", "Pages inactive", "Pages speculative")) * page
    compressed = values.get("Pages occupied by compressor", 0) * page
    used = max(0, total - free)
    return min(used, total), total, compressed


def disk_stats() -> tuple[str, str, str]:
    output = command("df", "-h", "/")
    lines = output.splitlines()
    if len(lines) > 1:
        fields = lines[-1].split()
        if len(fields) >= 5:
            return fields[2], fields[3], fields[4]
    return "?", "?", "?"


def network_stats() -> tuple[str, int, int]:
    route = command("route", "-n", "get", "default")
    match = re.search(r"interface:\s*(\S+)", route)
    interface = match.group(1) if match else "?"
    table = command("netstat", "-ibn")
    rx = tx = 0
    for line in table.splitlines():
        fields = line.split()
        if fields and fields[0] == interface and len(fields) >= 10:
            try:
                rx, tx = int(fields[7]), int(fields[9])
                break
            except ValueError:
                continue
    return interface, rx, tx


def process_rows() -> list[tuple[str, str, str, str]]:
    raw = command("ps", "-A", "-o", "pid=,pcpu=,rss=,comm=", timeout=3)
    rows = []
    for line in raw.splitlines():
        fields = line.strip().split(None, 3)
        if len(fields) != 4:
            continue
        pid, cpu, rss, name = fields
        try:
            rss_mb = int(rss) / 1024
            cpu_value = float(cpu)
        except ValueError:
            continue
        rows.append((cpu_value, pid, f"{rss_mb:.0f}M", name.rsplit("/", 1)[-1]))
    rows.sort(key=lambda row: row[0], reverse=True)
    return [(pid, f"{cpu:.1f}%", mem, name) for cpu, pid, mem, name in rows[:14]]


def uptime_text() -> str:
    raw = command("uptime")
    match = re.search(r"up\s+(.+?),\s+\d+ users?", raw)
    return match.group(1).strip() if match else raw or "—"


def battery_text() -> str:
    raw = command("pmset", "-g", "batt")
    match = re.search(r"(\d+)%", raw)
    return f"{match.group(1)}%" if match else "Desktop / unavailable"


def safe_add(stdscr, y: int, x: int, text: str, attr: int = 0, width: int | None = None) -> None:
    height, screen_width = stdscr.getmaxyx()
    if y < 0 or y >= height or x < 0 or x >= screen_width:
        return
    clipped = text[: max(0, (screen_width - x - 1) if width is None else min(width, screen_width - x - 1))]
    try:
        stdscr.addstr(y, x, clipped, attr)
    except curses.error:
        pass


def box(stdscr, top: int, left: int, height: int, width: int, title: str, color: int) -> None:
    if height < 3 or width < 8:
        return
    attr = curses.color_pair(color)
    safe_add(stdscr, top, left, "╭" + "─" * (width - 2) + "╮", attr, width)
    safe_add(stdscr, top + height - 1, left, "╰" + "─" * (width - 2) + "╯", attr, width)
    for y in range(top + 1, top + height - 1):
        safe_add(stdscr, y, left, "│", attr)
        safe_add(stdscr, y, left + width - 1, "│", attr)
    safe_add(stdscr, top, left + 2, f" {title} ", attr | curses.A_BOLD, width - 4)


def meter(value: float, width: int = 18) -> str:
    filled = min(width, max(0, round(value / 100 * width)))
    return "█" * filled + "░" * (width - filled)


def sparkline(values: deque[float], width: int, ceiling: float = 100.0) -> str:
    levels = "▁▂▃▄▅▆▇█"
    samples = list(values)[-max(1, width):]
    if not samples:
        return ""
    return "".join(levels[min(7, int(max(0, value) / max(1, ceiling) * 8))] for value in samples)


def draw(stdscr, info: dict[str, str], old_net: tuple[str, int, int], old_time: float) -> tuple[str, int, int]:
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    if height < 16 or width < 64:
        safe_add(stdscr, 0, 0, "Resize Kitty to at least 64 columns × 16 rows. Press q to exit.", curses.A_BOLD)
        stdscr.refresh()
        return old_net

    cyan, green, yellow, purple, red, dim, normal = (curses.color_pair(i) for i in range(1, 8))
    safe_add(stdscr, 0, 2, f"  {info['host']}  ·  macOS {info['os']}  ·  {info['chip']}  ", curses.A_BOLD | cyan)
    safe_add(stdscr, 0, max(2, width - 27), datetime.now().strftime("%a %d %b  %H:%M:%S"), dim)

    gap = 1
    col = (width - 3 * gap) // 4
    top = 2
    cpu_total = 0.0
    for _, cpu, _, _ in process_rows():
        try:
            cpu_total += float(cpu.rstrip("%"))
        except ValueError:
            pass
    try:
        cpu_percent = min(100.0, cpu_total / max(1, int(info["cores"])) )
    except ValueError:
        cpu_percent = min(cpu_total, 100.0)
    CPU_HISTORY.append(cpu_percent)
    used, total, compressed = memory_stats()
    mem_pct = used * 100 / total if total else 0
    cards = [
        ("CPU", f"{cpu_percent:.0f}%", f"{info['cores']} logical cores", cyan),
        ("MEMORY", f"{mem_pct:.0f}%", f"{used / 1024**3:.1f} / {total / 1024**3:.0f} GiB", purple),
        ("DISK · /", "", "", green),
        ("POWER", battery_text(), "Battery status", yellow),
    ]
    disk_used, disk_free, disk_pct = disk_stats()
    cards[2] = ("DISK · /", disk_pct, f"{disk_used} used · {disk_free} free", green)
    for index, (title, value, subtitle, color) in enumerate(cards):
        x = gap + index * (col + gap)
        box(stdscr, top, x, 6, col, title, 4 if color == cyan else 5 if color == green else 6 if color == purple else 3)
        safe_add(stdscr, top + 1, x + 2, value, curses.A_BOLD | color, col - 4)
        if index < 3:
            numeric = cpu_percent if index == 0 else mem_pct if index == 1 else (float(disk_pct.rstrip("%")) if disk_pct.endswith("%") else 0)
            safe_add(stdscr, top + 2, x + 2, meter(numeric, max(8, col - 5)), color, col - 4)
            if index == 0:
                safe_add(stdscr, top + 3, x + 2, sparkline(CPU_HISTORY, col - 5), color, col - 4)
        else:
            safe_add(stdscr, top + 2, x + 2, subtitle, dim, col - 4)
        safe_add(stdscr, top + 4, x + 2, subtitle, dim, col - 4)

    mid = 9
    left_width = max(26, width // 3)
    right_left = left_width + 2
    box(stdscr, mid, 1, 7, left_width, "MACHINE", 4)
    machine_rows = [
        f"Chip     {info['chip']}",
        f"Graphics {info['gpu']}",
        f"Memory   {info['memory']} total · {compressed / 1024**3:.1f} GiB compressed",
        f"Uptime   {uptime_text()}",
        f"Note     GPU load/temperature needs privileged sampling",
    ]
    for i, text in enumerate(machine_rows):
        safe_add(stdscr, mid + 1 + i, 3, text, normal if i < 4 else dim, left_width - 4)

    iface, rx, tx = network_stats()
    now = time.monotonic()
    prev_iface, prev_rx, prev_tx = old_net
    elapsed = max(0.1, now - old_time) if old_time else 1.0
    down = max(0, rx - prev_rx) / elapsed if iface == prev_iface else 0
    up = max(0, tx - prev_tx) / elapsed if iface == prev_iface else 0
    NET_HISTORY.append(down + up)
    box(stdscr, mid, right_left, 7, width - right_left - 1, "NETWORK", 5)
    safe_add(stdscr, mid + 1, right_left + 2, f"Interface  {iface}  ·  live interface throughput", dim)
    safe_add(stdscr, mid + 3, right_left + 2, f"↓  {down / 1024:7.1f} KiB/s      ↑  {up / 1024:7.1f} KiB/s", curses.A_BOLD | green)
    safe_add(stdscr, mid + 4, right_left + 2, sparkline(NET_HISTORY, max(8, width - right_left - 6), max(1024, max(NET_HISTORY, default=0))), green)
    safe_add(stdscr, mid + 5, right_left + 2, "Totals include all traffic on the default route.", dim)

    proc_top = mid + 8
    proc_height = height - proc_top - 2
    box(stdscr, proc_top, 1, proc_height, width - 2, "TOP PROCESSES · sorted by CPU · RSS memory", 6)
    safe_add(stdscr, proc_top + 1, 3, f"{'PID':>7}  {'CPU':>6}  {'RSS':>7}  PROCESS", dim | curses.A_BOLD)
    rows = process_rows()
    max_rows = max(0, proc_height - 3)
    for idx, (pid, cpu, rss, name) in enumerate(rows[:max_rows]):
        attr = normal if idx % 2 == 0 else dim
        safe_add(stdscr, proc_top + 2 + idx, 3, f"{pid:>7}  {cpu:>6}  {rss:>7}  {name}", attr)
    safe_add(stdscr, height - 1, 2, "q quit  ·  r refresh now  ·  2 second refresh", dim)
    stdscr.refresh()
    return iface, rx, tx


def main(stdscr) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(250)
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
            for idx, value in enumerate((CYAN, GREEN, PURPLE, YELLOW, RED, MUTED, FG), 1):
                color = curses.COLOR_CYAN if idx == 1 else curses.COLOR_GREEN if idx == 2 else curses.COLOR_MAGENTA if idx == 3 else curses.COLOR_YELLOW if idx == 4 else curses.COLOR_RED if idx == 5 else curses.COLOR_BLUE if idx == 6 else curses.COLOR_WHITE
                curses.init_pair(idx, color, -1)
        except curses.error:
            pass
    info = system_info()
    old_net = ("", 0, 0)
    old_time = 0.0
    last_refresh = 0.0
    while True:
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            break
        now = time.monotonic()
        if key == ord("r") or now - last_refresh >= 2:
            old_net = draw(stdscr, info, old_net, old_time)
            old_time = now
            last_refresh = now


if __name__ == "__main__":
    curses.wrapper(main)
