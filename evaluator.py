# evaluator.py

def eval_condition(cond, state):
    try:
        return bool(eval(cond, {"__builtins__": {}}, dict(state)))
    except Exception:
        return False


class Evaluator:
    def evaluate(self, scenario, action):
        valid_actions = scenario["valid_actions"]
        is_critical_scenario = scenario.get("critical", False)

        # -----------------------------
        # 설정값
        # -----------------------------
        invalid_output_penalty = scenario.get("invalid_output_penalty", -10)
        invalid_action_penalty = scenario.get("invalid_action_penalty", -12)
        wrong_action_penalty = scenario.get("wrong_action_penalty", -8)
        success_reward = scenario.get("success_reward", 10)

        # 핵심: critical fail 추가 벌점
        critical_fail_extra_penalty = scenario.get(
            "critical_fail_extra_penalty",
            -60
        )

        # 핵심: critical scenario에서 단순 오답도 더 세게
        critical_wrong_action_extra_penalty = scenario.get(
            "critical_wrong_action_extra_penalty",
            -12
        )

        # -----------------------------
        # 1) 출력 없음
        # -----------------------------
        if action is None:
            score = invalid_output_penalty

            # critical scenario면 출력 없음도 더 치명적으로
            if is_critical_scenario:
                score += scenario.get("critical_invalid_extra_penalty", -15)

            return {
                "score": score,
                "success": False,
                "status": "invalid_output",
                "critical_failed": False,
            }

        # -----------------------------
        # 2) valid_actions 밖의 행동
        # -----------------------------
        if action not in valid_actions:
            score = invalid_action_penalty

            if is_critical_scenario:
                score += scenario.get("critical_invalid_extra_penalty", -15)

            return {
                "score": score,
                "success": False,
                "status": "invalid_action",
                "critical_failed": False,
            }

        # -----------------------------
        # 3) 명시적 실패 조건 검사
        # -----------------------------
        for fail in scenario.get("failure_conditions", []):
            if not isinstance(fail, dict):
                continue

            if action == fail.get("action"):
                if eval_condition(fail.get("condition", "False"), scenario["state"]):
                    base_penalty = fail.get("penalty", -20)
                    fail_is_critical = fail.get("critical", is_critical_scenario)

                    score = base_penalty
                    status = fail.get("label", "failure_condition")

                    # critical fail이면 추가 벌점 부여
                    if fail_is_critical:
                        score += critical_fail_extra_penalty

                    return {
                        "score": score,
                        "success": False,
                        "status": status,
                        "critical_failed": fail_is_critical,
                    }

        # -----------------------------
        # 4) 정답
        # -----------------------------
        if action == scenario["correct_action"]:
            return {
                "score": success_reward,
                "success": True,
                "status": "correct",
                "critical_failed": False,
            }

        # -----------------------------
        # 5) 부분점수
        # -----------------------------
        partial_credit = scenario.get("partial_credit", {})
        if action in partial_credit:
            score = partial_credit[action]

            # critical scenario에서 부분점수 행동도 너무 느슨하면 추가 감점 가능
            if is_critical_scenario and score <= 0:
                score += scenario.get("critical_partial_extra_penalty", -3)

            return {
                "score": score,
                "success": False,
                "status": "partial",
                "critical_failed": False,
            }

        # -----------------------------
        # 6) 일반 오답
        # -----------------------------
        score = wrong_action_penalty

        # critical scenario에서 일반 오답은 추가 감점
        if is_critical_scenario:
            score += critical_wrong_action_extra_penalty

        return {
            "score": score,
            "success": False,
            "status": "wrong_action",
            "critical_failed": False,
        }