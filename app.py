from flask import Flask, render_template, request
import os
import csv
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

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

    # Save to CSV
    with open("data/submissions.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, email, skill])

    # Send confirmation email if email is provided
    if email:
        send_confirmation_email(name, email, skill)

    return render_template('confirmation.html', name=name, skill=skill)

@app.route('/policy')
def policy():
    return render_template('policy.html')

def send_confirmation_email(name, email, skill):
    subject = "Skill Acquisition Program Registration"
    message = f"Dear {name},\n\nThank you for registering for the {skill} training program.\n\nBlessings,\nSTEM Team"
    
    # Email config (set real credentials)
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
