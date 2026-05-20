# get_tokens.py - Used by main.py when output is set to --verbose to show prompt and response tokens Used
# Extensible Func can accept either `prompt` or `response` for token type and the actual response object (res) and returns the tokens used.

from google.genai import types


# Get Tokens from Response Object, either "prompt" or "response" tokens
def get_toks(res: GenerateContentResponse, tok_type: str) -> str:
    if tok_type not in ["prompt", "response"]:
        raise ValueError("tok_type must be either 'prompt' or 'response'")
    if not res.usage_metadata:
        raise RuntimeError("usage metadata not available")
    attr_type = "prompt_token_count" if tok_type == "prompt" else "candidates_token_count"
    toks = getattr(res.usage_metadata, attr_type, None)
    if not toks:
        raise RuntimeError(f"usage metadata does not contain {tok_type}")
    return f"{tok_type.capitalize()} tokens: {toks}"

