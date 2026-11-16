#!/usr/bin/python3
"""Resource labels and process popups; no process arguments are collected."""
import os
from pathlib import Path
import re
import subprocess

SB = '/opt/homebrew/bin/sketchybar'


def output(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=12)
        return p.stdout if p.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        return ''


def processes(text):
    rows = []
    for line in text.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) != 4:
            continue
        try:
            rows.append((int(parts[0]), float(parts[1]), int(parts[2]), Path(parts[3]).name))
        except ValueError:
            continue
    return rows


def memory_percent(vm, total):
    page = re.search(r'page size of (\d+) bytes', vm)
    if not page or total <= 0:
        return None
    values = dict((k.strip(), int(v)) for k, v in re.findall(r'^([^:\n]+):\s+(\d+)\.', vm, re.M))
    if 'Pages free' not in values:
        return None
    reclaimable = sum(values.get(k, 0) for k in ['Pages free', 'Pages inactive', 'Pages speculative'])
    return max(0, min(100, round((1 - reclaimable * int(page[1]) / total) * 100)))


def main():
    name = os.environ.get('NAME', 'cpu')
    sender = os.environ.get('SENDER', '')
    if sender == 'mouse.exited.global':
        subprocess.run([SB, '--set', name, 'popup.drawing=off'], check=False)
        return
    rows = processes(output(['/bin/ps', '-axo', 'pid=,pcpu=,rss=,comm=']))
    cpu = None
    top = output(['/usr/bin/top', '-l', '1', '-n', '0'])
    idle = re.search(r'CPU usage:.*?([\d.]+)% idle', top)
    if idle:
        cpu = round(100 - float(idle[1]))
    total_text = output(['/usr/sbin/sysctl', '-n', 'hw.memsize']).strip()
    memory = memory_percent(output(['/usr/bin/vm_stat']), int(total_text)) if total_text.isdigit() else None
    gpu_text = output(['/usr/sbin/ioreg', '-r', '-d', '1', '-w0', '-c', 'IOAccelerator'])
    gpu_match = re.search(r'"Device Utilization %"\s*=\s*(\d+)', gpu_text)
    gpu = int(gpu_match[1]) if gpu_match else None
    args = [SB]
    for item, value in [('cpu', cpu), ('mem', memory), ('gpu', gpu)]:
        args += ['--set', item, 'label=' + ('{}%'.format(value) if value is not None else '—')]
    for item, index, unit in [('cpu', 1, '%'), ('mem', 2, 'MiB')]:
        ranked = sorted(rows, key=lambda r: r[index], reverse=True)[:8]
        args += ['--set', item + '.header', 'label=' + ('Top CPU processes · PID / usage' if item == 'cpu' else 'Top RAM processes · PID / resident memory')]
        for i in range(8):
            label = 'Unavailable' if i == 0 and not ranked else ''
            if i < len(ranked):
                row = ranked[i]
                value = row[index] if item == 'cpu' else row[index] / 1024
                label = '{:<23} {:>6}  {:>7.1f} {}'.format(row[3][:23], row[0], value, unit)
            args += ['--set', '{}.row{}'.format(item, i + 1), 'label=' + label]
    args += ['--set', 'cpu.note', 'label=Process CPU: ps average; 100% = one core. Bar: total CPU.']
    args += ['--set', 'mem.note', 'label=RSS can share pages. Bar estimates RAM excluding inactive/cache.']
    args += ['--set', 'gpu.header', 'label=GPU · overall device usage']
    for i in range(1, 9):
        label = ''
        if i == 1:
            label = 'Overall: {}%'.format(gpu) if gpu is not None else 'Overall GPU usage unavailable on this Mac'
        elif i == 2:
            label = 'Per-process GPU usage is not exposed by this data source.'
        args += ['--set', 'gpu.row' + str(i), 'label=' + label, 'drawing=' + ('on' if i <= 2 else 'off')]
    args += ['--set', 'gpu.note', 'label=Activity Monitor → Window → GPU History for device history.']
    if sender == 'mouse.clicked':
        args += ['--set', name, 'popup.drawing=toggle']
    subprocess.run(args, check=False)


if __name__ == '__main__':
    main()
