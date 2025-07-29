from utils.email_sender import (
    send_email,
    form_email_message,
    render_cards,
    code_template,
    verify_link_template,
    update_account_template
)
from utils.recipes import RecipeService
from models import User
from config import Config, WEB_SERVER,BASE_SERVER
from utils.logger import setup_logger
logger = setup_logger("MANUAL EMAIL SENDER:")

async def send_email_noty(proverb: str, username: str, useremail: str,avatar:str,cards:list):
    try:
        cards_html = render_cards(cards)
        email_body = await form_email_message(
            update_account_template.format(
                proverb=proverb,
                username=username,
                url=f"{WEB_SERVER}/{username}",
                avatar=avatar,
                site = Config.SITE_NAME,
                trending_recipes_url=f"{WEB_SERVER}/recipes",
                cards_html=cards_html
            )
        )

        sent = await send_email(useremail, email_body,subject="Upgrade your profile")
        return sent

    except Exception as err:
        print(f"Email send error: {err}")
        return None



async def trigger():
    """
    Sends trending recipe email notifications to all registered users.

    This function:
      - Retrieves a list of trending recipe suggestions
      - Iterates through all users
      - Sends a personalized email to each user with:
        - A motivational proverb
        - User's name and avatar
        - A curated list of recipe cards

    All email sending is handled individually with error protection to avoid
    halting the loop on one failure.

    Returns:
        bool: True if the function executes to completion.
    """
    proverb = "In every great dish, there's a story only the chef can tell. - wantam"

    try:
        cards = await RecipeService().get_recipes_suggestions(
            name='trending',
            return_unsimilar=True,
            return_no=5
        )
    except Exception as e:
        logger.error(f"Failed to fetch recipe suggestions: {e}")
        return False

    try:
        users = await User.all()
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        return False

    for user in users:
        try:
            if user.email == "techmoversai@gmail.com":

                await send_email_noty(
                    proverb=proverb,
                    username=user.username or user.name,
                    useremail=user.email,
                    avatar=user.picture_url
                    if user.picture_url.startswith("https://")
                    else f"{BASE_SERVER}/{user.picture_url}",
                    cards=cards
                )
        except Exception as e:
            logger.warning(f"Failed to send email to {user.email}: {e}")

    return True