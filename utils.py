import re
import requests
import json
from bs4 import BeautifulSoup


def scrape_webpage(url:str):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        if text.strip():
            return json.dumps({"text": text})

    except requests.exceptions.RequestException as e:
        return json.dumps({"text": ""})


def parse_agent_response(details:str):
    
    industry, company_size, location = None, None, None
    
    for data in details.split("\n"):
        if data.startswith("INDUSTRY"):
            industry = data.split(":")[1].strip()
        elif data.startswith("SIZE"):
            company_size = data.split(":")[1].strip()
        elif data.startswith("LOCATION"):
            location = data.split(":")[1].strip()
    
    return (industry if industry else "", 
            company_size if company_size else "", 
            location if location else "")

def verify_url(url :str):
    
    URL_REGEX =  re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(URL_REGEX, url)