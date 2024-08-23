# Phishing Simulation Project

[Watch the video walkthrough on YouTube](https://www.youtube.com/watch?v=lQbfF3DHbQY)


## Overview
This project is a phishing simulation tool designed to help organizations educate their employees on how to recognize phishing emails and avoid falling victim to scams. The simulation mimics a real-world phishing attack and provides feedback to users who fall for the phishing attempt.

## Features
- **Realistic Login Page**: A replica of the UMass Memorial myChart login page, used to simulate the phishing scenario.
- **Feedback Mechanism**: Users who enter their credentials are redirected to a feedback page, alerting them to the phishing attempt.
- **Email Alerts**: Admins receive notifications of each phishing attempt via email.
- **Role-based Access Control**: Secure dashboard access for administrators to view the results of the simulation.
- **Data Export**: Export submission data as a CSV file for further analysis.
- **Training Integration**: A link to a phishing awareness training video is provided on the feedback page.

## Technologies Used
- **Flask**: Python web framework used to create the web application.
- **SQLAlchemy**: ORM for database management.
- **Bootstrap**: CSS framework for responsive and modern UI design.
- **SendGrid**: Third-party email service for sending alerts.
- **SQLite**: Database used to store submission data.
- **Jinja2**: Templating engine for rendering HTML pages.

## Setup and Installation

### Prerequisites
- Python 3.x
- Virtual Environment (optional but recommended)
- Flask
- SendGrid API Key

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/phishing-simulation.git
    cd phishing-simulation
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Set your `SENDGRID_API_KEY` and any other necessary environment variables in a `.env` file or directly in your environment.

5. Run the application:
    ```bash
    flask run
    ```

6. Access the application:
    - Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.

## Configuration
- **Database**: The application uses an SQLite database by default. You can configure a different database by modifying the `SQLALCHEMY_DATABASE_URI` in `app.py`.
- **Email Alerts**: Configure your SendGrid API key in the environment variables to enable email alerts.

## Usage

### Simulating a Phishing Attack
1. Deploy the application to a secure server.
2. Send phishing emails to your users with a link to the login page ([http://yourdomain.com/login](http://yourdomain.com/login)).
3. Monitor the dashboard to track who falls for the phishing attempt.
4. Provide feedback and training to users who fall victim to the simulation.

### Accessing the Dashboard
- Log in to the admin dashboard at [http://yourdomain.com/dashboard](http://yourdomain.com/dashboard) using the credentials set during the setup process.

## Contributing
1. Fork the repository.
2. Create your feature branch:
    ```bash
    git checkout -b feature/your-feature
    ```
3. Commit your changes:
    ```bash
    git commit -am 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature
    ```
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is intended for educational and training purposes only. Use it responsibly and within the bounds of your organization's policies and legal guidelines.
