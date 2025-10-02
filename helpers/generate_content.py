from google.genai import types

from helpers.call_function import call_function, available_functions
from helpers.gen_func_responses import gen_func_responses
from helpers.prompts import system_prompt
from config import MAX_ITERATIONS

def generate_content(client, messages, verbose):
    '''
    Generates content for a prompt
    Returns either:
        1) a text response
        2) a response and a list of messages
    '''
    # message = a list of Content objects

    iteration_count = 1

    while iteration_count <= MAX_ITERATIONS:
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
            return response, messages

        function_responses_parts = gen_func_responses(response.function_calls, verbose)

        # print(f"FUNCTION RESPONSES: {function_responses}")

        new_output = types.Content(
            role="user",
            parts=function_responses_parts
        )

        messages.append(new_output)

        iteration_count += 1
    
    if iteration_count > MAX_ITERATIONS:
        print(f"You maxed out on turns. The model is set to only run {MAX_ITERATIONS} times. Please try again with a more simple prompt.")
        raise Exception("Max iterations")