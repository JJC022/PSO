from .MovingAgent import MovingAgent
import random
import numpy as np

class Pedestrian(MovingAgent):
    def __init__(self, model, space):
        print(f"Pedestrian model type: {type(model)}")
        print(f"Pedestrian space type: {type(space)}")
        super().__init__(space ,model)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self.init_desired_speed(model) 
        

    def step(self):
        # Update teh velcoity and accleration, then move the agent for each step
        self.update_velocity(self.model)
        self.update_acceleration(self.model)
        self.position = self.position + self.velocity
        

    #There is potential for moving this to the MovingAgent class
    def init_desired_speed(self, model): 
        self.desired_speed = .7 * random.uniform(0.5, 1.0)


    def agent_portrayal(agent):
        portrayal = {"Filled": "true", "Layer": 0}
        
        portrayal.update({
                "Shape": "circle",
                "color": "tab:red",
                "r": 5
            })
        return portrayal