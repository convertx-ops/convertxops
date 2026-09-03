# Core agent: qualify inbound solar/roofing lead and book estimate.
# Reference impl. Swap telephony/LLM/calendar providers as needed.

from openai import OpenAI  # OpenAI-compatible; point base_url at local Ollama

CRITERIA = """
Qualify a solar/roofing lead. Extract: roof_type, service_area, timeline, budget_signals, intent.
Reply JSON only: {"qualified": bool, "roof_type": str, "area": str, "timeline": str, "notes": str}
"""

def qualify(transcript: str, base_url="http://localhost:11434/v1", model="qwen2.5:3b") -> dict:
    client = OpenAI(base_url=base_url, api_key="ollama")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CRITERIA},
            {"role": "user", "content": transcript},
        ],
        response_format={"type": "json_object"},
    )
    import json
    return json.loads(resp.choices[0].message.content)

def book(lead: dict):
    # Integrate Cal.com / Google Calendar here. Stub:
    return f"booked slot for {lead.get('area')} within {lead.get('timeline')}"

if __name__ == "__main__":
    sample = "Yeah I have a 2,000 sqft asphalt roof, in Austin, want solar before summer, got a quote already."
    lead = qualify(sample)
    print(lead)
    if lead.get("qualified"):
        print(book(lead))
