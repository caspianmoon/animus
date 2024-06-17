# werewolf/werewolf_scenario.py

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from animus.scenario import Scenario


class WerewolfScenario(Scenario):
    def __init__(self):
        description = "A village where some villagers are werewolves."
        super().__init__(description)
        self.day = 1
        self.phase = "night"
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def next_phase(self):
        if self.phase == "night":
            self.phase = "day"
        else:
            self.phase = "night"
            self.day += 1
        self.add_event(
            f"Day {self.day} - {self.phase.capitalize()} phase starts.")

    def __str__(self):
        return f"WerewolfScenario(day={self.day}, phase={self.phase}, players={self.players})"
