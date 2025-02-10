from mesa import Agent
from Movement import SocialForce
import random

class Bicycle(Agent):
    def __init__(self, model):
        super().__init__(model)
        #give cyclist deisred speed and goal of travel
        self.init_desired_speed() 
        self.init_goal
        self.direction = (0, 1)  # Example direction

    def step(self):
        # Decision-making logic for bicycles
        self.update_velocity()
        self.update_speed()
        new_position = (
            self.pos[0] + self.speed[0],
            self.pos[1] + self.speed[1]
        )
        # Check if the new position is within grid bounds
        if (0 <= new_position[0] < self.model.grid.width and
            0 <= new_position[1] < self.model.grid.height and
            self.model.grid.is_cell_empty(new_position)):
            self.model.grid.move_agent(self, new_position)

    def update_velocity(self, model, movement_model="social force"): 
        if movement_model == "social force": 
            self.velocity = SocialForce.calculate_social_force(self, model, self.pos)

    def update_speed(self, model): 
        self._speed += self.velocity
    
    def init_desired_speed(self, model): 
        self._desired_speed = 15 * random.uniform(0.5, 1.0)

    def init_goal(self, model, destination="random"): 
        if destination == "random":
            self.goal = random.choice(range(zip(model.height, model.width)))

    def agent_portrayal(agent):
        portrayal = {"Filled": "true", "Layer": 0}
        portrayal.update({
                "Shape": "circle",
                "color": "tab:blue",
                "r": 0.8
            })
        return portrayal
