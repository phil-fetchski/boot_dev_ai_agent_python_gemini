import os
import argparse
from dotenv import load_dotenv
from google import genai
from collections.abc import Callable
from google.genai import types
from prompts import system_prompt
# Get Tokens from Response (res)
from get_tokens import get_toks
# INDEX of Tool Schemas/Function Declarations, and FUNCTION_MAP
from functions.tool_schemas import *
from functions.call_function import call_function

# setup google genai Client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Gemini API Key Not Found")

client = genai.Client(api_key=api_key)

# Arg Parser
parser = argparse.ArgumentParser(description="Flash Bot Agent 007")
parser.add_argument("user_prompt", type=str, help="The user prompt is where you provide your question for the Agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# MESSAGES
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# Generate Content with Gemini
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
)

# Get Response and Response Text or Raise
if not response:
    raise RuntimeError("there was no response")
else:
    res = response

# Verbose Output Func
def get_verbose():
    try:
        print("\n")
        print(f"User prompt: {args.user_prompt}")
        print("\n")

        prompt_tok_msg = get_toks(res, "prompt") + "\n"
        print(prompt_tok_msg)

        response_tok_msg = get_toks(res, "response") + "\n"
        print(response_tok_msg)

    except (RuntimeError, ValueError) as e:
        print(f"Error retrieving tokens: {e}")

# MAIN
def main():
    
    is_verbose = False 

    if args.verbose:
        get_verbose()
        is_verbose = True
    
    try:
        # Get Function Calls - TOOL CALLS if any
        if res.function_calls:
            if res.function_calls != None:
                for fc in res.function_calls:
                    fc_result = call_function(fc)

                    if not fc_result.parts:
                        raise Exception(f"The function call result had no or empty .parts - PARTS: {fc_result.parts}")

                    if not fc_result.parts[0].function_response:
                        raise Exception(f"The function calls result parts[0].function_response is None or empty")

                    if is_verbose:
                        print(f"-> {fc_result.parts[0].function_response.response}")
                    

                    

        # Text Response from LLM            
        if res.text:
            print("Response: \n")
            print(res.text)

    except RuntimeError as e:
        print(e)
    

if __name__ == "__main__":
    main()
