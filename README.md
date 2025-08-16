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
