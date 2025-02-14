from datetime import date
import json
import smtplib
from email.mime.text import MIMEText

today = date.today()
day = today.strftime("%B %d, %Y")

def parse_and_send(filename):    
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

        filterKeywords = ["Software Engineer", "Frontend Engineer", "Researcher", "Analyst"] #set an array of keywords and have fun
        filtered_jobs = [] #leave empty

        mainsiteURL = "https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers" #this is the common part to any JD at CrowdStrike - you can change this

        for job in data:
            title = job.get("title", "N/A")
            location = job.get("locations", [{}])[0].get("displayName", "United Kingdom")
            externalPath = job.get('externalPath', '')
            job_url = f"{mainsiteURL}{externalPath}" #recreating the full job URL
            if any(keyword.lower() in title.lower() for keyword in filterKeywords) and ("United-Kingdom" in externalPath):
                filtered_jobs.append(f'<li>📌 <a href="{job_url}" target="_blank">{title}</a> - 📍 {location}</li>')

    if filtered_jobs:
        email_body = f"""
            <html>
            <body>
                <h2> {day} - 💻 New Jobs at ... for you!  👨🏼‍💻</h2>
                <ul>
                    {''.join(filtered_jobs)}
                </ul>
                <p>📢 Script developed by https://github.com/YorOdinSon!</p>
            </body>
            </html>
        """
    else:
        email_body = "<p>No matching jobs found.</p>"

    # Email Config (replace with actual credentials)
    SMTP_SERVER = "smtp.gmail.com" #used the gmail one for me
    SMTP_PORT = 587
    SENDER_EMAIL = "-----" 
    SENDER_PASSWORD = "-----"  # Use App Password
    RECIPIENT_EMAIL = "-----" # this would go in the To: of your email
    BCC_EMAIL = "" # there is no BCC, but if you don't specify it in the msg['To'] variable, it still sends the message to the recipient, but it won't show in the final message
    SUBJECT = f"😎Hey, ....!! 🔥 New Job Postings @ ....!!! 🧑🏼‍💻"

    # Send Email
    msg = MIMEText(email_body, "html")  # Set email type to HTML - otherwise it will send messages in a string format
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL 
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