from mesa.experimental.continuous_space import ContinuousSpaceAgent
from Movement import SocialForce
import random
import numpy as np

class Bicycle(ContinuousSpaceAgent):
    def __init__(self, model, space):
        super().__init__(space, model)
        self.space = space
        #give cyclist desired speed and goal of travel
        self.position = np.random.randint(0, model.space.x_max), np.random.randint(0, model.space.y_max) 
        self._goal = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.init_goal(self, model)
        self.init_desired_speed(model) 
        

    def step(self):
        # Decision-making logic for bicycles
        self.update_acceleration(self.model)
        self.update_velocity(self.model)
        #print(f"Before Step: Agent position: {self.pos}, Agent velocity: {self.velocity}, Agent acceleration: {self.acceleration}")
        self.position = self.position + self.velocity

    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    
    def init_desired_speed(self, model): 
        self.desired_speed = 1.2 * random.uniform(0.5, 1.0)

    def init_goal(self, model, destination="random"): 
        if destination == "random":
            self._goal = self._goal = (random.uniform(0, model.space.dimensions[0]), 
              random.randint(0, random.uniform.space.dimensions[1]))

    def agent_portrayal(agent):
        portrayal = {"Filled": "true", "Layer": 0}
        portrayal.update({
                "Shape": "circle",
                "color": "tab:blue",
                "r": 0.8
            })
        return portrayal

