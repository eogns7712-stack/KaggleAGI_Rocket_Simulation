# game_loop.py

from copy import deepcopy


class MissionGameLoop:
    def __init__(self, scenarios, evaluator, max_steps=50):
        self.scenarios = scenarios
        self.evaluator = evaluator
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        self.current_index = 0
        self.total_score = 0
        self.done = False
        self.history = []

    def get_current_scenario(self):
        if self.current_index >= len(self.scenarios):
            self.done = True
            return None
        return self.scenarios[self.current_index]

    def step(self, model):
        if self.done:
            return None

        scenario = self.get_current_scenario()
        if scenario is None:
            return None

        state = deepcopy(scenario["state"])
        valid_actions = scenario["valid_actions"]

        action = model.predict(state, valid_actions)
        result = self.evaluator.evaluate(scenario, action)

        self.total_score += result["score"]

        step_record = {
            "id": scenario["id"],
            "phase": scenario["phase"],
            "state": state,
            "action": action,
            "score": result["score"],
            "status": result["status"],
            "critical": scenario.get("critical", False),
            "critical_failed": result["critical_failed"],
        }
        self.history.append(step_record)

        self.current_index += 1
        if self.current_index >= len(self.scenarios):
            self.done = True

        return step_record

    def run(self, model):
        self.reset()

        while not self.done and self.current_index < self.max_steps:
            self.step(model)

        return {
            "total_score": self.total_score,
            "steps": self.history,
            "done": self.done,
        }