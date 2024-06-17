# animus/simulation.py

import time
import logging


class Simulation:
    def __init__(self, scenario, agents, scenario_manager):
        self.scenario = scenario
        self.agents = agents
        self.scenario_manager = scenario_manager
        self.scenario.agents = agents
        logging.basicConfig(level=logging.INFO)

    def run(self, steps):
        for step in range(steps):
            logging.info(f"Step {step + 1}")
            for agent in self.agents:
                action = agent.act(self.scenario)
                self.scenario_manager.process_action(agent, action)
            self.scenario_manager.update_scenario()
            self.scenario_manager.handle_social_dynamics()  # Handle social dynamics
            self.scenario.check_triggers()  # Check triggers after each step
            time.sleep(1)  # Add delay to observe simulation steps

    def __str__(self):
        return f"Simulation(scenario={self.scenario}, agents={self.agents}, scenario_manager={self.scenario_manager})"
