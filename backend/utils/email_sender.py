import random
import os
import smtplib
import datetime as datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from config import Config, WEB_SERVER


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
# update_account_template = """
# <div style="max-width: 600px; margin: 0 auto; padding: 32px; background-color: #ffffff; border-radius: 12px; font-family: 'Arial', sans-serif; color: #333333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); ">
#   <!-- Header -->
#   <div style="text-align: center; margin-bottom: 24px;">
#     <h2 style="color: #2c3e50; margin: 0; font-size: 26px; font-weight: 600; letter-spacing: -0.5px;">
#       Time to Refresh Your Profile!
#     </h2>
#   </div>

#   <!-- Inspirational Quote -->
#   <div style="background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 24px; text-align: center; font-style: italic; color: #555555; font-size: 15px; line-height: 1.6;">
#     {proverb}
#   </div>

#   <!-- Greeting -->
#   <div style="font-size: 22px; font-weight: bold; color: #2c3e50; text-align: center; margin: 24px 0; padding: 16px; background-color: #f5f9ff; border-radius: 8px; border-left: 4px solid #1e90ff; display:flex ; align-items:center; flex-direction:row">
#     Hello, <span style="color: #A52A2A;"> <a href="{url}" style="text-decoration: none;">{username} </a></span>!  <a href="{url}" style="margin-left:auto;"><img src="{avatar}" alt="{username}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 50%;background: #A52A2A; border: 1px solid rgba(255, 255, 255, 0.2);box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);" />   </a>
#   </div>

#   <!-- Update Message -->
#   <div style="font-size: 15px; line-height: 1.6; text-align: center; margin-bottom: 24px; padding: 0 16px;">
#     <p style="margin-bottom: 16px;">
#       <strong style="color: #1e90ff;">{site}</strong> has been upgraded with exciting new features!<br />
#       Keep your profile fresh to make the most of them.
#     </p>
#     <a href="{url}" style="display: inline-block; background-color: #1e90ff; color: white; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; margin-top: 8px; transition: background-color 0.3s;">
#       Update Profile Now
#     </a>
#   </div>

#   <!-- Divider -->
#   <hr style="border: none; height: 1px; background-color: #eaeaea; margin: 24px 0;" />

#   <!-- Trending Recipes -->
#   <div style="text-align: center;">
#     <p style="font-size: 14px; color: #666666; margin-bottom: 12px;">
#       While you're here, check out what's trending:
#     </p>
#     <div>
#     </div>
#     <a href="{trending_recipes_url}" style="color: #1e90ff; text-decoration: none; font-weight: bold; font-size: 15px;">
#       Explore Trending Recipes →
#     </a>
#   </div>
# </div>
# """


