from mesa import Agent, Model, DataCollector
from mesa.space import MultiGrid, PropertyLayer
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
import numpy as np
from SocialForce import calculate_social_force
from RoadUsers import Bicycle, Pedestrian

class PedestrianBicycleModel(Model):
    def __init__(self, width, height, num_pedestrians, num_bicycles):
        super().__init__()
        self.grid = MultiGrid(width, height, True)

        self.grid.add_property_layer(property_layer=PropertyLayer(name = "obstacles", width=width, height=height))

        #initalize datacollector
        self.datacollector = DataCollector(
            model_reporters={"mean speed": lambda m: m.agents.agg("speed", np.mean)}, 
            agent_reporters={"position": "pos"}
        )
        self.num_pedestrians = num_pedestrians
        self.num_bicycles = num_bicycles
        
        # Create pedestrians and bicycles
        pedestrians = Pedestrian.create_agents(model= self, n=num_pedestrians)
        cyclists = Bicycle.create_agents(model=self, n=num_bicycles)

        #generate postiions of bicycles at bottom of grid
        x = self.rng.integers(0, self.grid.width, size = (num_bicycles, ))
        y = np.zeros(shape = (num_bicycles, ), dtype= np.int64)

        #place cyclists on grid
        for a, i, j in zip(cyclists, x, y):
            self.grid.place_agent(a, (i,j))

        #generate postiions of pedestrians at left side of grid
        x = np.zeros(shape = (num_pedestrians, ), dtype= np.int64) 
        y = self.rng.integers(0, self.grid.height, size = (num_bicycles, ))

        #place pedestrians on grid
        for a, i , j in zip(pedestrians, x, y):
            self.grid.place_agent(a, (i,j))

    def step(self):
        # Random agent activation order - consider replacign with simultaneous activation, .do("step") then .do("advance")
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)


model_params = {
    "width": 10, 
   "height": 10,
   "num_pedestrians": 10, 
   "num_bicycles": 10  
    
}

traffic_model = PedestrianBicycleModel(width=10, height=10, num_bicycles=10, num_pedestrians=10)
SpaceGraph = make_space_component(Pedestrian.agent_portrayal)
# Visualization setup
page = SolaraViz(
    traffic_model, 
    components = [SpaceGraph], 
    model_params=model_params, 
    name = "Please work"
)
page



"""
"width": {
        "type": "SliderInt",
        "value": 50,
        "label": "Width",
        "min": 5,
        "max": 60,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 50,
        "label": "Height",
        "min": 5,
        "max": 60,
        "step": 1,
    },
   "num_bicycles": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of bicycles:",
        "min": 1,
        "max": 20,
        "step": 1,
   },
   "num_pedestrians": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of pedestrians:",
        "min": 1,
        "max": 20,
        "step": 1,
   }

"""
