import os
import argparse

from dotenv import load_dotenv
from google import genai

from google.genai import types

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
    contents=messages
)

# Get Response and Response Text or Raise
if not response:
    raise RuntimeError("there was no response")
else:
    res = response

if not res.text:
    raise RuntimeError("the response did not include a text response")
else:
    res_text = res.text

# Get Tokens from Response Object, either "prompt" or "response" tokens
def get_toks(res: GenerateContentResponse, tok_type: str):
    if tok_type not in ["prompt", "response"]:
        raise ValueError("tok_type must be either 'prompt' or 'response'")
    if not res.usage_metadata:
        raise RuntimeError("usage metadata not available")
    attr_type = "prompt_token_count" if tok_type == "prompt" else "candidates_token_count"
    toks = getattr(res.usage_metadata, attr_type, None)
    if not toks:
        raise RuntimeError(f"usage metadata does not contain {tok_type}")
    return f"{tok_type.capitalize()} tokens: {toks}"

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
    
    if args.verbose:
        get_verbose()
    
    try:
        print("Response: \n")
        print(res_text)
    except RuntimeError as e:
        print(e)

    



if __name__ == "__main__":
    main()
