import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from settings import config


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
URL = "https://www.pararius.nl/huurwoningen/rotterdam/1000-2250"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = config.app.EMAIL_USERNAME
EMAIL_PASSWORD = config.app.EMAIL_PASSWORD
TO_EMAILS = [EMAIL_USERNAME]  # List of email addresses

# Get the directory where this .py file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "assets/known_postings.json")


# Helper functions for persistence
def load_known_postings(file_path=JSON_PATH):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r") as f:
        data = json.load(f)
        return set(data)


def save_known_postings(postings_set, file_path=JSON_PATH):
    with open(file_path, "w") as f:
        json.dump(list(postings_set), f)


def send_email(new_listings):
    subject = "[Kratos] New Rental Postings Found in Rotterdam <3"
    body = "The following new listings were found:\n\n"
    for title, link in new_listings:
        body += f"{title}\n{link}\n\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = ", ".join(
        TO_EMAILS
    )  # Join the list of emails into a comma-separated string
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            # Send email to each recipient
            for recipient in TO_EMAILS:
                server.sendmail(EMAIL_USERNAME, recipient, msg.as_string())
        print("Email sent successfully to all recipients!")
    except Exception as e:
        print("Failed to send email:", e)


def scrape_pararius():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []
    listing_items = soup.find_all(
        "li", class_="search-list__item search-list__item--listing"
    )
    for item in listing_items:
        link_tag = item.find("a", class_="listing-search-item__link")
        if not link_tag:
            continue
        title = link_tag.get_text(strip=True)
        listing_url = "https://www.pararius.nl" + link_tag.get("href", "")
        listings.append((title, listing_url))

    return listings


def main():
    # 1. Load previously known postings from file
    known_postings = load_known_postings()

    # 2. Scrape the site
    current_listings = scrape_pararius()

    # 3. Determine which listings are new
    new_listings = []
    for title, link in current_listings:
        if link not in known_postings:
            new_listings.append((title, link))
            known_postings.add(link)

    # 4. If we have new listings, send email notification
    if new_listings:
        send_email(new_listings)
        # 5. Save the updated known_postings to file
        save_known_postings(known_postings)
    else:
        print("No new listings found.")
