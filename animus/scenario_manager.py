# animus/scenario_manager.py

class ScenarioManager:
    def __init__(self, scenario):
        self.scenario = scenario

    def process_action(self, agent, action):
        action_description = f"{agent.name} ({agent.role}) performs: {action}"
        self.scenario.add_event(action_description)
        self.scenario.check_triggers()

    def update_scenario(self):
        for agent in self.scenario.agents:
            agent.process_state()
        self.handle_social_dynamics()

    def handle_social_dynamics(self):
        for agent in self.scenario.agents:
            for other_agent in self.scenario.agents:
                if agent != other_agent:
                    relationship = self.scenario.get_relationship(
                        agent.name, other_agent.name)
                    for rule in agent.behavior_config.get("relationship_rules", []):
                        if eval(rule["condition"], {"relationship": relationship}):
                            agent.update_emotions(rule["emotions"])

    def handle_relationships(self, agent1, agent2, change):
        self.scenario.update_relationship(agent1.name, agent2.name, change)
