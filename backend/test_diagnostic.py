import os
import sys
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

results = {
    "gemini-2.5-flash": None,
    "gemini-3.5-flash": None
}

try:
    client = genai.Client(api_key=api_key)
    
    # Test 1: gemini-2.5-flash
    try:
        response = client.interactions.create(
            model="gemini-2.5-flash",
            input="Reply with exactly: Gemini access test successful."
        )
        results["gemini-2.5-flash"] = {"status": "SUCCESS"}
    except Exception as e:
        results["gemini-2.5-flash"] = {"status": "FAILURE", "error": str(e)}

    # Test 2: alternative model (gemini-3.5-flash)
    try:
        response2 = client.interactions.create(
            model="gemini-3.5-flash",
            input="Reply with exactly: Gemini access test successful."
        )
        results["gemini-3.5-flash"] = {"status": "SUCCESS"}
    except Exception as e:
        results["gemini-3.5-flash"] = {"status": "FAILURE", "error": str(e)}

except Exception as e:
    results["client_init_error"] = str(e)

print(json.dumps(results))
