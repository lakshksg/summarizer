from fastapi import FastAPI,Request, status
from fastapi.responses import JSONResponse
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from bs4 import BeautifulSoup
import requests
import json
import re

from modals import AgentResponse
from utils import parse_agent_response
from constant import OPEN_AI_KEY, SECRET_KEY

app = FastAPI()
model = OpenAIModel('gpt-3.5-turbo-0125', api_key=OPEN_AI_KEY)


summarizer_agent = Agent(  
    model,
    system_prompt=(
        """
            Instructions:
            You will receive content scraped from a webpage, primarily the homepage, using BeautifulSoup.
            Based on the content provided, answer the following questions in the format below:

            ---

            INDUSTRY: (Answer in 50 words, state "Not mentioned" if not found)

            SIZE: (Answer in 5 words, state "Not mentioned" if not found)

            LOCATION: (Answer in 50 words, state "Not mentioned" if not found)

            ---

            Questions to Answer:

            1. INDUSTRY: What industry does the company belong to? If mentioned, provide a brief description. If not found, clearly state "Not mentioned."

            2. SIZE: What is the company's size (e.g., small, medium, large)? If mentioned, specify. If not found, state "Not mentioned."

            3. LOCATION: Where is the company located (city, country)? If mentioned, provide details. If not found, clearly state "Not mentioned."

            ---

            Guidelines:

            - If any of the details (industry, size, or location) are not mentioned in the content, ensure you explicitly state that the information is "Not mentioned."
            - If multiple pieces of information exist, summarize them clearly without going over the word limit.
            """

        
    ),
)

def scrape_webpage(url:str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        if text.strip():
            return json.dumps({"text": text})

    except requests.exceptions.RequestException as e:
        return json.dumps({"text": ""})

def verify_token(authorization: str ):
    if not authorization or not authorization.startswith("Bearer "):
        return False
    
    token = authorization.split(" ")[1]

    if token != SECRET_KEY:
        return False
    
    return True

def verify_url(url :str):
    
    URL_REGEX = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE
    )
    return URL_REGEX.match(url)

@app.post("/summarize")
async def summarize(req: Request):
    
    data = await req.json()
    url = data.get("url") 
    
    if not url or not verify_url(url):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Invalid url"}
        )  
    
    authorization = req.headers.get("Authorization")
    
    if not verify_token(authorization):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Invalid or expired token"}
        )
    
    scraped_data = json.loads(scrape_webpage(url))  
    
    text = scraped_data.get("text")
    
    result = await summarizer_agent.run(user_prompt=text)
    company_detail = result.data
    
    industry, company_size, location = parse_agent_response(company_detail)

    return AgentResponse(industry=industry, company_size=company_size, location=location)
