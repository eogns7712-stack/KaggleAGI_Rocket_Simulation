# benchmark_runner.py
def run_benchmark(model):
    evaluator = Evaluator()
    loop = MissionGameLoop(
        scenarios=SCENARIOS,
        evaluator=evaluator,
        max_steps=len(SCENARIOS),
    )
    return loop.run(model)


def pretty_print(title, results):
    print(f"\n===== {title} =====")
    print("TOTAL SCORE:", results["total_score"])
    print("DONE:", results["done"])
    print("NUM STEPS:", len(results["steps"]))

    print("\n--- FIRST 5 STEPS ---")
    for step in results["steps"][:5]:
        print(
            f"{step['id']} | "
            f"action={step['action']} | "
            f"score={step['score']} | "
            f"status={step['status']}"
        )


# ===== 실행 =====

rule_model = RuleBasedLLM()
rule_results = run_benchmark(rule_model)
pretty_print("RULE MODEL", rule_results)


dummy_model = DummyLLM()
dummy_results = run_benchmark(dummy_model)
pretty_print("DUMMY MODEL", dummy_results)