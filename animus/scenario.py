# animus/scenario.py

from collections import defaultdict


class Scenario:
    def __init__(self, description, phase="initial", context=""):
        self.description = description
        self.phase = phase
        self.context = context
        self.events = []
        self.agents = []
        self.environment = {}
        self.relationships = defaultdict(lambda: defaultdict(int))
        self.triggers = []

    def add_event(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_environment(self, key, value):
        self.environment[key] = value

    def get_environment(self):
        return self.environment

    def update_relationship(self, agent1, agent2, change):
        self.relationships[agent1][agent2] += change

    def get_relationship(self, agent1, agent2):
        return self.relationships[agent1][agent2]

    def add_trigger(self, trigger):
        self.triggers.append(trigger)

    def check_triggers(self):
        for trigger in self.triggers:
            if trigger.condition(self):
                trigger.action(self)

    def __str__(self):
        return f"Scenario(description={self.description}, phase={self.phase}, context={self.context}, events={self.events}, agents={self.agents}, environment={self.environment})"
