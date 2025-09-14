import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    try:
        user_prompt = sys.argv[1]
    except:
        error_message = "Error: No prompt entered"
        print(error_message, file=sys.stderr)
        print('Proper usage: uv run main.py "your prompt here"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(user_prompt, client, messages)

def generate_content(user_prompt, client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
    )

    print(response.text)
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()