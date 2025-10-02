import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from helpers.call_function import call_function, available_functions
from helpers.prompts import system_prompt

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

    # Combine all non-flag args to create the user prompt
    user_prompt = " ".join(args)

    # If verbose flag is present, print user prompt
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Add the user's prompt to a list called 'messages' (so it can eventually hold the whole conversation)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):

    # Generate the response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions])
    )

    # Iterate over each candidate and add its content to the messages list
    for candidate in response.candidates:
        messages.append(candidate.content)

    # If the verbose flag is present, print token amounts used
    if verbose == True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # If the prompt doesn't require a function call, just return a text response
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)

        if not result.parts[0].function_response or not result.parts:
            raise Exception("No functions were called")
    
        if verbose:
            print(f"-> {result.parts[0].function_response.response['result']}")

        function_responses.append(result.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting")

if __name__ == "__main__":
    main()