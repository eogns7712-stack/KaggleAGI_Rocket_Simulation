# utils.py

import json
import re


def state_to_prompt(state, valid_actions):
    state_text = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True)
    actions_text = ", ".join(valid_actions)

    return f"""You are a mission decision model.

Read the mission state and choose exactly ONE action from AVAILABLE ACTIONS.

STATE:
{state_text}

AVAILABLE ACTIONS:
{actions_text}

Rules:
- Return exactly one action from AVAILABLE ACTIONS
- Do not explain
- Do not add extra text
- Preferred output format: ACTION: <action>

OUTPUT:
"""


def extract_action(text, valid_actions):
    if not text:
        return None

    valid_map = {action.upper(): action for action in valid_actions}

    cleaned = text.strip()
    cleaned = cleaned.replace("```", "").strip()

    match = re.search(r"ACTION\s*:\s*([A-Z0-9_]+)", cleaned, re.IGNORECASE)
    if match:
        candidate = match.group(1).strip().upper()
        return valid_map.get(candidate)

    first_line = cleaned.splitlines()[0].strip().strip('"').strip("'").upper()
    first_line = re.sub(r"[^A-Z0-9_]", "", first_line)

    return valid_map.get(first_line)