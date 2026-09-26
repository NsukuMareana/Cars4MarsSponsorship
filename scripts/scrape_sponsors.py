import csv
import os
import re
import time
import requests
from urllib.parse import urlparse
from dotenv import dotenv_values

SPONSORS_FILE = 'data/master_sponsors.csv'
FIELDS = ["company", "contact", "category", "tier", "sent", "replied"]

cfg = dotenv_values('.env')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or cfg.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID') or cfg.get('GOOGLE_CSE_ID')

# ── Search queries targeting robotics & coding companies in Africa ──
SEARCH_QUERIES = [
    "robotics company Africa contact email",
    "robotics startup South Africa email",
    "robotics startup Kenya contact",
    "robotics startup Nigeria email",
    "coding academy South Africa contact",
    "coding bootcamp Africa email",
    "coding school Kenya contact",
    "STEM education robotics Africa contact",
    "drone company Africa contact email",
    "automation company South Africa contact",
    "AI robotics company Africa email",
    "mechatronics company South Africa contact",
]

# ── Email regex: matches common contact addresses ──
EMAIL_REGEX = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
)

# ── Emails to ignore (generic, non-actionable) ──
BAD_EMAILS = {
    'example@example.com', 'test@test.com', 'noreply@',
    'no-reply@', 'donotreply@', 'privacy@', 'legal@',
    'abuse@', 'webmaster@', 'postmaster@', 'admin@localhost',
}

def is_bad_email(email):
    lower = email.lower()
    return any(bad in lower for bad in BAD_EMAILS)

def load_existing():
    """Load existing sponsors to avoid duplicates."""
    existing = set()
    if os.path.exists(SPONSORS_FILE):
        with open(SPONSORS_FILE, 'r') as f:
            for row in csv.DictReader(f):
                existing.add(row['company'].lower().strip())
    return existing

