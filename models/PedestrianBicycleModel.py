from mesa import Model, DataCollector
from mesa.experimental.continuous_space import ContinuousSpace
import numpy as np
from RoadUsers import Bicycle, Pedestrian, Obstacle, MovingAgent

class PedestrianBicycleModel(Model):
    def __init__(self, width=100, height=100, num_pedestrians=10, num_bicycles=10, num_obstacles=3):
        super().__init__()
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=True,
            random=self.random,
            n_agents= num_bicycles + num_pedestrians + num_obstacles,
        )

        self.collision_count = 0 
        self.near_miss_count = 0
        #initalize datacollector
        self.datacollector = DataCollector(
            model_reporters={"collision_count": "collision_count", 
                             "near_miss_count": "near_miss_count"}, 
            agent_reporters={"position": "position", 
                             "velocity": lambda a: a.velocity if isinstance(a, MovingAgent) else None}
        )
        self.num_pedestrians = num_pedestrians
        self.num_bicycles = num_bicycles
        self.num_obstacles = num_obstacles
        
        
        # Create pedestrians and bicycles
        pedestrians = Pedestrian.create_agents(model=self,space=self.space, n=num_pedestrians)
        cyclists = Bicycle.create_agents(model=self, space=self.space, n=num_bicycles)
        obstacles = Obstacle.Bench.create_agents(model=self, space=self.space, n=num_obstacles)

    def check_collisions(self, radius=5.0): 
        #check every agent in model
        for agent in self.agents: 
            neighbors = agent.get_neighbors_in_radius(radius)

            for neighbor in neighbors: 
                distance = self.space.calculate_distances(self.position, neighbor.position)
                if distance <= (self.size + neighbor.size) and type(neighbor) != Obstacle():
                    self.collision_count += 1
                if distance <= 2*(self.size + neighbor.size) and type(neighbor) != Obstacle():
                    self.near_miss_count += 1

    

    def step(self):
        # Random agent activation order - consider replacign with simultaneous activation, .do("step") then .do("advance")
        print(f"position of first agent: {self.agents[0].pos} velocity of first agent: {self.agents[0].velocity}")
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)



