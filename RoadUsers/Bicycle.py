from .MovingAgent import MovingAgent
import random

class Bicycle(MovingAgent):
    def __init__(self, model, space):
        print(f"Bicycle model type: {type(model)}")
        print(f"Bicycle space type: {type(space)}")
        super().__init__(space, model)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self.init_desired_speed(model) 
        

    def step(self):
        # Decision-making logic for bicycles
        self.update_acceleration(self.model)
        self.update_velocity(self.model)
        #print(f"Before Step: Agent position: {self.pos}, Agent velocity: {self.velocity}, Agent acceleration: {self.acceleration}")
        self.position = self.position + self.velocity

    
    def init_desired_speed(self, model): 
        self.desired_speed = 1.2 * random.uniform(0.5, 1.0)


    def agent_portrayal(agent):
        portrayal = {"Filled": "true", "Layer": 0}
        portrayal.update({
                "Shape": "circle",
                "color": "tab:blue",
                "r": 8
            })
        return portrayal

