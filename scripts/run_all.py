#!/usr/bin/env python3
"""
One-shot runner for the full pipeline:
1) analyze_traffic -> CSV
2) generate_report -> Markdown + PNG
"""
import subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PCAPS = BASE / "sample_pcaps"
REPORTS = BASE / "reports"

commands = [
    [sys.executable, str(BASE / "scripts" / "analyze_traffic.py"),
     "--pcap_dir", str(PCAPS),
     "--output", str(REPORTS / "anomaly_report.csv")],
    [sys.executable, str(BASE / "scripts" / "generate_report.py"),
     str(REPORTS / "anomaly_report.csv"),
     str(REPORTS / "anomaly_summary.md")]
]

for cmd in commands:
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd)

print("\nPipeline complete. See 'reports/' for CSV, MD, and PNG.")
