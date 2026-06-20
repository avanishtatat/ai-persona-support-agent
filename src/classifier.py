import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.config import MODEL_NAME

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

def classify_persona(user_message: str) -> dict:
    """
    Analyzes the user's message and classifies it into one of the three target personas.
    """
    # Initialize the Gemini GenAI Client
    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are an advanced customer persona classification engine.\n\n"
        "Classify the customer's message into exactly one of these personas:\n\n"
        "1. Technical Expert\n"
        "- Uses technical terminology such as APIs, authentication, tokens, logs, HTTP status codes, SDKs, configurations, deployments, stack traces, code snippets, or infrastructure.\n"
        "- Even if the message is urgent or frustrated, classify as Technical Expert if technical content is the dominant characteristic.\n\n"
        "2. Frustrated User\n"
        "- Expresses strong emotions, confusion, anger, disappointment, or urgency.\n"
        "- Usually describes symptoms without deep technical vocabulary.\n"
        "- Prioritize this only when emotion is stronger than technical content.\n\n"
        "3. Business Executive\n"
        "- Focuses on business impact, customers, deadlines, revenue, SLAs, operations, or timelines rather than technical implementation.\n\n"
        "Decision Rules:\n"
        "- If a message contains significant technical terminology, choose Technical Expert.\n"
        "- Do not classify as Frustrated User solely because words like \"urgent\", \"immediately\", or \"not working\" appear.\n"
        "- Only choose Frustrated User when emotional language is the dominant feature.\n"
        "- Return exactly one persona.\n\n"
        "Provide the response in the requested JSON schema."
    )

    # Define structured schema output
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": ["Technical Expert", "Frustrated User", "Business Executive"]
            },
            "confidence": {"type": "NUMBER"},
            "reasoning": {"type": "STRING"}
        },
        "required": ["persona", "confidence", "reasoning"]
    }

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0.1
        )
    )

    return json.loads(response.text.strip())

# Example usage check
if __name__ == "__main__":
    test_msg = [
        "Our production API key stopped working with a 401 Unauthorized block. Check our logs immediately.",
        "This application is terrible! Nothing is working and I'm extremely frustrated!",
        "This issue is delaying our client delivery. What is the expected resolution timeline?"
    ]
    for msg in test_msg:
        result = classify_persona(msg)
        print("=" * 60)
        print(f"User Message: {msg}")
        print(json.dumps(result, indent=2))