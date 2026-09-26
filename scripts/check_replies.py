import imaplib
import csv
import os
from dotenv import dotenv_values

cfg = dotenv_values('.env')
user = cfg.get('UCT_EMAIL') or os.environ.get('UCT_EMAIL')
password = cfg.get('UCT_PASSWORD') or os.environ.get('UCT_PASSWORD')

SPONSORS_FILE = 'data/master_sponsors.csv'
FIELDS = ["company", "contact", "category", "tier", "sent", "replied"]

def main():
    if not user or not password:
        print("No credentials. Skipping reply check.")
        return

    M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    M.login(user, password)
    M.select('"[Gmail]/All Mail"')

    rows = []
    with open(SPONSORS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['replied'] == 'yes':
                rows.append(row)
                continue
            typ, data = M.search(None, 'FROM', f'"{row["contact"]}"')
            if typ == 'OK' and data[0].split():
                row['replied'] = 'yes'
                print(f"Reply found from {row['company']}")
            rows.append(row)

    with open(SPONSORS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    M.logout()

if __name__ == "__main__":
    main()
