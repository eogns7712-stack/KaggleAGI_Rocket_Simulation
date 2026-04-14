# llm_gemini.py

import os
from google import genai

from utils import state_to_prompt, extract_action


class GeminiLLM:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 없습니다.")

        self.client = genai.Client(api_key=api_key)

        # quota 문제 발생 시 이번 실행 동안 비활성화
        self.disabled = False
        self.disable_reason = None

    def predict(self, state, valid_actions):
        if self.disabled:
            print(f"Gemini skipped: {self.disable_reason}")
            return None

        prompt = state_to_prompt(state, valid_actions)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )

            text = response.text or ""
            return extract_action(text, valid_actions)

        except Exception as e:
            error_text = str(e)
            error_lower = error_text.lower()

            print(f"Gemini error: {e}")

            # 핵심: quota가 0이면 더 이상 시도하지 않음
            if (
                "limit: 0" in error_lower
                or "resource_exhausted" in error_lower
                or "generaterequestsperdayperprojectperformodel-freetier" in error_lower
                or "generatecontentinputtokensperformodelperminute-freetier" in error_lower
            ):
                self.disabled = True
                self.disable_reason = "quota exhausted"
                print(f"Gemini disabled for this run: {self.disable_reason}")

            return None