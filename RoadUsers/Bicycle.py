from mesa import Agent
from Movement import SocialForce
import random
import numpy as np

class Bicycle(Agent):
    def __init__(self, model):
        super().__init__(model)
        #give cyclist desired speed and goal of travel
        self._goal = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.init_goal(self, model)
        self.init_desired_speed(model) 
        

    def step(self):
        # Decision-making logic for bicycles
        self.update_velocity(self.model)
        self.update_acceleration(self.model)
        new_position = (
            int(self.pos[0] + self.velocity[0]),
            int(self.pos[1] + self.velocity[1])
        )
        # Check if the new position is within grid bounds
        if (0 <= new_position[0] < self.model.grid.width and
            0 <= new_position[1] < self.model.grid.height and
            self.model.grid.is_cell_empty(new_position)):
            self.model.grid.move_agent(self, new_position)

    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    
    def init_desired_speed(self, model): 
        self.desired_speed = 15 * random.uniform(0.5, 1.0)

    def init_goal(self, model, destination="random"): 
        if destination == "random":
            self._goal = (random.randint(0, model.grid.height - 1), 
              random.randint(0, model.grid.width - 1))

    def agent_portrayal(agent):
        portrayal = {"Filled": "true", "Layer": 0}
        portrayal.update({
                "Shape": "circle",
                "color": "tab:blue",
                "r": 0.8
            })
        return portrayal
