import json
import re
from planner.prompt import SYSTEM_PROMPT
from planner.llm_client import call_llm


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def generate_learning_plan(skills, target, time_commitment, difficulty):

    if not skills or not target:
        return {"error": "Inputs cannot be empty"}

    user_prompt = f"""
    Current Skills: {skills}
    Target Role: {target}
    Daily Time Available: {time_commitment}
    Difficulty Level: {difficulty}
    """

    try:
        response = call_llm([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ])

        print("RAW LLM RESPONSE:", response)  

        json_text = extract_json(response)

        if not json_text:
            return {"error": "AI did not return valid JSON"}

        return json.loads(json_text)

    except Exception as e:
        return {"error": str(e)}