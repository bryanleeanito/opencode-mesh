#!/usr/bin/env python3
"""E2E tests untuk opencode-mesh router."""
import subprocess, sys, os, json, tempfile, shutil

MESH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTER = os.path.join(MESH_DIR, "router")

def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(ROUTER, script), *args],
                       capture_output=True, text=True, timeout=10)
    return r.returncode, r.stdout, r.stderr

def test_sync_status():
    rc, out, _ = run("sync.py", "--status")
    assert rc == 0
    assert "sync status" in out.lower() or "entries" in out
    print("[PASS] sync status")

def test_delegate():
    rc, out, _ = run("delegate.py", "--to", "school", "--task", "test bypass")
    assert rc == 0
    assert "Task" in out
    print("[PASS] delegate")

def test_delegate_list():
    rc, out, _ = run("delegate.py", "--list")
    assert rc == 0
    assert "Tasks" in out
    print("[PASS] delegate list")

def test_ideas_add():
    rc, out, _ = run("ideas.py", "--add", "test idea from mesh")
    assert rc == 0
    assert "Idea" in out
    print("[PASS] ideas add")

def test_ideas_list():
    rc, out, _ = run("ideas.py", "--list")
    assert rc == 0
    assert "Ideas" in out
    print("[PASS] ideas list")

def test_share_finding():
    rc, out, _ = run("share.py", "--type", "finding", "--message", "test finding")
    assert rc == 0
    assert "FINDING" in out
    print("[PASS] share finding")

def test_share_list():
    rc, out, _ = run("share.py", "--list")
    assert rc == 0
    assert "Findings" in out
    print("[PASS] share list")

if __name__ == "__main__":
    test_sync_status()
    test_delegate()
    test_delegate_list()
    test_ideas_add()
    test_ideas_list()
    test_share_finding()
    test_share_list()
    print("\n=== SEMUA TEST LULUS (7/7) ===")
