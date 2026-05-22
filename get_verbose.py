# get_verbose.py - setup verbose output for main.py when it is called with --verbose arg 

from google.genai import types 
from get_tokens import get_tokens, TokenType

def get_verbose(user_prompt: str, response: types.GenerateContentResponse) -> str:

    verbose: str = "\n"

    try:
        verbose += f"User prompt: {user_prompt} \n"

        prompt_tok_msg = get_tokens(response, TokenType.PROMPT)

        response_tok_msg = get_tokens(response, TokenType.RESPONSE)

        verbose += f"{prompt_tok_msg}\n{response_tok_msg}\n"
        
        return verbose

    except (RuntimeError, ValueError) as e:
        return f"Error retrieving tokens: {e}"

