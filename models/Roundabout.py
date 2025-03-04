from mesa import Agent, Model 
from mesa.space import MultiGrid
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
import numpy as np 

class RoundaboutModel(Model): 
    def __init__(self, width, height, num_agents): 
        self.grid = MultiGrid(width, height, torus=False) 
        self.num_agents = num_agents 

        #Define roundabout center and radius 
        self.roundabout_center = (width // 2, height // 2) 
        self.roundabout_radius = min(width, height) // 3 
        
        # Create agents 
        for i in range(self.num_agents): 
            agent = Pedestrian(i, self) 
            self.grid.place_agent(agent, self.get_entry_point())
            self.schedule.add(agent) 
            
    def get_entry_point(self): 
        """Get a random entry point around the roundabout.""" 
        angle = np.random.uniform(0, 2 * np.pi)
        x = int(self.roundabout_center[0] + self.roundabout_radius * np.cos(angle)) 
        y = int(self.roundabout_center[1] + self.roundabout_radius * np.sin(angle)) 
        return (x, y) 

    def is_on_roundabout(self, pos): 
        """Check if a position is on the roundabout.""" 
        distance = np.linalg.norm(np.array(pos) - np.array(self.roundabout_center)) 
        return distance <= self.roundabout_radius 

    def step(self): 
        self.schedule.step()

class Pedestrian(Agent): 
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model) 
        self.pos = model.get_entry_point() 
        self.velocity = np.array([0.0, 0.0]) 
        self.desired_speed = 1.0 
        self.goal = self.generate_exit_point() 
    def generate_exit_point(self):
        """Generate a random exit point around the roundabout.""" 
        angle = np.random.uniform(0, 2 * np.pi) 
        x = int(self.model.roundabout_center[0] + self.model.roundabout_radius * np.cos(angle)) 
        y = int(self.model.roundabout_center[1] + self.model.roundabout_radius * np.sin(angle)) 
        return (x, y) 
    def step(self): 
        # Calculate direction toward the goal 
        direction = np.array(self.goal) - np.array(self.pos) 
        direction = direction / np.linalg.norm(direction) 
        # Update velocity and position 
        self.velocity = direction * self.desired_speed 
        new_position = tuple(np.array(self.pos) + self.velocity) 
        # Move to new position if it's valid 
        if self.model.grid.is_cell_empty(new_position): 
            self.model.grid.move_agent(self, new_position) 
        # Check if the agent has reached its goal 
        if np.linalg.norm(np.array(self.pos) - np.array(self.goal)) < 1.0: 
            self.model.grid.remove_agent(self) 
            self.model.schedule.remove(self)

    def agent_portrayal(agent): 
        portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0, "Color": "red", "r": 0.5} 
        return portrayal 
