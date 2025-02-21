import numpy as np

def calculate_social_force(agent, other_agents, obstacles, goal, A=2.0, B=1.5, lambda_=0.5, tau=0.5):
    """ Calculate the instantaneous direction for an agent based on the Social Force Model.

    Parameters:
        agent (object): The agent for which to calculate the force.
        other_agents (list): List of other agents in the environment.
        obstacles (list): List of obstacles in the environment.
        goal (tuple): The goal position of the agent (x, y).
        A (float): Strength of repulsive force from other agents.
        B (float): Range of repulsive force from other agents.
        lambda_ (float): Weight for anisotropic behavior (preference for front interactions).
        tau (float): Relaxation time for driving force.

    Returns:
        np.array: The resultant force vector (direction and magnitude).
    """
    
    # Driving force: Directs the agent toward its goal
    desired_direction = np.array(goal) - np.array(agent.position)
    #print(f"Desired direction: {desired_direction}")
    norm_desired_direction = np.linalg.norm(desired_direction)
    if norm_desired_direction == 0:
        desired_velocity = np.array([0.0, 0.0])
    else:
        desired_velocity = desired_direction / norm_desired_direction * agent.desired_speed
    driving_force = (desired_velocity - np.array(agent.velocity)) / tau
    #print(f"Driving force: {driving_force}")

    # Repulsive force from other agents
    repulsive_force = np.array([0.0, 0.0])
    for other in other_agents:
        if other != agent:
            diff = np.array(agent.position) - np.array(other.position)
            distance = np.linalg.norm(diff)
            if distance > 0:
                direction = diff / distance
                repulsive_force += A * np.exp(-distance / B) * direction

    # Repulsive force from obstacles
    for obstacle in obstacles:
        diff = np.array(agent.position) - np.array(obstacle)
        distance = np.linalg.norm(diff)
        if distance > 0:
            direction = diff / distance
            repulsive_force += A * np.exp(-distance / B) * direction

    # Total force
    total_force = driving_force + repulsive_force
    #print(f"SocialForce:{total_force}")
    return total_force

if __name__ == "__main__":
    # Example test case
    class Agent:
        def __init__(self, position, velocity, desired_speed):
            self.position = position
            self.velocity = velocity
            self.desired_speed = desired_speed

    agent = Agent(position=[0, 0], velocity=[1, 1], desired_speed=1.0)
    other_agents = [Agent(position=[1, 1], velocity=[0, 0], desired_speed=1.0)]
    obstacles = [[2, 2]]
    goal = [5, 5]

    force = calculate_social_force(agent, other_agents, obstacles, goal)
    print("Calculated force:", force)