import numpy as np

def calculate_social_force(agent, other_agents, obstacles, goal, repulsion_strength=2.0, repulsion_range=1.5, anisotropy_weight=0.5, relaxation_time=0.5):
    """ Calculate the instantaneous direction for an agent based on the Social Force Model.

    Parameters:
        agent (object): The agent for which to calculate the force.
        other_agents (list): List of other agents in the environment.
        obstacles (list): List of obstacles in the environment.
        goal (tuple): The goal position of the agent (x, y).
        repulsion_strength (float): Strength of repulsive force from other agents.
        repulsion_range (float): Range of repulsive force from other agents.
        anisotropy_weight (float): Weight for anisotropic behavior (preference for front interactions).
        relaxation_time (float): Relaxation time for driving force.

    Returns:
        np.array: The resultant force vector (direction and magnitude).
    """
    
    # Driving force: Directs the agent toward its goal
    desired_direction = np.array(goal) - np.array(agent.position)
    distance_to_goal = np.linalg.norm(desired_direction)
    
    # Scale the desired speed based on the distance to the goal
    if distance_to_goal == 0:
        desired_velocity = np.array([0.0, 0.0])
    else:
        # Calculate the relative proximity to the goal
        max_distance = np.linalg.norm([agent.model.space.dimensions[0], agent.model.space.dimensions[1]])
        relative_proximity_goal = distance_to_goal / max_distance
        scaled_speed = agent.desired_speed * relative_proximity_goal
        desired_velocity = desired_direction / distance_to_goal * scaled_speed
    
    driving_force = (desired_velocity - np.array(agent.velocity)) / relaxation_time

    # Repulsive force from other agents
    repulsive_force = np.array([0.0, 0.0])
    for other in other_agents:
        if other != agent:
            difference_vector = np.array(agent.position) - np.array(other.position)
            distance_to_other = np.linalg.norm(difference_vector)
            if distance_to_other > 0:
                direction_to_other = difference_vector / distance_to_other
                repulsive_force += repulsion_strength * np.exp(-distance_to_other / repulsion_range) * direction_to_other

    # Repulsive force from obstacles
    for obstacle in obstacles:
        difference_vector = np.array(agent.position) - np.array(obstacle)
        distance_to_obstacle = np.linalg.norm(difference_vector)
        if distance_to_obstacle > 0:
            direction_to_obstacle = difference_vector / distance_to_obstacle
            repulsive_force += repulsion_strength * np.exp(-distance_to_obstacle / repulsion_range) * direction_to_obstacle

    # Total force
    total_force = driving_force + repulsive_force
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