#!/usr/bin/env python3
"""
Generate a human-readable Markdown summary and a matplotlib chart
from a CSV produced by analyze_traffic.py.

Outputs:
- <outfile>.md (e.g., reports/anomaly_summary.md)
- reports/anomalies_per_file.png
"""
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

def make_chart(df: pd.DataFrame, out_png: Path):
    # Bar chart: anomaly (0/1) per file
    plt.figure()  # one chart per figure; no global styles, no custom colors
    ax = df.set_index("file")["anomaly"].plot(kind="bar")
    ax.set_title("Anomalies per File (1 = anomaly, 0 = normal)")
    ax.set_xlabel("PCAP File")
    ax.set_ylabel("Anomaly Flag")
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=150)
    plt.close()
    print(f"[ok] wrote {out_png}")

def csv_to_md(infile: Path, outfile: Path, chart_png: Path):
    df = pd.read_csv(infile)
    anomalies = int(df["anomaly"].sum())
    total = int(len(df))
    normal = total - anomalies

    lines = []
    lines.append("# Network Anomaly Detection – Summary\n\n")
    lines.append("## Overview\n")
    lines.append(f"- Total files analyzed: **{total}**\n")
    lines.append(f"- Anomalous files: **{anomalies}**\n")
    lines.append(f"- Normal files: **{normal}**\n\n")
    lines.append("## Results Table\n\n")
    lines.append(df.to_markdown(index=False))
    lines.append("\n\n## Visualization\n")
    lines.append(f"![Anomalies per File]({chart_png.name})\n")

    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text("".join(lines), encoding="utf-8")
    print(f"[ok] wrote {outfile}")

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_report.py <in.csv> <out.md>")
        sys.exit(2)
    infile = Path(sys.argv[1]).resolve()
    outfile = Path(sys.argv[2]).resolve()
    chart_png = outfile.parent / "anomalies_per_file.png"

    if not infile.exists():
        raise SystemExit(f"Input CSV not found: {infile}")

    df = pd.read_csv(infile)
    make_chart(df, chart_png)
    csv_to_md(infile, outfile, chart_png)

if __name__ == "__main__":
    main()
