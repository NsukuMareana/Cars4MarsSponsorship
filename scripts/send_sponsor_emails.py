import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values

cfg = dotenv_values('.env')
user = cfg.get('UCT_EMAIL') or os.environ.get('UCT_EMAIL')
password = cfg.get('UCT_PASSWORD') or os.environ.get('UCT_PASSWORD')

SPONSORS_FILE = 'data/master_sponsors.csv'
FIELDS = ["company", "contact", "category", "tier", "sent", "replied"]

def send_email(to_email, company, tier):
    subject = f"Cars4Mars African Rover Challenge — Partnership Opportunity for {company}"
    body = f"""Dear {company} Team,

I'm reaching out from Cars4Mars, Africa's only Mars rover competition for high school and university students. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes, with 18 finalist teams competing at SANSA's Mars Yard.

We're inviting {company} to partner with us for the 2027 edition as a {tier} Sponsor. Your support would directly help develop Africa's next generation of engineers, robotics specialists, and space technologists.

Would you be open to a 15-minute call next week to explore this?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za
"""
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(user, password)
        server.send_message(msg)

def main():
    if not user or not password:
        print("No credentials found. Skipping send.")
        return

    rows = []
    with open(SPONSORS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['sent'] == 'no':
                try:
                    send_email(row['contact'], row['company'], row['tier'])
                    row['sent'] = 'yes'
                    print(f"Sent to {row['company']} ({row['contact']})")
                except Exception as e:
                    print(f"Failed to send to {row['company']}: {e}")
            rows.append(row)

    with open(SPONSORS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
