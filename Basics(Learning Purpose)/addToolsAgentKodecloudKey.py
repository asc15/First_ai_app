from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
load_dotenv()  # Load environment variables from .env file

def get_weather(city: str):
   """get weather for a givem city"""
   return {"condition": "sunny", "temperature": 30, "humidity": 50}

def get_location(city: str):
   """get user's current location. when user asks for weather without specifying a city,
     this tool will be used to get the user's current location"""
   return "rome","italy"

#initialize the Google Generative AI chat model
llm = ChatOpenAI(
    model="google/gemini-4-carbon",
    api_key=os.getenv("KODEKEY_API_KEY"),
    base_url="https://api.ai.kodekloud.com/v1",
    temperature=0.7
)

system_prompt = """You are a helpful assistant that can provide weather information for a given city.
YOUR WORKFLOW:
1. if the user ask about the weaher without specifying a location, you must follow:
- first call the get_location tool to get the user's current location
- then call the get_weather(city) tool to get the weather for that location
2. if user provide a city, you must call the get_weather(city) directly to get the weather for that city.
"""

#response = llm.invoke("how is the weather today in ranchi?")
#print(response.content)
agent = create_agent(model=llm, 
                     tools=[get_weather,get_location],
                     system_prompt=system_prompt)

user_query = input("Ask your question: ")

response = agent.invoke({"messages":
                        [{"role": "user",
                        "content": user_query}]})


print(response['messages'][-1].content)