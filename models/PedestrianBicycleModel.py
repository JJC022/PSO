from mesa import Agent, Model, DataCollector
from mesa.space import MultiGrid, PropertyLayer
import numpy as np
from RoadUsers import Bicycle, Pedestrian

class PedestrianBicycleModel(Model):
    def __init__(self, width=10, height=10, num_pedestrians=10, num_bicycles=10):
        super().__init__()
        self.grid = MultiGrid(width, height, True)

        #self.grid.add_property_layer(property_layer=PropertyLayer(name = "obstacles", width=width, height=height, default_value=0))

        #initalize datacollector
        self.datacollector = DataCollector(
            model_reporters={"mean velocity": lambda m: m.agents.agg("velocity", np.mean)}, 
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
        print(f"position of first agent: {self.agents[0].pos} velocity of first agent: {self.agents[0].velocity}")
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)



