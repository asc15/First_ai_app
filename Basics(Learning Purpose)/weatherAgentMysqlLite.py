from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import requests

load_dotenv()  # Load environment variables from .env file

def get_weather(city: str):
   """get weather for a givem city. 
   return temperature_farenheit value in farenheit lable for locaations such as USA, bahamas, Belize, Cayman Islands, Palau, Puerto Rico, US Virgin Islands, Guam, Northern Mariana Islands, American Samoa, and the Federated States of Micronesia.
   """
   api_key = os.getenv("OPEN_WEATHER_API_KEY")
   base_url = "https://api.openweathermap.org/data/2.5/weather"
   params = {
         "q": city,
            "appid": api_key,
            "units": "metric"
   }
   response = requests.get(base_url, params=params)
   data= response.json()
   temperature = data["main"]["temp"]
   temperature_farenheit = (temperature * 9/5) + 32
   return data, {'temperature_celsius': temperature, 'temperature_farenheit': temperature_farenheit}

def get_location(city: str):
   """get user's current location. when user asks for weather without specifying a city,
     this tool will be used to get the user's current location"""
   response = requests.get("https://ipapi.co/json/", headers={"User-Agent": "your_user_agent"})
   data = response.json()
   return data["city"]

#initialize the Google Generative AI chat model
llm = ChatOpenAI(
    model="google/gemini-3.8-flash",
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
3.  use your knowlege  to determine which temprature unit is standard for the given location.
"""


with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
   agent = create_agent(model=llm, 
                        tools=[get_weather,get_location],
                        system_prompt=system_prompt,
                        checkpointer=checkpointer)

   if __name__ == "__main__":
      while True:
         user_query = input("Ask your question: ")
         if user_query.lower() in {"exit", "quit"}:
               print("Goodbye!")
               break
         response = agent.invoke({"messages":
                                 [{"role": "user",
                                 "content": user_query}]},{"configurable":{"thread_id":"1"}})
         #get the last message from the response and print it
         #print(response['messages'])
         for i in response['messages']:
            #print(i.content)
            if i.type == "human":
               print(f"User: {i.content}")
            if i.type == "ai" and i.content:
               print(f"AI: {i.content}")

         print(response['messages'][-1].content)

    