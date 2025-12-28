from langchain_community.llms import ollama
import json
import re
from datetime import datetime

# Initialize model (CPU-safe)
llm = ollama.Ollama(model="llama3", temperature=0.7)

def extract_structured_data(article_text: str):
    prompt = f"""
You are an information extraction system.

Return ONLY valid JSON in this exact format:

{{
  "state_summary": "2–3 sentence summary",
  "evidence": ["fact1", "fact2", "fact3"],
  "metadata": {{
    "source_type": "news",
    "startup_name": "",
    "investor_name": "",
    "funding_stage": "",
    "startup_location": "",
    "investor_location": ""
  }},
  "confidence": 0.0
}}

ARTICLE:
{article_text}
"""

    try:
        response = llm.invoke(prompt)

        # 🔧 Extract JSON safely
        match = re.search(r"\{[\s\S]*\}", response)
        if not match:
            raise ValueError("No JSON detected in model output")

        parsed = json.loads(match.group())

        parsed["processed_at"] = datetime.utcnow().isoformat()
        parsed["model"] = "llama3"

        return parsed

    except Exception as e:
        return {
            "state_summary": "",
            "evidence": [],
            "metadata": {},
            "confidence": 0.0,
            "error": str(e),
            "raw_output": response if isinstance(response, str) else "",
            "processed_at": datetime.utcnow().isoformat()
        }
