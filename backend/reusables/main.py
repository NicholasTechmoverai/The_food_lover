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