update_account_template = """
<div style="max-width: 600px; margin: 0 auto; padding: 12px; background-color: #ffffff; border-radius: 12px; font-family: 'Arial', sans-serif; color: #333333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
  
  <!-- Header -->
  <div style="text-align: center; margin-bottom: 24px;">
    <h2 style="color: #2c3e50; margin: 0; font-size: 26px; font-weight: 600; letter-spacing: -0.5px;">
      Time to Refresh Your Profile!
    </h2>
  </div>

  <!-- Inspirational Quote -->
  <div style="background-color: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 24px; text-align: center; font-style: italic; color: #555555; font-size: 15px; line-height: 1.6;">
    {proverb}
  </div>

  <!-- Greeting -->
  <div style="font-size: 22px; font-weight: bold; color: #2c3e50; text-align: center; margin: 24px 0; padding: 16px; background-color: #f5f9ff; border-radius: 8px; border-left: 4px solid #1e90ff; display: flex; align-items: center;">
    Hello, <span style="color: #A52A2A;"> <a href="{url}" style="text-decoration: none;">{username}</a></span>!
    <a href="{url}" style="margin-left: auto;">
      <img src="{avatar}" alt="{username}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 50%; background: #A52A2A; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);" />
    </a>
  </div>

  <!-- Update Message -->
  <div style="font-size: 15px; line-height: 1.6; text-align: center; margin-bottom: 24px; padding: 0 16px;">
    <p style="margin-bottom: 16px;">
      <strong style="color: #1e90ff;">{site}</strong> has been upgraded with exciting new features!<br />
      Keep your profile fresh to make the most of them.
    </p>
    <a href="{url}" style="display: inline-block; background-color: #1e90ff; color: white; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; margin-top: 8px;">
      Update Profile Now
    </a>
  </div>

  <!-- Divider -->
  <hr style="border: none; height: 1px; background-color: #eaeaea; margin: 24px 0;" />

  <!-- Trending Recipes Section -->
  <div style="text-align: center;">
    <p style="font-size: 14px; color: #666666; margin-bottom: 12px;">
      While you're here, check out what's trending:
    </p>
  <div style='
  display: flex;
  flex-direction: row;
  overflow-x: auto;
  gap: 12px;
  padding: 16px 0;
  -webkit-overflow-scrolling: touch;

'>
  {cards_html}
</div>
    <a href="{trending_recipes_url}" style="color: #1e90ff; text-decoration: none; font-weight: bold; font-size: 15px;">
      Explore Trending Recipes →
    </a>
  </div>
</div>
"""


def render_cards(cards: list[dict]) -> str:
    cards_html = ""

    for index, card in enumerate(cards):
        cards_html += f"""
<div style="display: inline-block; width: 280px; margin: 0 8px; font-family: 'Arial', sans-serif;">
  <div style="
    width: 280px;
    height: 340px;
    position: relative;
    display: block;
    overflow: hidden;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    background: {card.get("theme", "linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%)")};
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    padding: 20px;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,0.15);
    text-align: center;
  " aria-label="{card['title']} - {card['description']}">
    
    <!-- Image container -->
    <div style="
      width: 130px;
      height: 130px;
      border-radius: 50%;
      margin: 0 auto 24px auto;
      background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%);
      backdrop-filter: blur(4px);
      z-index: 2;
      border: 3px solid rgba(255,255,255,0.25);
      box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    ">
     <a href="{card["url"]}" style="text-decoration: none;">
      <img src="{card["image"]}" alt="{card["title"]}" style="
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid white;
        display: block;
        margin: 8px auto;
      "/>
      </a>
    </div>
    
    <!-- Content -->
    <div style="
      z-index: 2;
      text-align: center;
      width: 100%;
    ">
     <a href="{card["url"]}" style="text-decoration: none;">
      <h3 style="
        font-size: 22px;
        font-weight: 700;
        color: white;
        margin: 0 0 10px 0;
        text-shadow: 0 2px 6px rgba(0,0,0,0.3);
      ">{card["title"]}</h3>
      </a>
      <p style="
        font-size: 15px;
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 20px 0;
        line-height: 1.5;
      ">{card["description"]}</p>
      
      <a href="{card["url"]}" style="text-decoration: none;">
        <div style="
          display: inline-block;
          padding: 10px 24px;
          background: rgba(255,255,255,0.25);
          border-radius: 50px;
          color: white;
          font-size: 13px;
          font-weight: 600;
          letter-spacing: 0.8px;
          text-transform: uppercase;
          border: 1px solid rgba(255,255,255,0.3);
        ">
          View Recipe
        </div>
      </a>
    </div>
    
    <!-- Decorative elements -->
    <div style="
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at 20% 80%, rgba(255,255,255,0.15) 0%, transparent 70%);
      z-index: 1;
    "></div>
  </div>
</div>
"""

    # Wrap all cards in horizontally scrollable row
    return cards_html


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

        <div style="padding: 20px 5px;">
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


async def send_email(
    recipient_email: str, html_content: str, subject: str = "Verification Code"
) -> bool:
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
        msg["Subject"] = subject

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
