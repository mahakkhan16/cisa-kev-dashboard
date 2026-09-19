import requests
import json
import os
from datetime import datetime, date, timezone
from collections import Counter

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def fetch_kev_data():
    response = requests.get(KEV_URL, timeout=30)
    response.raise_for_status()
    return response.json()

def build_dashboard_data(raw):
    vulns = raw["vulnerabilities"]
    today = date.today()

    vulns_sorted = sorted(vulns, key=lambda v: v["dateAdded"], reverse=True)
    recent = []
    for v in vulns_sorted[:15]:
        recent.append({
            "cveID": v.get("cveID"),
            "vendorProject": v.get("vendorProject"),
            "product": v.get("product"),
            "vulnerabilityName": v.get("vulnerabilityName"),
            "dateAdded": v.get("dateAdded"),
            "dueDate": v.get("dueDate"),
            "shortDescription": v.get("shortDescription"),
            "knownRansomwareCampaignUse": v.get("knownRansomwareCampaignUse", "Unknown"),
        })

    vendor_counts = Counter(v.get("vendorProject", "Unknown") for v in vulns)
    top_vendors = vendor_counts.most_common(10)

    ransomware_count = sum(
        1 for v in vulns if v.get("knownRansomwareCampaignUse", "").lower() == "known"
    )
    overdue_count = 0
    for v in vulns:
        due = v.get("dueDate")
        if due:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if due_date < today:
                    overdue_count += 1
            except ValueError:
                pass

    from datetime import timedelta
    thirty_days_ago = today - timedelta(days=30)
    added_last_30 = 0
    for v in vulns:
        added = v.get("dateAdded")
        if added:
            try:
                added_date = datetime.strptime(added, "%Y-%m-%d").date()
                if added_date >= thirty_days_ago:
                    added_last_30 += 1
            except ValueError:
                pass

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "catalogVersion": raw.get("catalogVersion"),
        "dateReleased": raw.get("dateReleased"),
        "totalCount": len(vulns),
        "addedLast30Days": added_last_30,
        "ransomwareLinkedCount": ransomware_count,
        "overdueCount": overdue_count,
        "topVendors": [{"vendor": v, "count": c} for v, c in top_vendors],
        "recentEntries": recent,
    }

if __name__ == "__main__":
    print("Fetching CISA KEV catalog...")
    raw = fetch_kev_data()
    print(f"Fetched {len(raw['vulnerabilities'])} total vulnerabilities")

    dashboard_data = build_dashboard_data(raw)

    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)

    print("Saved processed data to docs/data.json")
    print(f"Added in last 30 days: {dashboard_data['addedLast30Days']}")
    print(f"Ransomware-linked: {dashboard_data['ransomwareLinkedCount']}")
    print(f"Overdue: {dashboard_data['overdueCount']}")