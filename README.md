Port Scanner Tool

A lightweight, multi-threaded TCP port scanner in Python.
This project implements a safe, lab-friendly port scanner that discovers open TCP ports on a target host, attempts simple banner grabbing, and exports results to CSV and a Markdown report. It’s intended for learning, demonstrations, and use only against systems you own or have explicit permission to test (e.g., Metasploitable or a local VM).

Project summary:

This repository contains a Python-based TCP port scanner (scanner.py) and a small wrapper (report_gen.py) that runs the scanner and generates a human-readable Markdown report from the CSV output. The scanner uses socket for TCP connects, optionally grabs service banners, and uses concurrent.futures.ThreadPoolExecutor for concurrent scanning.

Key principles:

1. Simple and readable code (teaching-first)
2. Uses standard Python library (no mandatory third-party packages)
3. Configurable port range, concurrency, and timeouts
4. Exports machine-readable CSV and Markdown report to easily document results

Features:

a. Multi-threaded TCP connect-based scanning
b. Banner grabbing (best-effort) for open ports
c. CSV export of results for artifact submission
d. Simple Markdown report generator summarizing open services
e. Command-line options for:
  1. target host (IP or hostname)
  2. port ranges (single ports, comma list, or ranges like 1-1024)
  3. worker threads
  4. socket timeout
  5. CSV / Markdown output file names

Requirements:

1. Python 3.8+ (tested in Kali Linux)
2. No external packages required for the core scanner. (Optional: tabulate for prettier terminal tables if you choose to install it.)

Recommended environment:

1. Kali Linux VM (or any Linux VM) for running the scanner.
2. Metasploitable (or other test VM/container) as a safe target.

Repository structure:
port-scanner/
├─ scanner.py                 # Main multi-threaded port scanner
├─ report_gen.py              # Wrapper that runs scanner and builds a markdown report
├─ metasploitable_scan.csv     # (optional) CSV results produced by a run
├─ metasploitable_report.md    # (optional) generated report
├─ README.md                  # This file
└─ venv/                      # local virtualenv (should be ignored)

Quick start — run in 5 steps:
Copy & paste these commands from your project folder on Kali:

1. Activate virtualenv (optional; recommended):

cd ~/projects/port-scanner
python3 -m venv venv         # only if venv not created yet
source venv/bin/activate

2. Make scripts executable (optional):

chmod +x scanner.py report_gen.py

3. Basic localhost test:

./scanner.py localhost --ports 20-1024 --workers 100 --timeout 0.6 --csv localhost_scan.csv

4. Scan a lab target (example: Metasploitable):

./scanner.py 192.168.56.101 --ports 1-1000 --workers 200 --timeout 0.6 --csv metasploitable_scan.csv

5. Generate a Markdown report from the CSV:

./report_gen.py 192.168.56.101 --ports 1-1000 --csv metasploitable_scan.csv --md metasploitable_report.md


Full usage & examples:
scanner.py — options
Usage: scanner.py target [--ports 1-1024] [--workers 100] [--timeout 0.8] [--csv scan_results.csv]

Positional:
  target          Target hostname or IP to scan

Options:
  -p, --ports     Ports to scan (e.g. 22,80,443 or 1-1024)  (default: 1-1024)
  -w, --workers   Max concurrent threads (default: 100)
  -t, --timeout   Socket timeout in seconds (default: 0.8)
  --csv           CSV output filename (default: scan_results.csv)

Examples

Quick scan of top ports:

./scanner.py 192.168.56.101 --ports 22,80,443 --csv quick.csv


Large range with slower workers:

./scanner.py 192.168.56.101 --ports 1-5000 --workers 50 --timeout 1.2 --csv big_scan.csv

report_gen.py — quick run (wrapper)
This will run scanner.py (using python3 scanner.py) then read CSV and produce a Markdown table of only the open ports.

Example:

python3 report_gen.py 192.168.56.101 --ports 1-1000 --csv metasploitable_scan.csv --md metasploitable_report.md

Output format explanation:
CSV (scan_results.csv)

Columns:

1. timestamp — ISO timestamp when the CSV row was written
2. ip — resolved target IP
3. port — port number scanned
4. open — True/False
5. service — placeholder (empty by default; could be extended)
6. banner — first N bytes of the banner grabbed (best-effort)

Example CSV snippet:

timestamp,ip,port,open,service,banner
2025-10-05T21:02:00,192.168.56.101,21,True,,220 (vsFTPd 2.3.4)
2025-10-05T21:02:00,192.168.56.101,22,True,,SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
2025-10-05T21:02:00,192.168.56.101,80,True,,Apache/2.2.8 (Ubuntu)...

Markdown report (metasploitable_report.md):
A readable report that includes:

1. Target, scan date and settings
2. A table of discovered open ports and banners
3. Short observations and recommended next steps

Security, ethics & legal notice:

1. IMPORTANT — Always obey laws and ethical rules:
2. Do not scan systems you do not own or do not have explicit permission to test.
3. Port scanning can be flagged by intrusion detection systems. Use isolated lab environments (Metasploitable, VMs, containers).
4. The tools here are for educational and authorized use only. Misuse is YOUR responsibility.

Troubleshooting & tips:

1. If the scanner prints no open ports:
  a. Ensure the target is reachable (ping -c 3 <target>).
  b. Try increasing --timeout to 1.0 or 1.5.
  c. Reduce --workers if your VM or network becomes overloaded.
2. If you see permission denied for low ports, you can use sudo (rarely needed for connect scans).
3. For noisy / evasive services, banner grabbing with a simple recv() may return nothing — service may require a protocol handshake.
4. CSV empty or missing: check scanner.py was run with the same --csv filename as you pass to report_gen.py.

Enhancements & next steps (ideas)

1. Add UDP scanning (careful: UDP scanning is trickier due to lack of response).
2. Add service/version detection (send protocol-specific probes; integrate with a signature DB).
3. OS fingerprinting (passive fingerprints from banners or use TCP fingerprinting).
4. Create a GUI (Tkinter / PyQt) to visualize results.
5. Export to PDF or generate a nicer HTML report.
6. Integrate with nmap for cross-validation (educational only).
7. Add tests and small CI pipeline to validate scripts.
