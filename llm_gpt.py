# llm_gpt.py

import os
from openai import OpenAI

from utils import state_to_prompt, extract_action


class GPTLLM:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 없습니다.")
        self.client = OpenAI(api_key=api_key)

    def predict(self, state, valid_actions):
        prompt = state_to_prompt(state, valid_actions)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
            )

            text = response.choices[0].message.content or ""
            return extract_action(text, valid_actions)

        except Exception as e:
            print("GPT error:", e)
            return None