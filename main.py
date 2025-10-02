import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from helpers.generate_content import generate_content
from config import MAX_ITERATIONS

def main():
    load_dotenv()

    # If the verbose flag is present in the list of command line arguments, set verbose to True
    verbose = "--verbose" in sys.argv

    # Put all args that are not flags into a list called 'args'
    args = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))

    # If there is no prompt, run an error message
    if not args:
        error_message = "Error: No prompt entered"
        print(error_message, file=sys.stderr)
        print('Proper usage: uv run main.py "your prompt here"')
        sys.exit(1)

    # Utilize API key
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Combine all non-flag args into a string to create the user prompt
    user_prompt = " ".join(args)

    # If verbose flag is present, print user prompt
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Add the user's prompt to a list of Content objects called 'messages' (so it can eventually hold the whole conversation)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    try:
        response, messages = generate_content(client, messages, verbose)
    except Exception as e:
        return f"Error generating content: {e}"
    
    # If the response contains a text response that is explainable to a human
    #   then the model is done iterating (thinking), so return the final response
    if response.text:
        print("")
        print(f"FINAL RESPONSE: {response.text}")

    
if __name__ == "__main__":
    main()