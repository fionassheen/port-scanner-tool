#!/usr/bin/env python3
"""
report_gen.py: run scanner.py and convert CSV to a markdown report.
"""
import argparse, subprocess, csv
from datetime import datetime

def run_scanner(target, ports, csvfile, workers, timeout):
    cmd = ["python3", "scanner.py", target, "--ports", ports, "--csv", csvfile, "--workers", str(workers), "--timeout", str(timeout)]
    print("Running scanner:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def csv_to_md(csvfile, mdfile, target):
    rows = []
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(mdfile, 'w') as m:
        m.write(f"# Scan Report for {target}\n")
        m.write(f"Generated: {now}\n\n")
        m.write("## Summary of Open Ports\n\n")
        m.write("| Port | Open | Banner |\n")
        m.write("|--:|:--:|:--|\n")
        for r in rows:
            if r['open'].lower() in ("true","1","yes"):
                banner = (r.get('banner') or \"\").replace(\"\\n\",\" \").replace(\"|\",\" \")
                m.write(f"| {r['port']} | {r['open']} | {banner[:200]} |\n")
    print(f"Markdown report written to {mdfile}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--ports", default="1-1024")
    parser.add_argument("--csv", default="scan_results.csv")
    parser.add_argument("--md", default="scan_report.md")
    parser.add_argument("--workers", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=0.8)
    args = parser.parse_args()

    run_scanner(args.target, args.ports, args.csv, args.workers, args.timeout)
    csv_to_md(args.csv, args.md, args.target)

if __name__ == "__main__":
    main()
