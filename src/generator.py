import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.config import MODEL_NAME, CONFIDENCE_THRESHOLD

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)

def generate_handoff_summary(user_query: str, persona: str, context_chunks: list) -> str:
    handoff_data = {
        'persona': persona,
        'detected_issue': user_query[:100] + '...' ,
        'retrieved_sources': [chunk['source'] for chunk in context_chunks],
        'confidence_score': max([chunk['score'] for chunk in context_chunks]) if context_chunks else 0.0,
        'recommended_action': 'Review the retrieved sources and contact the customer directly.'
    }

    return json.dumps(handoff_data, indent=2)

def generate_adaptive_response(user_query: str, persona: str, context_chunks: list) -> dict:
    best_score = max([chunk['score'] for chunk in context_chunks]) if context_chunks else 0.0

    if best_score < CONFIDENCE_THRESHOLD or not context_chunks:
        return {
            'escalated': True,
            'response': "I’m sorry, but I could not find enough reliable information in the support documents. I’m escalating this to a human support specialist.",
            'handoff_summary': generate_handoff_summary(user_query, persona, context_chunks)
        }
    
    if persona == "Technical Expert":
        persona_instructions = (
            "You are a Senior Systems Engineer. Give precise technical steps, mention headers, "
            "status codes, configuration checks, and concise diagnostics where relevant."
        )
    elif persona == "Frustrated User":
        persona_instructions = (
            "You are an empathetic customer support specialist. Start with a short apology or validation. "
            "Use simple language and clear step-by-step actions. Avoid heavy jargon."
        )
    else:
        persona_instructions = (
            "You are a concise client relations manager. Focus on business impact, resolution path, "
            "timeline expectations, and keep the answer brief and professional."
        )
    
    context_text = '\n\n'.join([f"Source: [{chunk['source']}]: {chunk['text']}" for chunk in context_chunks])

    system_prompt = (
        f"{persona_instructions}\n\n"
        "CRITICAL RULES:\n"
        "- Answer ONLY using the provided support context.\n"
        "- Do not invent policies, timelines, or technical details.\n"
        "- If the context is insufficient, say that the issue should be escalated.\n\n"
        f"SUPPORT CONTEXT:\n{context_text}"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2
        )
    )

    return {
        'escalated': False,
        'response': response.text.strip(),
        'handoff_summary': None
    }



