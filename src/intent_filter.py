DOMAIN_KEYWORDS = [
    "domain name",
    "buy domain",
    "sell domain",
    "domain for",
    ".com",
    ".io",
    ".ai",
    ".net",
    "brand name",
    "startup name",
    "choose domain",
    "domain suggestions",
]


def is_domain_related(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in DOMAIN_KEYWORDS)
