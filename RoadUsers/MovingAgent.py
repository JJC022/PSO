from mesa.experimental.continuous_space import ContinuousSpaceAgent
from mesa import Agent
import numpy as np
import random
from Movement import SocialForce

"""
1. Should this be an abstract class? How would that interact with the inheritance setup? This question was motivated by the idea of trying 
to set a differential max speed. I think that delving into the question of how the class hierarchy is going to work and interact with the different 
movement parameters is really important before adding all those attributes and methods 

"""

class MovingAgent(ContinuousSpaceAgent):
    def __init__(self, space, model, logic=None, placement=None):
        super().__init__(space, model)
        # Model parameters 
        self.model = model
        self.space = space

        #Movement Parameters 
        self._goal = self.init_goal(model)
        self.position = self.init_position(model=model, logic=logic, placement=placement)
        self.max_speed = self.init_max_speed()
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

        #np.random.seed(0) when I uncomment this line of code they all spawn in the same spot 

        goal_x = np.random.uniform(x_min, x_max)
        goal_y = np.random.uniform(y_min, y_max)

        return (goal_x, goal_y)
    
    def init_max_speed(self):
        return 20
            
    def update_acceleration(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.acceleration = SocialForce.calculate_social_force(agent=self, other_agents= model.agents, obstacles=[0, 0], goal= self._goal)

    def update_velocity(self, model): 
        self.velocity += self.acceleration
    
    def remove(self): 
        ContinuousSpaceAgent.remove(self)
    

    def agent_portrayal(self, model): 
        pass