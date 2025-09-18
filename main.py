import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.schemas import schema_get_files_info

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
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info
        ]
    )

    # Generate the response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions])
    )

    # If the verbose flag is present, print token amounts used
    if verbose == True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    functions = response.function_calls

    if functions:
        for function in functions:
            print(f"Calling function: {function.name}({function.args})")
            
    # Print the model response
    print("RESPONSE:")
    print(response.text)

if __name__ == "__main__":
    main()