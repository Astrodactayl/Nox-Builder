import requests
import re

def check_webhook(webhook):
    regex = re.compile(r"https?:\/\/(?:ptb\.|canary\.)?discord(?:app)?\.com\/api(?:\/)?(v\d{1,2})?\/webhooks\/\d{17,21}\/[\w\-]{68}")
    match = regex.match(webhook)
    if match:
        status = requests.get(webhook).status_code
        if status == 200:
            return True
    else:
        return False
