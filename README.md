 Network Anomalies Detection – Wireshark + ML (Functional)

A **fully local, recruiter-friendly** simulation that demonstrates network anomaly detection using
**pre-captured PCAP filenames** (placeholders) → **deterministic feature extraction** → **IsolationForest** →
**CSV + Markdown report** with a **matplotlib** chart.  
No live capture, no privileged access, and no heavy PCAP parsing required.

> Why deterministic? Recruiters want a reproducible demo. This project derives stable features
> from PCAP filenames, so results are consistent across machines without bundling large PCAPs.

---

## What’s included

- `sample_pcaps/` – two placeholder PCAPs (names drive deterministic feature generation)
- `scripts/analyze_traffic.py` – extracts features, trains IsolationForest, outputs `reports/anomaly_report.csv`
- `scripts/generate_report.py` – turns CSV into `reports/anomaly_summary.md` + `reports/anomalies_per_file.png`
- `scripts/run_all.py` – convenience runner for the full pipeline
- `docs/interview_prep.md` – talking points for interviews
- `requirements.txt`, `.gitignore`, `LICENSE`

---
# 1) Analyze (build features + model + predictions)
python scripts/analyze_traffic.py --pcap_dir sample_pcaps --output reports/anomaly_report.csv

# 2) Generate summary (markdown + chart)
python scripts/generate_report.py reports/anomaly_report.csv reports/anomaly_summary.md

## Quickstart

```bash
python -V           # Python 3.8+
python scripts/run_all.py
# Outputs:
#  - reports/anomaly_report.csv
#  - reports/anomaly_summary.md
#  - reports/anomalies_per_file.png

```
How it works (High-level)

Feature Extraction (Deterministic):

For each *.pcap file, features are derived from a filename hash:

packet_count, avg_len, tcp_ratio, udp_ratio, flow_entropy

This avoids bundling large binary PCAPs but keeps the data science workflow authentic.

Modeling:

IsolationForest with reproducible defaults (random_state=42, contamination=0.15).

Produces anomaly column: 1 = anomaly, 0 = normal.

Reporting:

Markdown summary with key counts and a table of results.

A chart anomalies_per_file.png (matplotlib) showing anomaly flags per file.

Example Results (from provided placeholders)

suspicious_traffic.pcap → likely anomaly

normal_traffic.pcap → likely normal

Because features are deterministic from names, “suspicious” tends to score as anomalous without random noise.

Extend this project (optional)

Swap deterministic features with real parsing (e.g., pyshark / scapy) when you want to demo deeper packet/flow features.

Add more placeholder PCAPs named by scenario: dns_tunnel.pcap, port_scan.pcap, etc.

Log metrics (precision/recall) if you label a larger sample set.

Skills demonstrated

Anomaly detection with IsolationForest

End-to-end ML workflow (features → model → artifacts → report + chart)

Reproducible, minimal-dependency portfolio engineering

Clear GitHub documentation and structure


```
