import random
import os
import smtplib
import datetime as datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from config import Config,WEB_SERVER





# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))



# Template for sending a verification code
code_template = """
<div style="max-width: 600px; margin: 0 auto; padding: 24px; background-color: #f5f5f5; border-radius: 10px; font-family: Arial, sans-serif; color: #333;">
  <h2 style="color: #2c3e50; margin-bottom: 16px;">Your Verification Code</h2>

  <p style="font-size: 15px; line-height: 1.6;">
    Use the code below to verify your account:
  </p>

  <div style="font-size: 26px; font-weight: bold; color: #A52A2A; text-align: center; margin: 24px 0;">
    {code}
  </div>

  <p style="font-size: 14px; color: #666; text-align: center;">
    This code will expire in 10 minutes.
  </p>
</div>
"""

# Template for sending a clickable verification link
verify_link_template = """
<div style="max-width: 600px; margin: 0 auto; padding: 24px; background-color: #f5f5f5; border-radius: 10px; font-family: Arial, sans-serif; color: #333;">
  <h2 style="color: #2c3e50; margin-bottom: 16px;">Confirm Your Email Address</h2>
  
  <p style="font-size: 15px; line-height: 1.6;">
    To complete your sign-up, please click the button below to verify your email:
  </p>

  <a href="{link}" style="
    display: inline-block;
    background-color: #A52A2A;
    color: white;
    font-weight: bold;
    padding: 12px 24px;
    border-radius: 6px;
    text-decoration: none;
    margin: 20px 0;
    text-align: center;
  ">
    Verify Email
  </a>

  <p style="font-size: 14px; line-height: 1.5; margin-top: 24px;">
    If the button above doesn’t work, copy and paste the link below into your browser:
  </p>
  <p style="background-color: #fff; padding: 10px; word-break: break-all; border: 1px solid #ccc; border-radius: 6px;">
    {link}
  </p>

  <div style="text-align: center; margin: 30px 0;">
    <span style="display: inline-block; background-color: #ddd; height: 1px; width: 100%; margin-bottom: 20px;"></span>
    <strong style="font-size: 14px; color: #888;">OR</strong>
    <span style="display: inline-block; background-color: #ddd; height: 1px; width: 100%; margin-top: 20px;"></span>
  </div>

  <p style="font-size: 15px; text-align: center;">Use this verification code:</p>
  <div style="font-size: 26px; font-weight: bold; color: #A52A2A; text-align: center; margin-top: 12px;">
    {code}
  </div>
</div>
"""


# Function to wrap body in a branded HTML skeleton
async def form_email_message(body: str) -> str:
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #ffffff; color: #333333; line-height: 1.6; padding: 20px;">
      <div style="max-width: 600px; margin: auto; border-radius: 10px; border: 1px solid #eee; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
        <div style="text-align: center; padding: 20px 0;">
          <img src="{Config.SITE_LOGO}" alt="{Config.SITE_NAME}" style="width: 60px; height: 60px; object-fit: contain; border-radius: 50%;background: #A52A2A; border: 2px solid rgba(255, 255, 255, 0.2);box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);" />
          <h2 style="margin: 10px 0; color: #222;">{Config.SITE_NAME}</h2>
        </div>

        <div style="padding: 20px;">
          {body}
        </div>
            <div style="
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            border-top: 1px solid #e1e5eb;
            font-size: 13px;
            color: #6c757d;
        ">
          <p style="margin: 5px 0;">© {datetime.datetime.now().year} {Config.SITE_NAME}. All rights reserved.</p>
          <p style="margin: 5px 0;">
            Need help? <a href="{WEB_SERVER}/contact" style="color: #007bff; text-decoration: none;">Contact us</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """


async def send_email(recipient_email: str, html_content: str) -> bool:
    """
    Sends a verification email with HTML content to the specified recipient.

    Args:
        recipient_email (str): The recipient's email address.
        html_content (str): The HTML message body to send.

    Returns:
        bool: True if the email was sent successfully.

    Raises:
        ValueError: If the email or message is invalid.
        smtplib.SMTPException: For SMTP-related errors.
        Exception: For any other unexpected issues.
    """
    if not recipient_email or "@" not in recipient_email:
        raise ValueError("Invalid recipient email address.")
    
    if not html_content:
        raise ValueError("Email message content cannot be empty.")

    try:
        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = "Verification Code"

        msg.attach(MIMEText(html_content, "html"))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, msg.as_string())

        return True

    except smtplib.SMTPException as smtp_err:
        print(f"[SMTP Error] {smtp_err}")
        raise
    except Exception as ex:
        print(f"[Unexpected Error] {ex}")
        raise
    
    
    
 
# print(send_email("techmoversai@gmail.com",form_email_message(code_template.format(code="123456"))))    
    
    
    
    # usagge
# html_message = form_email_message(code_template.format(code="123456"))

# # Or with a link
# html_message = form_email_message(verify_link_template.format(link="https://example.com/verify?token=abc123"))
