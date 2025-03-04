from mesa.experimental.continuous_space import ContinuousSpaceAgent
from mesa import Agent
import numpy as np
import random
from Movement import SocialForce

class MovingAgent(ContinuousSpaceAgent):
    def __init__(self, space, model, logic=None, placement=None):
        super().__init__(space, model)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self._goal = self.init_goal(model)
        print(f"MovingAgent {self.unique_id} initialized with goal: {self._goal}")
        self.position = self.init_position(model=model, logic=logic, placement=placement)
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        

    def init_position(self, model, logic="random", placement=None):
        if logic == "random": 
            return (np.random.uniform(model.space.x_min, model.space.x_max), np.random.uniform(model.space.y_min, model.space.y_max))
        if logic == "placed":
            if placement is not None:
                self.position = placement
            else:
                raise ValueError("must provide specific_location when placement == 'specific'")
        else: 
            raise ValueError(f"Invalid logic provided. Must be 'random' or 'placed'. Received{logic}")
    

    def init_goal(self, model, destination="random"): 
        #if destination == "random":
        x_min, x_max = model.space.x_min, model.space.x_max
        y_min, y_max = model.space.y_min, model.space.y_max

        np.random.seed(0)

        goal_x = np.random.uniform(x_min, x_max)
        goal_y = np.random.uniform(y_min, y_max)

        return (goal_x, goal_y)
        print(f"MovingAgent {self.unique_id} initialized with goal: {self._goal}")
            
    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    
    def remove(self): 
        ContinuousSpaceAgent.remove(self)
    

    def agent_portrayal(self, model): 
        pass