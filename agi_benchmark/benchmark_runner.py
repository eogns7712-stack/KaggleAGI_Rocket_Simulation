# benchmark_runner.py

from agi_benchmark.scenarios import SCENARIOS
from agi_benchmark.evaluator import Evaluator
from agi_benchmark.game_loop import MissionGameLoop


def run_benchmark(model):
    evaluator = Evaluator()
    loop = MissionGameLoop(
        scenarios=SCENARIOS,
        evaluator=evaluator,
        max_steps=len(SCENARIOS),
    )
    return loop.run(model)