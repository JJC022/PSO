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
    desired_direction = np.array(goal) - np.array(agent.pos)
    desired_velocity = desired_direction / np.linalg.norm(desired_direction) * agent.desired_speed
    driving_force = (desired_velocity - np.array(agent.velocity)) / tau

    # Repulsive force from other agents
    repulsive_force = np.array([0.0, 0.0])
    for other in other_agents:
        if other != agent:
            diff = np.array(agent.pos) - np.array(other.pos)
            distance = np.linalg.norm(diff)
            if distance > 0:
                direction = diff / distance
                # Anisotropic term (preference for front interactions)
                theta = np.arccos(np.dot(agent.velocity / np.linalg.norm(agent.velocity), direction))
                anisotropic_factor = lambda_ + (1 - lambda_) * (1 + np.cos(theta)) / 2
                repulsive_force += A * np.exp(-distance / B) * direction * anisotropic_factor

    # Repulsive force from obstacles
    for obstacle in obstacles:
        diff = np.array(agent.pos) - np.array(obstacle)
        distance = np.linalg.norm(diff)
        if distance > 0:
            direction = diff / distance
            repulsive_force += A * np.exp(-distance / B) * direction

    # Total force
    total_force = driving_force + repulsive_force
    return total_force