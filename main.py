import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from argparse import ArgumentParser
from prompts import system_prompt
from call_functions import available_functions

parser = ArgumentParser()
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
contents = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response = client.models.generate_content(
    model=model, 
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0,
        tools=[available_functions],
    ),
    )

if args.verbose:
    print("User prompt:", contents)

    if response.usage_metadata:
        prompt_token = response.usage_metadata.prompt_token_count
        response_token = response.usage_metadata.candidates_token_count

        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")
    else:
        raise RuntimeError("Usage metadata not found")

function_calls = response.function_calls

if function_calls is not None:
    for call in function_calls:
        print(f"Calling function: {call.name}({call.args})")
else:
    print("Response:")
    print(response.text)