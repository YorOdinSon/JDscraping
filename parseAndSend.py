from datetime import date
import json
import smtplib
from email.mime.text import MIMEText

def parse_and_send(filename):    
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

        filterKeywords = ["Software Engineer", "Frontend Engineer", "Researcher", "Analyst"]
        filtered_jobs = []

        mainsiteURL = "https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers"

        for job in data:
            title = job.get("title", "N/A")
            location = job.get("locations", [{}])[0].get("displayName", "United Kingdom")
            externalPath = job.get('externalPath', '')
            job_url = f"{mainsiteURL}{externalPath}" #recreating the full job URL
            if any(keyword.lower() in title.lower() for keyword in filterKeywords) and ("United Kingdom" in location or "United-Kingdom---Remote" in externalPath):
                filtered_jobs.append(f'<li>📌 <a href="{job_url}" target="_blank">{title}</a> - 📍 {location}</li>')

    if filtered_jobs:
        email_body = f"""
            <html>
            <body>
                <h2> 💻 New Job Listings at CrowdStrike 👨🏼‍💻</h2>
                <ul>
                    {''.join(filtered_jobs)}
                </ul>
                <p>📢 Script developed by Yor Himself!</p>
            </body>
            </html>
        """
    else:
        email_body = "<p>No matching jobs found.</p>"

    # Email Config (replace with actual credentials)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "kurtcob@gmail.com"
    SENDER_PASSWORD = "fwyh flzg zbwl fxop"  # Use App Password
    RECIPIENT_EMAIL = "yor.francavilla@gmail.com"
    BCC_EMAIL = "" 
    SUBJECT = "😎Hey, Yor! 🔥 New Job Postings@ CrowdStrike Matching Your Criteria!!! 🧑🏼‍💻"

    # Send Email
    msg = MIMEText(email_body, "html")  # Set email type to HTML - otherwise it will send messages in a string format
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER_EMAIL
    #msg["To"] = RECIPIENT_EMAIL 
#if msg["To"] isn't specified, then the email.mime.text will leave it blank, just as if it was a BCC - uncomment the previous line if the main recipient has to be visible
    try:
        recipients = [RECIPIENT_EMAIL, BCC_EMAIL]
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
        print("📧 ✅ Email Sent Successfully! 👨🏼‍💻 Please check your Inbox! 📩")
    except Exception as e:
        print(f"❌ Email failed: {e}")