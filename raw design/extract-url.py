# It shows how to extract the name from the url
from urllib.parse import urlparse

url = "https://copilot.com/chat/conversation/fa06c177-83ba-462c-8b55-e18bcc1f8a59?fromcode=cmmlf487uwy&es=Click&redirfrom=userTypeCookie&redirfrom=cosmicRingCookie"

domain = urlparse(url).netloc.replace("www.", "")
website_name = domain.split(".")[0]

print(website_name)  # github
