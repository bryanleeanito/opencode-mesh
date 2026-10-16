#!/usr/bin/env python3
"""sync.py — Sinkronisasi state antar mesin OpenCode Mesh.

Usage:
    python3 sync.py --pull     # Pull update dari git
    python3 sync.py --push     # Push update ke git
    python3 sync.py --status   # Lihat status sync
"""
import argparse, json, os, subprocess, sys
from datetime import datetime

STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "state")
STATE_DIR = os.path.abspath(STATE_DIR)

def load_state(filename):
    path = os.path.join(STATE_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_state(filename, data):
    os.makedirs(STATE_DIR, exist_ok=True)
    path = os.path.join(STATE_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def git_pull():
    print("[*] Pulling updates from git...")
    try:
        r = subprocess.run(["git", "pull", "--rebase"], capture_output=True, text=True)
        if r.returncode == 0:
            print("[+] Pull successful")
            return True
        else:
            print(f"[-] Pull failed: {r.stderr}")
            return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def git_push():
    print("[*] Pushing updates to git...")
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"mesh-sync: {timestamp}"], check=True)
        r = subprocess.run(["git", "push"], capture_output=True, text=True)
        if r.returncode == 0:
            print("[+] Push successful")
            return True
        else:
            print(f"[-] Push failed: {r.stderr}")
            return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def show_status():
    print("[*] Mesh sync status")
    print()
    for f in ["tasks.json", "findings.json", "ideas.json", "status.json"]:
        data = load_state(f)
        count = len(data) if isinstance(data, (list, dict)) else 0
        print(f"  {f:20} {count} entries")
    print()
    # Git status
    try:
        r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        if r.stdout.strip():
            print("[*] Git changes:")
            for line in r.stdout.strip().split("\n"):
                print(f"  {line}")
        else:
            print("[*] Git: clean")
    except:
        pass

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "--pull":
        git_pull()
    elif cmd == "--push":
        git_push()
    elif cmd == "--status":
        show_status()
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