def google_search(query, num=10):
    """Run a Google Custom Search API query."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("⚠️  No Google API keys found — skipping search")
        return []
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'num': num,
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get('items', [])
    except Exception as e:
        print(f"⚠️  Search failed for '{query}': {e}")
        return []

def extract_emails_from_site(url):
    """Visit a website and extract contact emails."""
    emails = set()
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Cars4MarsBot/1.0)'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return emails
        # Look for mailto: links first (most reliable)
        for match in re.findall(r'mailto:([^"\'>\s]+)', r.text):
            emails.add(match.lower())
        # Fallback: scan raw HTML for email patterns
        for match in EMAIL_REGEX.findall(r.text):
            emails.add(match.lower())
    except Exception:
        pass
    return {e for e in emails if not is_bad_email(e)}

def add_sponsor(company, contact, category, tier="Silver"):
    """Append a new sponsor to the CSV."""
    with open(SPONSORS_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({
            "company": company,
            "contact": contact,
            "category": category,
            "tier": tier,
            "sent": "no",
            "replied": "no",
        })

def init_csv():
    """Initialise the CSV with seed sponsors if it doesn't exist."""
    if not os.path.exists(SPONSORS_FILE):
        os.makedirs('data', exist_ok=True)
        seed = [
            {"company": "BATTALION Technologies", "contact": "info@battaliontech.co.za", "category": "Robotics", "tier": "Platinum"},
            {"company": "Directech (Pty) Ltd", "contact": "info@directech.co.za", "category": "Robotics", "tier": "Gold"},
            {"company": "ZeroBionic", "contact": "zerobionicteam@gmail.com", "category": "Robotics", "tier": "Gold"},
            {"company": "Terra Industries", "contact": "info@terraindustries.co", "category": "Robotics", "tier": "Platinum"},
            {"company": "Raedbots", "contact": "info@raedbots.com", "category": "Robotics", "tier": "Silver"},
            {"company": "Arone Technologies", "contact": "info@aronetech.com", "category": "Robotics", "tier": "Silver"},
            {"company": "WeThinkCode", "contact": "chris@wethinkcode.co.za", "category": "Coding Education", "tier": "Platinum"},
            {"company": "codeX", "contact": "info@projectcodex.co", "category": "Coding Education", "tier": "Gold"},
            {"company": "HyperionDev", "contact": "contact@hyperiondev.com", "category": "Coding Education", "tier": "Gold"},
            {"company": "Umuzi.org", "contact": "rivoningo.maphophe@umuzi.org", "category": "Coding Education", "tier": "Gold"},
            {"company": "Codetrain Africa", "contact": "admissions@codetrainafrica.com", "category": "Coding Education", "tier": "Gold"},
            {"company": "Zaio", "contact": "info@zaio.io", "category": "Coding Education", "tier": "Silver"},
            {"company": "redAcademy", "contact": "info@redacademy.co.za", "category": "Coding Education", "tier": "Silver"},
            {"company": "AmaliTech", "contact": "info@amalitech.com", "category": "Coding Education", "tier": "Silver"},
            {"company": "Aptiv", "contact": "africa@aptiv.com", "category": "Robotics (Global)", "tier": "Platinum"},
            {"company": "John Deere", "contact": "Africa@JohnDeere.com", "category": "Robotics (Global)", "tier": "Platinum"},
            {"company": "Rockwell Automation", "contact": "CustomerCareZA@ra.rockwell.com", "category": "Robotics (Global)", "tier": "Gold"},
            {"company": "Honeywell", "contact": "hsa@honeywell.com", "category": "STEM Education", "tier": "Platinum"},
            {"company": "Siemens", "contact": "automation.za@siemens.com", "category": "STEM Education", "tier": "Platinum"},
            {"company": "Telkom Foundation", "contact": "telkom.foundation@telkom.co.za", "category": "STEM Education", "tier": "Gold"},
            {"company": "Epiroc South Africa", "contact": "customer.care@epiroc.com", "category": "STEM Education", "tier": "Gold"},
            {"company": "Creality / SMD Technologies", "contact": "info@smd.co.za", "category": "Hardware", "tier": "Platinum"},
            {"company": "RS Components SA", "contact": "southafrica@rs-components.com", "category": "Electronics", "tier": "Gold"},
            {"company": "SIMTEQ Engineering", "contact": "Gael@Simteq.co.za", "category": "Software", "tier": "Gold"},
        ]
        with open(SPONSORS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for s in seed:
                s["sent"] = "no"
                s["replied"] = "no"
                writer.writerow(s)
        print(f"✅ Initialised {SPONSORS_FILE} with {len(seed)} seed sponsors.")

def discover_sponsors():
    """Run intensive Google searches and add new companies."""
    existing = load_existing()
    print(f"📋 Existing sponsors: {len(existing)}")
    new_count = 0

    for query in SEARCH_QUERIES:
        print(f"\n🔍 Searching: {query}")
        results = google_search(query)
        for item in results:
            title = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')

            # Extract company name from title
            company_name = title.split('|')[0].split('-')[0].strip()
            if not company_name or len(company_name) < 3:
                continue
            if company_name.lower() in existing:
                continue

            # Try to extract email from the snippet first
            emails = EMAIL_REGEX.findall(snippet)
            # Then scrape the actual website
            if link:
                site_emails = extract_emails_from_site(link)
                emails.extend(site_emails)

            # Pick the best email
            if emails:
                # Prefer info@, contact@, hello@
                best = None
                for e in emails:
                    if e.startswith(('info@', 'contact@', 'hello@')):
                        best = e
                        break
                if not best:
                    best = emails[0]

                # Determine category from query
                if 'coding' in query.lower():
                    category = "Coding Education"
                elif 'robotics' in query.lower():
                    category = "Robotics"
                else:
                    category = "STEM Education"

                add_sponsor(company_name, best, category)
                existing.add(company_name.lower())
                new_count += 1
                print(f"  ✅ Added: {company_name} → {best}")
            time.sleep(1)  # be polite

    print(f"\n🎉 Done. Added {new_count} new sponsors.")

if __name__ == "__main__":
    init_csv()
    discover_sponsors()
