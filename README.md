# 🛰️ CISA KEV Tracker

A live, self-updating dashboard that tracks the U.S. Cybersecurity & Infrastructure Security Agency's (CISA) catalog of vulnerabilities confirmed to be actively exploited in the wild — refreshed automatically every day, with zero manual maintenance.

**🔗 Live Dashboard:** https://mahakkhan16.github.io/cisa-kev-dashboard/

---

## What Is the KEV Catalog?

CISA's Known Exploited Vulnerabilities (KEV) catalog is the U.S. federal government's authoritative list of vulnerabilities that are **already being exploited by real attackers**, not just theoretically dangerous ones. Under Binding Operational Directive 22-01, every federal civilian agency is legally required to patch KEV entries by their assigned deadline. It's one of the most trusted, high-signal sources in the entire security industry — unlike raw CVE databases, which can list thousands of vulnerabilities that are never actually exploited, everything on the KEV list is real, confirmed, active risk.

This project pulls that live feed daily and turns it into a readable, at-a-glance dashboard.

## What It Does

1. A scheduled script fetches CISA's official KEV JSON feed
2. Processes it into meaningful insights: total catalog size, newly added vulnerabilities, vendors with the most exploited products, vulnerabilities linked to active ransomware campaigns, and entries past their federal remediation deadline
3. Saves the processed data as a JSON snapshot
4. A static dashboard reads that snapshot and displays it visually
5. A GitHub Actions workflow re-runs this entire pipeline daily, automatically committing fresh data — the site updates itself with no human intervention

## Tech Stack

| Layer | Tool |
|---|---|
| Data fetching & processing | Python, `requests` |
| Data source | [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (public, official feed) |
| Dashboard | Static HTML, CSS, vanilla JavaScript |
| Automation | GitHub Actions (scheduled daily) |
| Hosting | GitHub Pages |

## Why It's Built This Way

Government data feeds typically don't allow direct browser-side fetching due to CORS restrictions, so rather than trying to call CISA's servers live from the dashboard, this project fetches the data server-side (via GitHub Actions), processes it, and commits a static snapshot the dashboard reads instead. This keeps the site fast, reliable, and free to host — no backend server, no API keys, no database.

## Project Structure

```
cisa-kev-dashboard/
│
├── scripts/
│   └── fetch_kev.py          # fetches and processes the live CISA KEV feed
│
├── docs/
│   ├── index.html            # the dashboard (served via GitHub Pages)
│   └── data.json             # processed snapshot, auto-updated daily
│
├── .github/workflows/
│   └── refresh.yml           # daily automated data refresh
│
└── README.md
```

## Running Locally

```bash
git clone https://github.com/mahakkhan16/cisa-kev-dashboard.git
cd cisa-kev-dashboard
python -m venv venv
venv\Scripts\activate        # Windows
pip install requests

python scripts/fetch_kev.py   # generates docs/data.json

cd docs
python -m http.server 8000
```
Then visit `http://localhost:8000`

## Automation

`refresh.yml` runs daily (and can be triggered manually from the Actions tab) to:
1. Re-fetch the latest CISA KEV data
2. Recompute all dashboard statistics
3. Commit the updated `data.json` back to the repo, which GitHub Pages then serves automatically

## What I Learned

This project pushed me past working with static or simulated datasets into pulling and processing a real, live, authoritative government data feed. I learned to work around real-world constraints like CORS restrictions by shifting data fetching server-side, and to build a genuinely autonomous system: once deployed, this dashboard requires no manual updates to stay current — the automation does that on its own, every day.

## Future Improvements

- Add historical trend charts (entries added per week/month over time)
- Add search/filter functionality by vendor or CVE ID
- Add email or Slack alerts when a new ransomware-linked vulnerability is added
- Cross-reference with EPSS (Exploit Prediction Scoring System) scores for deeper risk context

---

Built by **Mahak Khan** — [LinkedIn](https://linkedin.com/in/mahak-khan-50ba99270)

*This is an independent project and is not affiliated with or endorsed by CISA. Data is sourced from CISA's public KEV catalog feed.*
