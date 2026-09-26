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

def get_subject(company, category):
    if category == "Robotics":
        return f"Partnership: Africa's next robotics engineers"
    elif category == "Coding Education":
        return f"Partnership: Your graduates mentoring Mars rover teams"
    elif category == "Robotics (Global)":
        return f"Partnership: Extend your robotics impact to Africa"
    elif category == "STEM Education":
        return f"Partnership: Showcase your STEM impact with Cars4Mars"
    elif category in ["Hardware", "Electronics", "Software"]:
        return f"Partnership: Your products power Africa's Mars rovers"
    else:
        return f"Cars4Mars Partnership Opportunity for {company}"

def get_body(company, tier, category):
    if category == "Robotics":
        return f"""Dear {company} Team,

I came across your work in robotics and it perfectly reflects what Cars4Mars is building.

Cars4Mars is Africa's only Mars rover competition. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes, with 18 finalist teams competing at SANSA's Mars Yard. Your work in robotics aligns directly with our mission.

We're inviting {company} to partner with us for the 2027 edition as a {tier} Sponsor. Your support would help develop the next generation of robotics engineers — the exact talent pipeline your company needs.

Would you be open to a 15-minute call next week?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za"""

    elif category == "Coding Education":
        return f"""Dear {company} Team,

I've been following {company}'s work in coding education and believe there's a natural partnership with Cars4Mars.

Cars4Mars is Africa's only Mars rover competition. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes. Your graduates are exactly the coding mentors our student teams need.

We're inviting {company} to partner as a {tier} Sponsor. Your support would connect your alumni with Africa's brightest young engineers — and give your brand visibility across 11 countries.

Would you be open to a 15-minute call next week?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za"""

    elif category == "Robotics (Global)":
        return f"""Dear {company} Team,

I know {company} has invested significantly in robotics education globally. I'd like to invite you to extend that impact to Africa's only Mars rover competition.

Cars4Mars is Africa's only Mars rover competition. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes, with 18 finalist teams competing at SANSA's Mars Yard.

We're inviting {company} to partner as a {tier} Sponsor for 2027. This is a natural extension of your existing STEM commitment in Africa.

Would you be open to a 30-minute call to explore this?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za"""

    elif category == "STEM Education":
        return f"""Dear {company} Team,

I've seen {company}'s commitment to STEM education in Africa. Cars4Mars is a natural platform to amplify that impact.

Cars4Mars is Africa's only Mars rover competition. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes. Your existing CSI investment in STEM makes this a perfect alignment.

We're inviting {company} to partner as a {tier} Sponsor for 2027. Your support would directly reach the same students your programmes already serve.

Would you be open to a 15-minute call next week?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za"""

    else:
        return f"""Dear {company} Team,

I'm reaching out from Cars4Mars, Africa's only Mars rover competition for high school and university students. In 2026, 100 teams from 11 African countries designed and built Mars rover prototypes, with 18 finalist teams competing at SANSA's Mars Yard.

We're inviting {company} to partner with us for the 2027 edition as a {tier} Sponsor.

Would you be open to a 15-minute call next week to explore this?

Best regards,
Cars4Mars Sponsorship Team
www.cars4mars.co.za"""

def send_email(to_email, company, tier, category):
    subject = get_subject(company, category)
    body = get_body(company, tier, category)
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
                    send_email(row['contact'], row['company'], row['tier'], row['category'])
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
