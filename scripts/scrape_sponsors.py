import csv
import os

SPONSORS_FILE = 'data/master_sponsors.csv'
FIELDS = ["company", "contact", "category", "tier", "sent", "replied"]

initial_sponsors = [
    # ── African Robotics Companies ──
    {"company": "BATTALION Technologies", "contact": "info@battaliontech.co.za", "category": "Robotics", "tier": "Platinum"},
    {"company": "Directech (Pty) Ltd", "contact": "info@directech.co.za", "category": "Robotics", "tier": "Gold"},
    {"company": "ZeroBionic", "contact": "info@zerobionicafrica.com", "category": "Robotics", "tier": "Gold"},
    {"company": "Terra Industries", "contact": "info@terraindustries.africa", "category": "Robotics", "tier": "Platinum"},
    {"company": "Raedbots", "contact": "info@raedbots.com", "category": "Robotics", "tier": "Silver"},
    {"company": "Arone Technologies", "contact": "info@aronetech.com", "category": "Robotics", "tier": "Silver"},

    # ── Coding & Tech Education ──
    {"company": "WeThinkCode", "contact": "info@wethinkcode.co.za", "category": "Coding Education", "tier": "Platinum"},
    {"company": "codeX", "contact": "info@codex.co.za", "category": "Coding Education", "tier": "Gold"},
    {"company": "HyperionDev", "contact": "info@hyperiondev.com", "category": "Coding Education", "tier": "Gold"},
    {"company": "Umuzi.org", "contact": "info@umuzi.org", "category": "Coding Education", "tier": "Gold"},
    {"company": "Codetrain Africa", "contact": "info@codetrain.africa", "category": "Coding Education", "tier": "Gold"},
    {"company": "Zaio", "contact": "info@zaio.io", "category": "Coding Education", "tier": "Silver"},
    {"company": "redAcademy", "contact": "info@redacademy.co.za", "category": "Coding Education", "tier": "Silver"},
    {"company": "AmaliTech", "contact": "info@amalitech.com", "category": "Coding Education", "tier": "Silver"},

    # ── Global Robotics ──
    {"company": "Aptiv", "contact": "africa@aptiv.com", "category": "Robotics (Global)", "tier": "Platinum"},
    {"company": "John Deere", "contact": "africa@deere.com", "category": "Robotics (Global)", "tier": "Platinum"},
    {"company": "Rockwell Automation", "contact": "africa@rockwellautomation.com", "category": "Robotics (Global)", "tier": "Gold"},

    # ── Corporate STEM Education ──
    {"company": "Honeywell", "contact": "Vivian.Smith@Honeywell.com", "category": "STEM Education", "tier": "Platinum"},
    {"company": "Stellantis South Africa", "contact": "info@stellantis.com", "category": "STEM Education", "tier": "Platinum"},
    {"company": "Siemens", "contact": "africa@siemens.com", "category": "STEM Education", "tier": "Platinum"},
    {"company": "Telkom Foundation", "contact": "foundation@telkom.co.za", "category": "STEM Education", "tier": "Gold"},
    {"company": "Epiroc South Africa", "contact": "info@epiroc.com", "category": "STEM Education", "tier": "Gold"},

    # ── Existing Hardware Sponsors ──
    {"company": "Creality / SMD Technologies", "contact": "info@smd.co.za", "category": "Hardware", "tier": "Platinum"},
    {"company": "RS Components SA", "contact": "southafrica@rs-components.com", "category": "Electronics", "tier": "Gold"},
    {"company": "SIMTEQ Engineering", "contact": "Gael@Simteq.co.za", "category": "Software", "tier": "Gold"},
]

def init_csv():
    if not os.path.exists(SPONSORS_FILE):
        os.makedirs('data', exist_ok=True)
        with open(SPONSORS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for s in initial_sponsors:
                s["sent"] = "no"
                s["replied"] = "no"
                writer.writerow(s)
        print(f"Initialised {SPONSORS_FILE} with {len(initial_sponsors)} sponsors.")
    else:
        print(f"{SPONSORS_FILE} already exists. Skipping seed.")

if __name__ == "__main__":
    init_csv()
