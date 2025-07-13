import bleach
from bleach.css_sanitizer import CSSSanitizer
import re
import base64
import uuid
import os
from pathlib import Path
from typing import Optional
import base64
import uuid
import os
from pathlib import Path
from typing import Optional
import logging
from config import Config

def sanitizeContents(content: str) -> str:
    safe_tags = [
        'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br',
        'ul', 'li', 'ol', 'img', 'div', 'span',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'hr', 'pre', 'code'
    ]

    safe_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['style', 'class'],
        'span': ['style', 'class'],
        'p': ['style', 'class'],
        '*': ['style']
    }

    css_sanitizer = CSSSanitizer(allowed_css_properties=[
        'text-align', 'color', 'background-color', 'font-weight',
        'font-style', 'font-size', 'margin', 'padding',
        'border', 'width', 'height'
    ])

    sanitized = bleach.clean(
        content,
        tags=safe_tags,
        attributes=safe_attributes,
        protocols=['http', 'https'],
        css_sanitizer=css_sanitizer,
        strip=True,
        strip_comments=True
    )

    return bleach.linkify(sanitized)






# Setup logger
logger = logging.getLogger("image_saver")
logger.setLevel(logging.DEBUG)  # Change to INFO or WARNING in prod

# Ensure handler is only added once
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Configure logger for production
logger = logging.getLogger("image_saver")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

async def save_base64_image(base64_str: str, folder: str = "uploads", filename: str = None) -> Optional[str]:
    if not base64_str.startswith("data:image/"):
        logger.warning("Invalid base64 image string format.")
        return None

    try:
        # Split base64 header and content
        header, encoded = base64_str.split(",", 1)
        file_ext = header.split(";")[0].split("/")[1]

        # Generate filename
        if not filename:
            filename = f"{uuid.uuid4().hex}.{file_ext}"
        else:
            filename = f"{filename}.{file_ext}"

        # Construct paths
        relative_path = os.path.join(folder, filename)
        full_path = os.path.join(Config.BASE_DIR, relative_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Decode and write file
        with open(full_path, "wb") as f:
            f.write(base64.b64decode(encoded))

        logger.info(f"✅ Image saved: {full_path}")
        return relative_path.replace("\\", "/")  # return URL-friendly path

    except Exception as e:
        logger.error(f"❌ Failed to save image: {e}")
        return None


async def sanitize_name (name):
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.strip().replace(" ", "_").lower())
