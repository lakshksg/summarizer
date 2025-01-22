import re

def parse_agent_response(details:str):
    
    industry, company_size, location = None, None, None
    
    for data in details.split("\n"):
        if data.startswith("INDUSTRY"):
            industry = data.split(":")[1].strip()
        elif data.startswith("SIZE"):
            company_size = data.split(":")[1].strip()
        elif data.startswith("LOCATION"):
            location = data.split(":")[1].strip()

    return industry, company_size, location

def verify_url(url :str):
    
    URL_REGEX = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE
    )
    return URL_REGEX.match(url)