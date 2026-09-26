# Cars4Mars Sponsorship Outreach

Automated sponsor outreach for the Cars4Mars African Rover Challenge.
Runs daily at 08:00 & 14:00 SAST from 1 January 2027.

## Structure
- scripts/scrape_sponsors.py       — seeds data/master_sponsors.csv
- scripts/send_sponsor_emails.py   — sends outreach via Gmail SMTP
- scripts/check_replies.py         — tracks replies and updates CSV
- scripts/cleanup_sponsor_emails.py — deletes unreplied sent emails > 2 days old

## Setup
1. Add secrets UCT_EMAIL and UCT_PASSWORD in repo Settings -> Secrets -> Actions.
2. Enable Actions.
3. Manual test: Actions -> Cars4Mars Sponsor Outreach -> Run workflow.
