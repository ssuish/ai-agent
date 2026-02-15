import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(model=model, contents=contents)

print("User prompt:", contents)

if response.usage_metadata:
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {response_token}")
else:
    raise RuntimeError("Usage metadata not found")

print("Response:")
print(response.text)