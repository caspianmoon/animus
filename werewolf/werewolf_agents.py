# werewolf/werewolf_agents.py

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from animus.agents import Agent

class WerewolfAgent(Agent):
    def __init__(self, name, role, llm=None):
        super().__init__(name, llm)
        self.role = role
        self.alive = True

    def generate_action(self, scenario):
        if not self.llm:
            return "Default action"
        
        prompt = f"The scenario is: {scenario.description}. {self.name} is a {self.role}. The current phase is {scenario.phase}. What should {self.name} do next? Consider the current situation and the roles of other players."
        messages = [
            {"role": "system", "content": "You are a Werewolf game assistant."},
            {"role": "user", "content": prompt}
        ]
        action = self.llm.generate_action(messages)
        return action

    def act(self, scenario):
        if not self.alive:
            return f"{self.name} is dead and cannot act."
        
        if scenario.phase == "night":
            if self.role == "Werewolf":
                return self.werewolf_action(scenario)
            elif self.role == "Seer":
                return self.seer_action(scenario)
            else:
                return f"{self.name} (Villager) sleeps."
        elif scenario.phase == "day":
            return self.day_action(scenario)
    
    def werewolf_action(self, scenario):
        targets = [player for player in scenario.players if player.alive and player.role != "Werewolf"]
        if targets:
            prompt = f"As a Werewolf, {self.name} needs to decide whom to kill among {', '.join([t.name for t in targets])}. Provide a dialogue-like response explaining the choice."
            messages = [
                {"role": "system", "content": "You are a Werewolf game assistant."},
                {"role": "user", "content": prompt}
            ]
            action = self.llm.generate_action(messages)
            chosen_target = next((t for t in targets if t.name in action), targets[0])
            chosen_target.alive = False
            return action
        return f"{self.name} (Werewolf) finds no one to kill."

    def seer_action(self, scenario):
        targets = [player for player in scenario.players if player.alive and player != self]
        if targets:
            prompt = f"As a Seer, {self.name} needs to decide whom to investigate among {', '.join([t.name for t in targets])}. Provide a dialogue-like response explaining the choice and the result."
            messages = [
                {"role": "system", "content": "You are a Werewolf game assistant."},
                {"role": "user", "content": prompt}
            ]
            action = self.llm.generate_action(messages)
            chosen_target = next((t for t in targets if t.name in action), targets[0])
            return action
        return f"{self.name} (Seer) finds no one to investigate."

    def day_action(self, scenario):
        if self.alive:
            targets = [player for player in scenario.players if player.alive and player != self]
            if targets:
                prompt = f"As a {self.role}, {self.name} needs to decide whom to vote to lynch among {', '.join([t.name for t in targets])}. Provide a dialogue-like response explaining the choice."
                messages = [
                    {"role": "system", "content": "You are a Werewolf game assistant."},
                    {"role": "user", "content": prompt}
                ]
                action = self.llm.generate_action(messages)
                chosen_target = next((t for t in targets if t.name in action), targets[0])
                chosen_target.alive = False if "lynch" in action else chosen_target.alive
                return action
        return f"{self.name} cannot participate in the vote because they are dead."