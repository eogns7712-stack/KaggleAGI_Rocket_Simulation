from agi_benchmark.benchmark_runner import run_benchmark
from agi_benchmark.llm_rule import RuleBasedLLM
# from agi_benchmark.llm_gpt import GPTLLM
# from agi_benchmark.llm_gemini import GeminiLLM


def run():
    # Kaggle에서는 여기만 바꾸면 됨
    model = RuleBasedLLM()

    results = run_benchmark(model)

    print("TOTAL SCORE:", results["total_score"])
    print("STEPS:", len(results["steps"]))

    return results