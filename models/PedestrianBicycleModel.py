from mesa import Agent, Model, DataCollector
from mesa.experimental.continuous_space import ContinuousSpace
import numpy as np
from RoadUsers import Bicycle, Pedestrian

class PedestrianBicycleModel(Model):
    def __init__(self, width=100, height=100, num_pedestrians=10, num_bicycles=10):
        super().__init__()
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=True,
            random=self.random,
            n_agents= num_bicycles + num_pedestrians,
        )


        #self.space.add_property_layer(property_layer=PropertyLayer(name = "obstacles", width=width, height=height, default_value=0))

        #initalize datacollector
        self.datacollector = DataCollector(
            model_reporters={"mean velocity": lambda m: m.agents.agg("velocity", np.mean)}, 
            agent_reporters={"position": "pos"}
        )
        self.num_pedestrians = num_pedestrians
        self.num_bicycles = num_bicycles
        
        # Create pedestrians and bicycles
        pedestrians = Pedestrian.create_agents(model= self, n=num_pedestrians, space= self.space)
        cyclists = Bicycle.create_agents(model=self, n=num_bicycles, space= self.space)

    

    def step(self):
        # Random agent activation order - consider replacign with simultaneous activation, .do("step") then .do("advance")
        print(f"position of first agent: {self.agents[0].pos} velocity of first agent: {self.agents[0].velocity}")
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)



