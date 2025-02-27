from mesa.experimental.continuous_space import ContinuousSpaceAgent
from mesa import Agent
import numpy as np
import random
from Movement import SocialForce

class MovingAgent(ContinuousSpaceAgent):
    def __init__(self, space, model):
        print(f"Received by MovingAgent. Space: {self.space} Model: {self.model}")
        super().__init__(space, model)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self.position = self.init_position(model=model)
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.init_goal(self, model)

    def init_position(self, model, logic="random"):
        if logic == "random": 
            return (np.random.uniform(model.space.x_min, model.space.x_max), np.random.uniform(model.space.y_min, model.space.y_max))

    def init_goal(self, model, destination="random"): 
        if destination == "random":
            x_min, x_max = model.space.x_min, model.space.x_max
            y_min, y_max = model.space.y_min, model.space.y_max

            goal_x = np.random.uniform(x_min, x_max)
            goal_y = np.random.uniform(y_min, y_max)

            self._goal = (goal_x, goal_y)
            
    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    

    def agent_portrayal(self, model): 
        pass