from langchain.chat_models import init_chat_model
GOOGLE_API_KEY = "your_google_api_key_here"  # Replace with your actual Google API key
model = init_chat_model(model="gemini-3-flash-preview", 
                             model_provider="google-genai",
                             api_key=GOOGLE_API_KEY)
with open("woods.txt", "r") as file:
    text = file.read()

response = model.invoke(f"which are the best trees in {text}?")
print(response.content[0]["text"])