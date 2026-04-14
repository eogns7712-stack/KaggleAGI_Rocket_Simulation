# llm_manager.py

import time

from llm_gpt import GPTLLM
from llm_gemini import GeminiLLM
from llm_rule import RuleBasedLLM
from llm_stub import DummyLLM


class LLMManager:
    def __init__(self):
        self.models = {
            "RULE": RuleBasedLLM(),
            "DUMMY": DummyLLM(),
            # "GEMINI": GeminiLLM(),
            # "GPT": GPTLLM(),
        }

        self.model_delays = {
            "RULE": 0.0,
            "DUMMY": 0.0,
            "GPT": 0.8,
            "GEMINI": 1.0,
        }

    def run_all(self, scenarios, evaluator):
        results = {}

        for name, model in self.models.items():
            total_score = 0
            total_correct = 0
            total_partial = 0
            total_invalid = 0
            total_critical_fails = 0
            phase_scores = {}
            details = []

            print(f"\n===== {name} =====")

            per_call_delay = self.model_delays.get(name, 0.0)

            for sc in scenarios:
                # Gemini가 quota로 죽은 뒤에는 더 이상 소모 호출 안 하게 처리
                if hasattr(model, "disabled") and model.disabled:
                    action = None
                    result = {
                        "score": 0,
                        "success": False,
                        "status": f"skipped_model_disabled:{getattr(model, 'disable_reason', 'unknown')}",
                        "critical_failed": False,
                    }
                else:
                    action = model.predict(sc["state"], sc["valid_actions"])
                    result = evaluator.evaluate(sc, action)

                score = result["score"]
                status = result["status"]

                total_score += score
                phase_scores[sc["phase"]] = phase_scores.get(sc["phase"], 0) + score

                if result["success"]:
                    total_correct += 1
                if status == "partial":
                    total_partial += 1
                if status in ("invalid_output", "invalid_action"):
                    total_invalid += 1
                if result["critical_failed"]:
                    total_critical_fails += 1

                details.append({
                    "id": sc["id"],
                    "phase": sc["phase"],
                    "action": action,
                    "score": score,
                    "status": status,
                    "critical": sc.get("critical", False),
                })

                print(
                    f"[{sc['id']}] "
                    f"action={action} | score={score} | status={status}"
                )

                if per_call_delay > 0:
                    time.sleep(per_call_delay)

            results[name] = {
                "total_score": total_score,
                "correct_count": total_correct,
                "partial_count": total_partial,
                "invalid_count": total_invalid,
                "critical_fail_count": total_critical_fails,
                "phase_scores": phase_scores,
                "details": details,
            }

            print(f"{name} TOTAL SCORE: {total_score}")
            print(f"{name} CORRECT: {total_correct}")
            print(f"{name} PARTIAL: {total_partial}")
            print(f"{name} INVALID: {total_invalid}")
            print(f"{name} CRITICAL FAILS: {total_critical_fails}")

        return results