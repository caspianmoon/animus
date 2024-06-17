# animus/utils.py

def visualize_scenario(scenario):
    print(f"Scenario: {scenario.description}")
    print(f"Context: {scenario.context}")
    print(f"Environment: {scenario.environment}")
    print(f"Relationships: {scenario.relationships}")
    for event in scenario.get_events():
        print(f"Event: {event}")
    print("\n")


def analyze_interactions(agents):
    for agent in agents:
        print(f"{agent.name} ({agent.role}) is in state {agent.state}")
