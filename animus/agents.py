# animus/agents.py

import json
from collections.abc import Callable, Iterable
import numpy as np


class Agent:
    def __init__(self, name, role, llm, memory_model, traits=None, components=None):
        self.name = name
        self.role = role
        self.llm = llm
        self.memory_model = memory_model
        self.state = {"status": "active", "emotions": {},
                      "goals": [], "traits": traits or {}}
        self.memory = []
        self.components = components or []
        self.behavior_config = {}

    def set_llm(self, llm):
        self.llm = llm

    def update_memory(self, observation):
        self.memory_model.add(observation)
        if len(self.memory) > 100:  # Limit memory size for performance
            self.memory.pop(0)

    def update_emotions(self, new_emotions):
        self.state["emotions"].update(new_emotions)

    def set_goals(self, goals):
        self.state["goals"] = goals

    def set_components(self, components):
        self.components = components

    def set_behavior_config(self, config):
        self.behavior_config = config

    def generate_action(self, scenario):
        if not self.llm:
            return "Default action"

        # Use last 10 memories
        memory_text = " ".join(self.memory_model.retrieve_recent(10))
        component_states = {comp.name(): comp.state()
                            for comp in self.components}
        prompt = (
            f"Scenario: {scenario.description}. "
            f"Current phase: {scenario.phase}. "
            f"{self.name} is a {self.role} and currently has the state {json.dumps(self.state)}. "
            f"Memory: {memory_text}. "
            f"Components: {json.dumps(component_states)}. "
            f"What should {self.name} do next considering the roles, states, emotions, goals, traits, and interactions of all participants?"
        )
        messages = [
            {"role": "system", "content": "You are a simulation assistant."},
            {"role": "user", "content": prompt}
        ]
        action = self.llm.generate_action(messages)
        return action

    def act(self, scenario):
        action = self.generate_action(scenario)
        scenario.add_event(f"{self.name} ({self.role}) decides to: {action}")
        self.update_memory(f"{self.name} ({self.role}) decides to: {action}")
        self.process_emotions(action)
        return action

    def process_emotions(self, action):
        for trigger, emotion_update in self.behavior_config.get("emotions", {}).items():
            if trigger in action:
                self.update_emotions(emotion_update)

    def process_state(self):
        for condition, update in self.behavior_config.get("state_transitions", {}).items():
            if eval(condition, {"state": self.state}):
                self.state.update(update)

    def __str__(self):
        return f"Agent(name={self.name}, role={self.role}, state={self.state})"
