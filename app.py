from flask import Flask, render_template, request
import os
import smtplib
from email.mime.text import MIMEText
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/')
def index():
    skills = ['Baking', 'Hairdressing', 'Solar Installation', 'Photography', 'Hair Tying']
    return render_template('index.html', skills=skills)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip().capitalize()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    skill = request.form.get('skill')

    if not name or not phone or not skill:
        return "Please fill in all required fields.", 400

    # Save to Google Sheet instead of CSV
    save_to_google_sheet(name, phone, email, skill)

    # Send confirmation email if email is provided
    if email:
        send_confirmation_email(name, email, skill)

    return render_template('confirmation.html', name=name, skill=skill)

@app.route('/policy')
def policy():
    return render_template('policy.html')

def save_to_google_sheet(name, phone, email, skill):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    google_creds = json.loads(os.getenv('GOOGLE_CREDS'))  # Read from environment
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)

    client = gspread.authorize(creds)
    sheet = client.open_by_key("1FBXc05XSs1K_5qhSyAC_jjW4YhR2_CKevee9hNROIpI").sheet1
    sheet.append_row([name, phone, email, skill])

def send_confirmation_email(name, email, skill):
    subject = "Skill Acquisition Program Registration"
    message = f"Dear {name},\n\nThank you for registering for the {skill} training program.\n\nBlessings,\nSTEM Team"
    
    sender = "jglory995@gmail.com"
    password = "gcmd uelw ymuc gnuy"
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)
