# app/emails/link_cleaner.py

import re

def remove_all_links(html: str) -> str:
    """
    Removes ALL <a href="...">...</a> links from the AI-generated body.
    Leaves only the visible text.
    """
    # remove anchor tags but keep inner text
    cleaned = re.sub(
        r'<a\s+[^>]*>(.*?)</a>',
        r'\1',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    return cleaned
