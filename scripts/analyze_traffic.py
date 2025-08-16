#!/usr/bin/env python3
"""
Analyze PCAP files in --pcap_dir, generate deterministic features from filenames,
train IsolationForest, and write predictions to --output (CSV).

Why deterministic?
- Avoids bundling large binary PCAPs
- Ensures repeatable results on any machine
- Still demonstrates a real ML workflow end-to-end

Output columns:
file, packet_count, avg_len, tcp_ratio, udp_ratio, flow_entropy, anomaly
(anomaly: 1 = anomaly, 0 = normal)
"""
from pathlib import Path
import argparse
import hashlib
import math
import pandas as pd
from sklearn.ensemble import IsolationForest

def hash_to_unit(hbytes: bytes, salt: str) -> float:
    """Map sha256(filename+salt) to [0,1)."""
    h = hashlib.sha256(hbytes + salt.encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF

def deterministic_features(filename: str) -> dict:
    """
    Generate pseudo-features from a filename so results are reproducible.
    """
    b = filename.encode("utf-8")
    # Packet count: 80–1200
    packet_count = int(80 + hash_to_unit(b, "pc") * 1120)
    # Avg packet length: 64–1400 bytes
    avg_len = round(64 + hash_to_unit(b, "len") * (1400 - 64), 1)
    # Ratios (sum <= 1)
    tcp_ratio = round(hash_to_unit(b, "tcp"), 3)
    udp_ratio = round(0.9 * (1 - tcp_ratio) * hash_to_unit(b, "udp"), 3)
    # Flow entropy: 0.2–1.8 (higher = more diverse endpoints/ports)
    flow_entropy = round(0.2 + hash_to_unit(b, "ent") * 1.6, 3)
    return {
        "packet_count": packet_count,
        "avg_len": avg_len,
        "tcp_ratio": tcp_ratio,
        "udp_ratio": udp_ratio,
        "flow_entropy": flow_entropy,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pcap_dir", required=True, help="Directory with .pcap files (placeholders are fine)")
    ap.add_argument("--output", required=True, help="CSV output path")
    args = ap.parse_args()

    pcap_dir = Path(args.pcap_dir)
    out_csv = Path(args.output)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    pcaps = sorted([p for p in pcap_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pcap"])
    if not pcaps:
        raise SystemExit(f"No .pcap files found in: {pcap_dir}")

    rows = []
    for p in pcaps:
        feat = deterministic_features(p.name)
        feat["file"] = p.name
        rows.append(feat)

    df = pd.DataFrame(rows, columns=[
        "file", "packet_count", "avg_len", "tcp_ratio", "udp_ratio", "flow_entropy"
    ])

    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,   # assume ~15% anomalous
        random_state=42
    )
    df["anomaly"] = model.fit_predict(df[["packet_count","avg_len","tcp_ratio","udp_ratio","flow_entropy"]])
    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    df.to_csv(out_csv, index=False)
    print(f"[ok] wrote {out_csv}")

if __name__ == "__main__":
    main()
