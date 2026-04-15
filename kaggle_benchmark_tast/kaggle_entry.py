# ===== pretty 출력 함수 =====

def pretty_summary(title, results):
    print(f"\n===== {title} =====")
    print(f"TOTAL SCORE : {results['total_score']}")
    print(f"DONE        : {results['done']}")
    print(f"NUM STEPS   : {len(results['steps'])}")


def pretty_steps(results, n=5):
    print("\n--- SAMPLE STEPS ---")
    for step in results["steps"][:n]:
        print(
            f"{step['id']} | "
            f"{step['action']:>18} | "
            f"{step['status']:>10} | "
            f"{step['score']:>4}"
        )


def compare(rule_results, dummy_results):
    print("\n===== COMPARISON =====")
    print(f"RULE  TOTAL SCORE : {rule_results['total_score']}")
    print(f"DUMMY TOTAL SCORE : {dummy_results['total_score']}")
    print(f"DIFF              : {rule_results['total_score'] - dummy_results['total_score']}")


# ===== 실행 =====

rule_results = run_benchmark(RuleBasedLLM())
dummy_results = run_benchmark(DummyLLM())

# 요약
pretty_summary("RULE MODEL", rule_results)
pretty_steps(rule_results)

pretty_summary("DUMMY MODEL", dummy_results)
pretty_steps(dummy_results)

# 비교
compare(rule_results, dummy_results)