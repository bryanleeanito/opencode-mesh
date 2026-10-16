# OpenCode Mesh

Framework kolaborasi 3 mesin OpenCode: Tablet (analisa) ↔ School (lapangan) ↔ Windows (dev).
Dibuat 2026-10-16.

## Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                   OPENCOD MESH                          │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │  Tablet  │◄──►│  School  │◄──►│ Windows  │         │
│  │ (Analisa)│    │ (Lapangan)│   │  (Dev)   │         │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘         │
│       │               │               │                │
│       └───────────────┼───────────────┘                │
│                       ▼                                │
│            ┌─────────────────┐                         │
│            │  Shared State   │                         │
│            │  (Git + SQLite) │                         │
│            └─────────────────┘                         │
│                       ▼                                │
│            ┌─────────────────┐                         │
│            │  Task Router    │                         │
│            │  (delegasi job) │                         │
│            └─────────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

## Mesin & Peran

| Mesin | Peran | Kategori Kit |
|---|---|---|
| **Kali Linux** | Attack & Eksekusi — pentest, bypass, exploit, payload, scanning | waf-bypass, sqli-helper, payload-generator, firewall-bypass |
| **Tablet** | Specialist Analysis — OSINT, analisa temuan, source review, reporting | sherlock-osint, ctf-decoder, code-audit, report-packer |
| **Windows** | Specialist Development + DevOps — build, deploy, automasi | windev-specialist, security-protect, extreme-efficiency |

## Cara Pakai

### 1. Sync State

```bash
# Pull update dari mesin lain
python3 router/sync.py --pull

# Push update ke mesin lain
python3 router/sync.py --push
```

### 2. Delegate Task

```bash
# Kirim task ke mesin lain
python3 router/delegate.py --to school --task "bypass WAF target.com"

# Lihat task masuk
python3 router/tasks.py --list
```

### 3. Share Findings

```bash
# Share temuan ke mesin lain
python3 router/share.py --type finding --message "SQLi ditemukan di /login"

# Lihat temuan dari mesin lain
python3 router/share.py --list
```

### 4. Sync Ideas (Tukar Pikiran)

```bash
# Broadcast ide ke semua mesin
python3 router/ideas.py --add "Pakai double-url encode bypass CF"

# Lihat ide dari mesin lain
python3 router/ideas.py --list
```

## Struktur

```
config/
  mesh.yaml          — konfigurasi mesh
  env.template       — template env var
state/
  tasks.json         — antrian task
  findings.json      — kumpulan temuan
  ideas.json         — tukar pikiran
  status.json        — status tiap mesin
router/
  sync.py            — sinkronisasi state
  delegate.py        — delegasi task
  share.py           — share findings
  ideas.py           — tukar pikiran
  tasks.py           — manajemen task
templates/
  task.md            — template task
  finding.md         — template finding
  idea.md            — template ide
  report.md          — template laporan
```

## Aturan

1. **Satu direction of truth** — semua state sinkron lewat git.
2. **Pull before push** — selalu `sync.py --pull` sebelum `--push`.
3. **Naming convention** — `[mesin]/[type]/[timestamp]`.
4. **No secrets** — credentials di env var, jangan di state file.
5. **Redact output** — semua sensitive data di-redact.

## Changelog

- **2026-10-16** — repo dibuat, framework awal.
