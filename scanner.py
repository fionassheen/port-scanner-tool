#!/usr/bin/env python3
"""
scanner.py
Simple multi-threaded TCP port scanner with banner grabbing and CSV output.
Safe to run against localhost or lab VMs only.
"""
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import csv

DEFAULT_TIMEOUT = 0.8

def scan_port(ip, port, timeout=DEFAULT_TIMEOUT):
    result = {"port": port, "open": False, "banner": "", "service": ""}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        code = sock.connect_ex((ip, port))
        if code == 0:
            result["open"] = True
            # try grabbing banner
            try:
                sock.sendall(b"\r\n")
            except Exception:
                pass
            try:
                data = sock.recv(2048)
                banner = data.decode(errors="ignore").strip()
                result["banner"] = banner[:200]  # limit length
            except Exception:
                result["banner"] = ""
        sock.close()
    except Exception as e:
        result["banner"] = f"err:{e}"
    return result

def parse_ports(ports_str):
    ports = set()
    for part in ports_str.split(','):
        part = part.strip()
        if '-' in part:
            a,b = part.split('-',1)
            ports.update(range(int(a), int(b)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def write_csv(results, csvfile):
    now = datetime.now().isoformat()
    with open(csvfile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","ip","port","open","service","banner"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "timestamp": now,
                "ip": r.get("ip"),
                "port": r["port"],
                "open": r["open"],
                "service": r.get("service",""),
                "banner": r["banner"]
            })

def main():
    parser = argparse.ArgumentParser(description="Simple multi-threaded TCP port scanner (lab use only).")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("--ports", "-p", default="1-1024", help="Ports to scan (e.g. 22,80,443 or 1-1024)")
    parser.add_argument("--workers", "-w", type=int, default=100, help="Max concurrent threads")
    parser.add_argument("--timeout", "-t", type=float, default=DEFAULT_TIMEOUT, help="Socket timeout seconds")
    parser.add_argument("--csv", default="scan_results.csv", help="CSV output filename")
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.target)
    except Exception as e:
        print(f"Cannot resolve target '{args.target}': {e}")
        return

    ports = parse_ports(args.ports)
    print(f"Scanning {ip} ({args.target}) ports: {len(ports)} ports with {args.workers} workers, timeout {args.timeout}s")

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as exe:
        futures = { exe.submit(scan_port, ip, p, args.timeout): p for p in ports }
        for fut in as_completed(futures):
            r = fut.result()
            r["ip"] = ip
            results.append(r)
            if r["open"]:
                print(f"[OPEN] {r['port']:5}  banner: {r['banner'][:80]}")
    # sort results by port
    results_sorted = sorted(results, key=lambda x: x["port"])

    # write CSV
    write_csv(results_sorted, args.csv)
    print(f"Scan complete. Results saved to {args.csv}")

if __name__ == "__main__":
    main()
