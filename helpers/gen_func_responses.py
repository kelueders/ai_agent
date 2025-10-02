from helpers.call_function import call_function

def gen_func_responses(function_calls, verbose):
    '''
    Goes through the list of function calls to generate function responses
    then stores these responses as a list of Part objects
    '''
    # Create an empty list to hold content Part objects
    function_responses = []

    for function_call_part in function_calls:
        # call_function returns a Content object
        content = call_function(function_call_part, verbose)

        # Extract the function response from the 1st content part
        part = content.parts[0]
        function_response = part.function_response

        # Return exception if the function response of the part is empty or there are no parts in the content
        if not function_response or not content.parts:
            raise Exception("No functions were called")
    
        # If the verbose option is selected, return a printout of the result of the function call
        if verbose:
            print(f"-> {function_response.response['result']}")

        # Add the content Part to the list of function responses
        function_responses.append(part)
    
    if not function_responses:
        raise Exception("No function responses generated, exiting")
    
    return function_responses