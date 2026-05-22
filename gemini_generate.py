# gemini_generate.py - Set up and call Gemini SDK (google.genai) to generate content

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from prompts import system_prompt
from functions.tool_schemas import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
gemini_model_string = os.environ.get("GEMINI_MODEL_STRING")

if not api_key:
    raise RuntimeError("Gemini API Key Not Found")

if not gemini_model_string:
    raise RuntimeError("Gemini Model Not Set. Please add the model string to your .env file, e.g. `gemini-2.5-flash`")

client = genai.Client(api_key=api_key)

def gemini(messages: list) -> types.GenerateContentResponse:
    response: types.GenerateContentResponse = client.models.generate_content(
        model=gemini_model_string,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    return response
