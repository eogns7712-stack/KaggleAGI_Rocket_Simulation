# llm_stub.py

import random


class DummyLLM:
    def predict(self, state, valid_actions):
        return random.choice(valid_actions)