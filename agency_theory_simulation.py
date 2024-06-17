import sys
import os
import json
import numpy as np
from animus.simulation import Simulation
from animus.scenario_manager import ScenarioManager
from animus.utils import visualize_scenario, analyze_interactions
from animus.agents import Agent
from animus.scenario import Scenario
from animus.trigger import Trigger
from custom_llm import GPT4LLM

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define a simple memory model for the agents


class SimpleMemoryModel:
    def __init__(self):
        self.memory = []

    def add(self, memory):
        self.memory.append(memory)
        if len(self.memory) > 100:  # Limit memory size for performance
            self.memory.pop(0)

    def retrieve_recent(self, n):
        return self.memory[-n:]


# Define a dynamic configuration for the simulation
dynamic_config = {
    "api_key": "",
    "scenario": {
        "description": "A corporate environment where managers make decisions on behalf of shareholders.",
        "context": "Company operations and performance."
    },
    "agents": [
        {
            "name": "Manager1",
            "role": "Manager",
            "traits": {"risk_averse": True, "self_interested": True},
            "components": [],
            "goals": ["Maximize personal bonus", "Achieve company targets"],
            "behavior_config": {
                "emotions": {
                    "achieve_goal": {"satisfied": True},
                    "fail_goal": {"frustrated": True}
                },
                "state_transitions": {
                    "state['status'] == 'overworked'": {"status": "inactive"}
                },
                "relationship_rules": [
                    {
                        "condition": "lambda relationship: relationship > 0",
                        "emotions": {"happy": True}
                    },
                    {
                        "condition": "lambda relationship: relationship < 0",
                        "emotions": {"angry": True}
                    }
                ]
            }
        },
        {
            "name": "Shareholder1",
            "role": "Shareholder",
            "traits": {"profit_oriented": True, "demanding": True},
            "components": [],
            "goals": ["Maximize company profit", "Ensure manager accountability"],
            "behavior_config": {
                "emotions": {
                    "achieve_profit": {"satisfied": True},
                    "lose_profit": {"dissatisfied": True}
                },
                "state_transitions": {
                    "state['status'] == 'dissatisfied'": {"status": "active"}
                },
                "relationship_rules": [
                    {
                        "condition": "lambda relationship: relationship > 0",
                        "emotions": {"content": True}
                    },
                    {
                        "condition": "lambda relationship: relationship < 0",
                        "emotions": {"dissatisfied": True}
                    }
                ]
            }
        }
    ],
    "triggers": [
        {
            "condition": "lambda scenario: scenario.phase == 'midday'",
            "action": "lambda scenario: scenario.update_environment('time', 'afternoon')"
        }
    ],
    "simulation": {
        "steps": 4
    }
}

# Load configuration for the simulation
config = dynamic_config

# Define a scenario based on the configuration
scenario = Scenario(
    description=config["scenario"]["description"], context=config["scenario"]["context"])

# Define the GPT-4 LLM integration
api_key = config["api_key"]
llm = GPT4LLM(api_key)

# Define agents with roles and traits from the configuration
agents = []
for agent_config in config["agents"]:
    memory_model = SimpleMemoryModel()
    agent = Agent(agent_config["name"], agent_config["role"],
                  llm, memory_model, traits=agent_config["traits"])
    agent.set_components(agent_config["components"])
    agent.set_goals(agent_config["goals"])
    agent.set_behavior_config(agent_config["behavior_config"])
    agents.append(agent)

# Add agents to the scenario
for agent in agents:
    scenario.add_agent(agent)

# Define triggers from the configuration
for trigger_config in config["triggers"]:
    condition = eval(trigger_config["condition"])
    action = eval(trigger_config["action"])
    trigger = Trigger(condition, action)
    scenario.add_trigger(trigger)

# Initialize Scenario Manager
manager = ScenarioManager(scenario)

# Initialize and run the simulation
sim = Simulation(scenario, agents, manager)
sim.run(config["simulation"]["steps"])

# Visualize the scenario and analyze interactions
visualize_scenario(scenario)
analyze_interactions(agents)
