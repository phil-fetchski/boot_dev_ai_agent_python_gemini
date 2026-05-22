import os
import argparse
from collections.abc import Callable
from google.genai import types

from get_verbose import get_verbose
from gemini_generate import gemini 
from functions.call_function import call_function


# Arg Parser
parser = argparse.ArgumentParser(description="Gemini Agent 007")
parser.add_argument("user_prompt", type=str, help="The user prompt is where you provide your question for the Agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# USER PROMPT
user_prompt = args.user_prompt

is_verbose = False

if args.verbose:
    is_verbose = True

# MESSAGES
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

# MAIN
def main():

    iterations = 0

    try:
        for _ in range(20):
            iterations += 1
            response: types.GenerateContentResponse = gemini(messages)
            candidates = response.candidates

            if candidates:
                for c in candidates:
                    if c.content: 
                        can_con = c.content
                        messages.append(can_con)
            else:
                return
            
            # Get Function Calls - TOOL CALLS if any
            if response.function_calls:

                fc_results: list = []

                for fc in response.function_calls:

                    fc_result = call_function(fc)

                    if not fc_result.parts:
                        raise Exception(f"The function call result had no or empty .parts - PARTS: {fc_result.parts}")

                    if not fc_result.parts[0].function_response:
                        raise Exception(f"The function calls result parts[0].function_response is None or empty")

                    if is_verbose:
                        print(f"-> {fc_result.parts[0].function_response.response}")

                    for part in fc_result.parts:
                        fc_results.append(part)

                messages.append(types.Content(role="user", parts=fc_results))
                    
            # Text Response from LLM            
            if response.text:
                print("Response: \n")
                print(response.text)

            if is_verbose:
                print(get_verbose(user_prompt, response))

            if not response.function_calls or response.function_calls is None:
                break

            if iterations == 20:
                print("The Agent has exceeded the maximum number of allowed iterations.")
                exit(1)

    except RuntimeError as e:
        print(e)
    
if __name__ == "__main__":
    main()
