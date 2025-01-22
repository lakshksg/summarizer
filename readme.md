# README


This project provides an API that allows users to summarize information from a provided URL. The summarization includes details such as industry, company size, and location. The service is built using FastAPI, PyJWT, Pydantic, BeautifulSoup4, and Requests.
Live Demo

You can access the live version of the API 
    
    https://summarizer-wandering-mountain-9255.fly.dev/

Login Credentials

    Username: laksh
    Password: P@@sw0rd123
    
## Installation


To use this project, you'll need to have the following dependencies installed:

- FastAPI  
- PyJWT  
- Pydantic  
- BeautifulSoup4  
- Requests  

You can install these dependencies using `pip`:

```bash
python -m venv venv

# For Linux
source venv/bin/activate

# For Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

uvicorn main:app --reload

Step 1: Create Access Token

Use the /login API to generate an access token (valid for 20 min).

API: Login

    Endpoint: /login
    Method: POST
 

    curl --location '127.0.0.1:8000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"laksh",
    "pass": "P@@sw0rd123"
}'

Response:

{
  "access_token": "your_access_token",
  "token_type": "Bearer"
}

###############################

Step 2: Use the Access Token for Authorization

Pass the access token generated from the login API in the Authorization headers.

API: Summarize

    Endpoint: /summarize
    Method: POST


    curl --location '127.0.0.1:8000/summarize' \
    --header 'Authorization: Bearer 'your token' \
    --header 'Content-Type: application/json' \
    --data '{"url":"https://wellfound.com/"}'

    Response:

{
  "industry": "Industry description",
  "company_size": "Company size",
  "location": "Company location"
}


Example:
    
    curl --location '127.0.0.1:8000/summarize' \
    --header 'Authorization: Bearer your token' \
    --header 'Content-Type: application/json' \
    --data '{"url":"https://gomechanic.in/"}'


    curl --location '127.0.0.1:8000/summarize' \
    --header 'Authorization: Bearer your token' \
    --header 'Content-Type: application/json' \
    --data '{"url":"https://careercampuspro.com/"}'


    curl --location '127.0.0.1:8000/summarize' \
    --header 'Authorization: Bearer your token' \
    --header 'Content-Type: application/json' \
    --data '{"url":"https://wellfound.com/"}'