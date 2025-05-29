Email Summarizer Agent

This project creates an AI agent that regularly scans your inbox for new emails, summarizes their content, and sends the summaries to your email. It uses a local model for summarization to ensure privacy, and it is deployed in a Docker container for easy portability.

Features
Fetches unread emails from your inbox.

Summarizes the email content.

Sends the summarized content back to your email.

Exposes a Flask API (/fetch_emails) to trigger the process manually.

Requirements
Before setting up the project, ensure you have the following installed:

Python 3.6 or later

Docker (optional for containerized deployment)

Access to your email (Yahoo Mail supported for this example)

Python Libraries
Flask

python-dotenv

smtplib (standard Python library for sending emails)

Setup Instructions
1. Clone the repository
Clone the repository to your local machine:

bash
Copy
Edit
git clone https://github.com/your-username/email-summarizer-agent.git
cd email-summarizer-agent
2. Install Dependencies
Install the necessary Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory of your project. This file will store your email credentials. It should look like this:

.env:

text
Copy
Edit
EMAIL_USER=your_email@yahoo.com
EMAIL_PASSWORD=your_email_password
Replace your_email@yahoo.com and your_email_password with your actual email address and password. If you're using two-factor authentication, you'll need to use an app-specific password.

4. Set Up Email Fetching
In email_reader.py, the function fetch_emails() is responsible for fetching emails from your inbox. The example provided works for Yahoo Mail using IMAP. Make sure your email provider allows access to apps via IMAP.

5. Run the Flask Application
You can run the application locally by using the following command:

bash
Copy
Edit
python main.py
This will start the Flask application, and you can access the API at http://localhost:8000.

Docker Deployment (Optional)
If you prefer to deploy the application in a Docker container, follow these steps.

1. Build the Docker Image
To build the Docker image, run the following command in the root of your project:

bash
Copy
Edit
docker build -t email-summarizer-agent .
2. Run the Docker Container
To start the container and map the port, use this command:

bash
Copy
Edit
docker run -d -p 8000:8000 --name email-summarizer-agent email-summarizer-agent
3. Verify the Deployment
Once the container is running, you can access the API at http://localhost:8000. You can also check the logs using:

bash
Copy
Edit
docker logs -f email-summarizer-agent
How It Works
Fetch Emails: When you visit the /fetch_emails endpoint, the system will fetch unread emails from your inbox using the fetch_emails() function in email_reader.py. This function supports IMAP for email providers like Yahoo, Gmail, etc.

Summarize Emails: After fetching an email, the content is passed to the summarize_text() function in summarizer.py to generate a summary.

Send Summary: Once the email is summarized, the summary is sent back to your email using the send_summary_via_email() function in email_utils.py.

API Endpoint
/fetch_emails
Method: GET

Description: This endpoint fetches unread emails from your inbox, summarizes them, and sends the summaries to your email.

Response: A JSON array containing the subject and summary of each email.

Example response:

json
Copy
Edit
[
  {
    "subject": "Email Subject 1",
    "summary": "This is the summary of the first email."
  },
  {
    "subject": "Email Subject 2",
    "summary": "This is the summary of the second email."
  }
]
Troubleshooting
IMAP Access Issues: If you're unable to fetch emails, make sure IMAP is enabled for your email account (for Yahoo, visit: Yahoo IMAP setup).

Email Sending Issues: If you encounter errors sending emails, double-check your email credentials in the .env file. If you're using two-factor authentication, generate an app-specific password for your email provider.

Docker Issues: If the Docker container fails to start, check the logs for any errors using:

bash
Copy
Edit
docker logs -f email-summarizer-agent
Future Improvements
Support for additional email providers.

Advanced summarization techniques using larger models or fine-tuned models.

Implementing scheduled email fetching using cron jobs or a task scheduler.

License
This project is licensed under the MIT License - see the LICENSE file for details.

