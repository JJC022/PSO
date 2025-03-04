from .MovingAgent import MovingAgent
import random

class Bicycle(MovingAgent):
    def __init__(self, model, space, logic='random', placement=None, index=None):
        super().__init__(space, model,logic, placement)
        self.model = model
        self.space = space
        #give cyclist desired speed and goal of travel
        self.init_goal(model)
        self.init_desired_speed() 
        

    def step(self):
        # Decision-making logic for bicycles
        self.update_acceleration(self.model)
        self.update_velocity(self.model)
        #print(f"Before Step: Agent position: {self.pos}, Agent velocity: {self.velocity}, Agent acceleration: {self.acceleration}")
        self.position = self.position + self.velocity

    
    def init_desired_speed(self): 
        self.desired_speed = 1.2 * random.uniform(0.5, 1.0)


    def agent_portrayal(agent):
        portrayal = {
                "Shape": "circle",
                "color": "tab:blue",
                "size": 8
            }
        return portrayal

