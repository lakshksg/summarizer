from fastapi import FastAPI,Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import requests
import json

from modals import AgentResponse, TokenResponse
from utils import parse_agent_response, scrape_webpage
from constant import GEMINI_KEY, test_user
from utils import verify_url
from auth import create_access_token, verify_token

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = GeminiModel('gemini-1.5-flash', api_key=GEMINI_KEY)


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
            - If info is there then no mentioned should not be present in answer.
            """

        
    ),
)


@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})

@app.get("/detail", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse("summerizer.html", {"request": req})

@app.post("/login", response_model=TokenResponse)
async def login(req: Request, response: Response):

    data = await req.json()
    user = data.get("name")
    password = data.get("pass")
    
    if not user or (test_user["pass"] != password and test_user["name"] != user):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid username or password"}
        )
    access_token = create_access_token(data={"user_name": user})

    return TokenResponse(access_token=access_token, token_type="Bearer")


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
