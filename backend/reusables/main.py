import bleach
from bleach.css_sanitizer import CSSSanitizer

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


import base64
import uuid
import os
from pathlib import Path
from typing import Optional


async def save_base64_image(base64_str: str, folder: str = "uploads",filename:str = None) -> Optional[str]:
    """
    Saves a base64-encoded image string to a file and returns the filename.

    Args:
        base64_str (str): The full base64 string (e.g. "data:image/jpeg;base64,...").
        folder (str): Destination folder to save the image.

    Returns:
        str: The saved filename (e.g., "uploads/abc123.jpg"), or None if invalid.
    """

    if not base64_str.startswith("data:image/"):
        return None

    try:
        # Split the metadata from the actual base64 content
        header, encoded = base64_str.split(",", 1)
        file_ext = header.split(";")[0].split("/")[1]  # e.g. "jpeg"

        # Decode base64
        image_data = base64.b64decode(encoded)

        # Ensure folder exists
        Path(folder).mkdir(parents=True, exist_ok=True)

        # Generate a unique filename
        if not filename:
            filename = f"{uuid.uuid4().hex}.{file_ext}"
        else:
            filename = f"{filename}.{file_ext}"
            
        filepath = os.path.join(folder, filename)

        # Save the image
        with open(filepath, "wb") as f:
            f.write(image_data)

        return filepath
    except Exception as e:
        print(f"[Image Save Error]: {e}")
        return None


async def sanitize_name (name):
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_").lower())
