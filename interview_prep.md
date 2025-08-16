# Interview Prep – Network Anomaly Detection

## Talking Points
- **Why IsolationForest?**  
  Unsupervised, robust to high-dimensional feature spaces, does not require labeled data.

- **Deterministic features rationale:**  
  For a portfolio demo, you need reproducibility without shipping large PCAPs.  
  Filename-derived features keep the ML workflow realistic yet lightweight.

- **Feature ideas for real parsing (future):**  
  - Packet/byte counts per flow, inter-arrival times (IAT), protocol distribution  
  - Flow-level stats: durations, unique dst/src counts, entropy of ports/IPs  
  - TLS SNI counts, DNS QNAME patterns, HTTP status distributions

- **Evaluation strategy when you add labels:**  
  Train/validation split with synthetic or labeled PCAPs → precision/recall/ROC.  
  Use contamination grid-search for IsolationForest sensitivity.

- **Hardening / Productionization:**  
  Batch scheduler (cron), log to JSONL, alerts to Slack/Email, dashboards (Grafana).

## Red Flags To Mention Honestly
- Current version uses **deterministic features** (safe & reproducible); no raw packet parsing.  
- No live capture (no elevated privileges required).  
- Small sample set; meant for **demonstration and interview** discussion.
