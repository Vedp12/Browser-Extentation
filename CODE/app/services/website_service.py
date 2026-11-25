from urllib.parse import urlparse


def normalize_url(raw):

    raw = raw.strip()

    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw

    parsed = urlparse(raw)

    if not parsed.hostname:
        raise ValueError("Invalid website URL")

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    return raw


def site_label(url):

    hostname = urlparse(url).hostname or ""

    return hostname.removeprefix("www.").split(".")[0].capitalize()


def extract_logo(url):

    hostname = urlparse(url).hostname

    return f"https://www.google.com/s2/favicons" f"?domain={hostname}&sz=128"
