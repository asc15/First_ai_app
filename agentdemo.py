from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
load_dotenv()  # Load environment variables from .env file

#initialize the Google Generative AI chat model
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7)

#response = llm.invoke("how is the weather today in ranchi?")
#print(response.content)
agent = create_agent(llm)

response = agent.invoke({"messages":
                        [{"role": "user",
                        "content": "how is the weather today in ranchi?"}]})


print(response)