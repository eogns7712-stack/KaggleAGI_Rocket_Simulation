# main.py

import json

from scenarios import SCENARIOS
from evaluator import Evaluator
from llm_manager import LLMManager


MISSION_COMPLETION_BONUS = 50
PERFECT_RUN_BONUS = 25
NO_CRITICAL_FAIL_BONUS = 15


def apply_bonuses(results):
    """
    모델별 상세 결과를 보고 보너스 점수 추가
    """
    for model_name, info in results.items():
        details = info.get("details", [])

        total_scenarios = len(details)
        correct_count = info.get("correct_count", 0)
        critical_fail_count = info.get("critical_fail_count", 0)
        invalid_count = info.get("invalid_count", 0)

        mission_completed = (
            correct_count == total_scenarios
            and critical_fail_count == 0
            and invalid_count == 0
        )

        bonus = 0
        bonus_reasons = []

        # 전체 미션 완주 보너스
        if mission_completed:
            bonus += MISSION_COMPLETION_BONUS
            bonus_reasons.append(f"mission_completion:+{MISSION_COMPLETION_BONUS}")

        # 완벽한 정답 런
        if correct_count == total_scenarios:
            bonus += PERFECT_RUN_BONUS
            bonus_reasons.append(f"perfect_run:+{PERFECT_RUN_BONUS}")

        # 치명적 실패 0회
        if critical_fail_count == 0:
            bonus += NO_CRITICAL_FAIL_BONUS
            bonus_reasons.append(f"no_critical_fail:+{NO_CRITICAL_FAIL_BONUS}")

        info["bonus_score"] = bonus
        info["bonus_reasons"] = bonus_reasons
        info["final_score"] = info["total_score"] + bonus

    return results


def build_summary(results):
    summary = {}

    phase_names = sorted({sc["phase"] for sc in SCENARIOS})

    for model_name, info in results.items():
        details = info.get("details", [])
        phase_scores = info.get("phase_scores", {})

        phase_success = {phase: {"correct": 0, "total": 0} for phase in phase_names}
        critical_fail_details = []
        worst_failures = []

        for item in details:
            phase = item["phase"]
            status = item["status"]
            score = item["score"]

            phase_success[phase]["total"] += 1
            if status == "correct":
                phase_success[phase]["correct"] += 1

            if item.get("critical", False) and score < 0:
                worst_failures.append({
                    "id": item["id"],
                    "phase": item["phase"],
                    "action": item["action"],
                    "score": score,
                    "status": status,
                })

            if status not in ("correct", "partial") and "critical" in status:
                critical_fail_details.append({
                    "id": item["id"],
                    "phase": item["phase"],
                    "action": item["action"],
                    "score": score,
                    "status": status,
                })

        # 점수 낮은 순으로 5개
        worst_failures = sorted(worst_failures, key=lambda x: x["score"])[:5]

        phase_success_rate = {}
        for phase, stats in phase_success.items():
            total = stats["total"]
            correct = stats["correct"]
            rate = (correct / total * 100.0) if total > 0 else 0.0
            phase_success_rate[phase] = {
                "correct": correct,
                "total": total,
                "success_rate_percent": round(rate, 1),
                "phase_score": phase_scores.get(phase, 0),
            }

        summary[model_name] = {
            "final_score": info["final_score"],
            "raw_score": info["total_score"],
            "bonus_score": info["bonus_score"],
            "bonus_reasons": info["bonus_reasons"],
            "correct_count": info["correct_count"],
            "partial_count": info["partial_count"],
            "invalid_count": info["invalid_count"],
            "critical_fail_count": info["critical_fail_count"],
            "phase_success_rate": phase_success_rate,
            "worst_failures": worst_failures,
            "critical_fail_details": critical_fail_details,
        }

    return summary


def print_summary(results, summary):
    print("\n===== FINAL RESULT =====")

    for model_name, info in results.items():
        print(f"\n[{model_name}]")
        print(f"RAW SCORE: {info['total_score']}")
        print(f"BONUS SCORE: {info['bonus_score']}")
        print(f"FINAL SCORE: {info['final_score']}")
        print(f"CORRECT: {info['correct_count']}")
        print(f"PARTIAL: {info['partial_count']}")
        print(f"INVALID: {info['invalid_count']}")
        print(f"CRITICAL FAILS: {info['critical_fail_count']}")
        print(f"PHASE SCORES: {info['phase_scores']}")

        if info["bonus_reasons"]:
            print("BONUSES:")
            for reason in info["bonus_reasons"]:
                print(f"  - {reason}")

        print("PHASE SUCCESS:")
        for phase, stats in summary[model_name]["phase_success_rate"].items():
            print(
                f"  - {phase}: "
                f"{stats['correct']}/{stats['total']} "
                f"({stats['success_rate_percent']}%) "
                f"| score={stats['phase_score']}"
            )

        worst_failures = summary[model_name]["worst_failures"]
        if worst_failures:
            print("WORST FAILURES:")
            for wf in worst_failures:
                print(
                    f"  - [{wf['id']}] phase={wf['phase']} "
                    f"action={wf['action']} score={wf['score']} status={wf['status']}"
                )


def run():
    evaluator = Evaluator()
    manager = LLMManager()

    results = manager.run_all(SCENARIOS, evaluator)
    results = apply_bonuses(results)
    summary = build_summary(results)

    print_summary(results, summary)

    payload = {
        "results": results,
        "summary": summary,
        "scenario_count": len(SCENARIOS),
        "mission_completion_bonus": MISSION_COMPLETION_BONUS,
        "perfect_run_bonus": PERFECT_RUN_BONUS,
        "no_critical_fail_bonus": NO_CRITICAL_FAIL_BONUS,
    }

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("\nresults.json 저장 완료")


if __name__ == "__main__":
    run()