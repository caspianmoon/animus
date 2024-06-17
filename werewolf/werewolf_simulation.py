# examples/werewolf_simulation.py

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from animus.simulation import Simulation
from animus.scenario_manager import ScenarioManager
from animus.utils import visualize_scenario, analyze_interactions
from custom_llm import GPT4LLM
from werewolf.werewolf_agents import WerewolfAgent
from werewolf.werewolf_scenario import WerewolfScenario

# Define a scenario
scenario = WerewolfScenario()

# Define the GPT-4 LLM integration
api_key = "your_openai_api_key_here"
llm = GPT4LLM(api_key)

# Define agents with roles
agent1 = WerewolfAgent("Alice", "Villager", llm)
agent2 = WerewolfAgent("Bob", "Werewolf", llm)
agent3 = WerewolfAgent("Charlie", "Seer", llm)
agent4 = WerewolfAgent("Dave", "Villager", llm)

# Add agents to the scenario
scenario.add_player(agent1)
scenario.add_player(agent2)
scenario.add_player(agent3)
scenario.add_player(agent4)

# Initialize Scenario Manager
manager = ScenarioManager(scenario)

# Initialize and run the simulation
sim = Simulation(scenario, [agent1, agent2, agent3, agent4], manager)
sim.run(steps=6)

# Visualize the scenario and analyze interactions
visualize_scenario(scenario)
analyze_interactions([agent1, agent2, agent3, agent4])