from mesa.experimental.continuous_space import ContinuousSpaceAgent
from mesa import Agent
import numpy as np
import random
from Movement import SocialForce

class MovingAgent(ContinuousSpaceAgent):
    def __init__(self, model, space):
        super().__init__(space, model)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self.position = self.init_position()
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.init_goal(self, model)

    def init_position(self, model, logic="random"):
        if logic == "random": 
            np.random.randint(0, model.space.x_max), np.random.randint(0, model.space.y_max) 

    def init_goal(self, model, destination="random"): 
        if destination == "random":
            self._goal = self._goal = (random.uniform(0, model.space.dimensions[0]), 
              random.randint(0, random.uniform.space.dimensions[1]))
            
    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    

    def agent_portrayal(self, model): 
        pass