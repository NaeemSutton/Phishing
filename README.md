# Phishing Simulation Project

[🎥 Watch the video walkthrough on YouTube](https://www.youtube.com/watch?v=lQbfF3DHbQY)

## Overview
This project is a phishing simulation tool designed to help organizations educate employees on recognizing phishing emails and preventing data compromise. The simulation mimics a real-world phishing scenario and provides immediate feedback to users who submit credentials.

---

## Features
- **🖥️ Realistic Login Page**: Clone of the UMass Memorial myChart portal to simulate phishing scenarios.
- **⚠️ Email Alerts**: Sends admin notifications when users interact with phishing emails.
- **🔐 Feedback Mechanism**: Users who submit credentials are redirected to a security warning page.
- **📊 Dashboard**: Interactive dashboard to view submission patterns and domain types.
- **📥 CSV Export**: Submissions can be downloaded for analysis.
- **🔒 Role-based Access Control**: Admin-only access to simulation results.
- **🎓 Training Integration**: Redirect users to phishing awareness training after detection.

---

## Technologies Used
- **Flask** – Web server and routing
- **SQLAlchemy** – ORM for database interaction
- **SQLite** – Local data storage
- **Jinja2** – HTML templating engine
- **Bootstrap** – Responsive frontend UI
- **SendGrid** – Email delivery and notifications

---

## Screenshots

### 📧 Phishing Email Sample
Fake email designed to resemble a legitimate UMass alert requesting credential verification.
![Phishing Email](images/email.png)

### 🧑‍💻 Spoofed myChart Login Page
Deceptively realistic login form used to simulate credential harvesting.
![Login Page](images/login.png)

### 🧾 SQLite Database View
Captured submission data stored in a local SQLite database.
![Database](images/database.png)

### 🚨 Feedback Page (Security Alert)
Notifies users that they fell for a phishing attempt and redirects them to training.
![Alert Page](images/training alert.png)

### 📊 Admin Dashboard
Shows submission counts and domain types over time for admin analysis.
![Dashboard](images/dashboard.png)

### 📄 CSV Submission Export
Example of the exported `.csv` containing captured data.
![CSV File](images/csv.png)

---

## Setup and Installation

### Prerequisites
- Python 3.x
- Flask
- SendGrid account and API key (for email alerts)

### Installation Steps

```bash
# Clone the repo
git clone https://github.com/yourusername/phishing-simulation.git
cd phishing-simulation

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (SendGrid key, etc.)
touch .env
# Add: SENDGRID_API_KEY=your_key_here

# Run the app
flask run


---



