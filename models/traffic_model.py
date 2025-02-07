from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
import numpy as np

class Pedestrian(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.speed = 1  # Example speed
        self.direction = (1, 0)  # Example direction

    def step(self):
        # Decision-making logic for pedestrians
        new_position = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1]
        )
        # Check if the new position is within grid bounds
        if (0 <= new_position[0] < self.model.grid.width and
            0 <= new_position[1] < self.model.grid.height and
            self.model.grid.is_cell_empty(new_position)):
            self.model.grid.move_agent(self, new_position)

class Bicycle(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.speed = 2  # Example speed
        self.direction = (0, 1)  # Example direction

    def step(self):
        # Decision-making logic for bicycles
        new_position = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1]
        )
        # Check if the new position is within grid bounds
        if (0 <= new_position[0] < self.model.grid.width and
            0 <= new_position[1] < self.model.grid.height and
            self.model.grid.is_cell_empty(new_position)):
            self.model.grid.move_agent(self, new_position)

class PedestrianBicycleModel(Model):
    def __init__(self, width, height, num_pedestrians, num_bicycles):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.num_pedestrians = num_pedestrians
        self.num_bicycles = num_bicycles
        
        # Create pedestrians and bicycles
        pedestrians = Pedestrian.create_agents(model= self, n=num_pedestrians)
        cyclists = Bicycle.create_agents(model=self, n=num_bicycles)

        #generate postiions of bicycles at bottom of grid
        x = self.rng.integers(0, self.grid.width, size = (num_bicycles, ))
        y = np.zeros(shape = (num_bicycles, ), dtype= np.int64)

        #generate postiions of pedestrians at left side of grid
        x = np.zeros(shape = (num_pedestrians, ), dtype= np.int64) 
        y = self.rng.integers(0, self.grid.height, size = (num_bicycles, ))
        
        #place cyclists on grid
        for a, i , j in zip(cyclists, x, y):
            self.grid.place_agent(a, (i,j))

        #place pedestrians on grid
        for a, i , j in zip(pedestrians, x, y):
            self.grid.place_agent(a, (i,j))



    def step(self):
        # Random agent activation order - consider replacign with simultaneous activation, .do("step") then .do("advance")
        self.agents.shuffle_do("step")

def agent_portrayal(agent):
    portrayal = {"Filled": "true", "Layer": 0}
    
    if isinstance(agent, Pedestrian):
        portrayal.update({
            "Shape": "circle",
            "Color": "red",
            "r": 0.5
        })
    elif isinstance(agent, Bicycle):
        portrayal.update({
            "Shape": "circle",
            "Color": "blue",
            "r": 0.8
        })
    return portrayal

def show_steps(model):
    return f"Steps: {model.steps}"



traffic_model = PedestrianBicycleModel(width=200, height=200, num_bicycles=10, num_pedestrians=10)

SpaceGraph = make_space_component(agent_portrayal)
# Corrected step call
for _ in range(10): 
    traffic_model.step()
model_params = {
    "num_bicycles": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of bicycles:",
        "min": 10,
        "max": 100,
        "step": 1,
   },
   "num_pedestrians": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of pedestrians:",
        "min": 10,
        "max": 100,
        "step": 1,
   },
   "width": 10, 
   "height": 10
}
# Visualization setup
page = SolaraViz(
    traffic_model, 
    components = [SpaceGraph], 
    model_params=model_params, 
    name = "Please work"
)
page
