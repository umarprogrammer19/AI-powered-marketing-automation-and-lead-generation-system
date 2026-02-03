DOMAIN_KEYWORDS = [
    "domain",
    "name for sale",
    "taking offers",
    "brand name",
    "startup name",
    ".com",
    ".io",
    ".ai",
    ".net",
    "godaddy",
    "namecheap",
    "sedo",
    "dan.com",
    "squadhelp",
    "naming",
    "branding",
    "url",
    "website for sale",
]


def is_domain_related(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    return any(keyword in text for keyword in DOMAIN_KEYWORDS)
