from mesa import Model, DataCollector, Agent
from mesa.experimental.continuous_space import ContinuousSpace
import numpy as np
from RoadUsers import Bicycle, Pedestrian, Obstacle, MovingAgent

class PedestrianBicycleModel(Model):
    def __init__(self, width=100, height=100, num_pedestrians=10, num_bicycles=10, num_obstacles=3, logic="random", placement=None):
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

        self.n_agents = self.num_pedestrians + self.num_bicycles + self.num_obstacles
        
       # Create pedestrians
        pedestrians = Pedestrian.create_agents(model=self, n=num_pedestrians, space=self.space, logic=logic or "random", placement=placement)

        # Create cyclists
        cyclists = Bicycle.create_agents(model=self, n=num_bicycles, space=self.space, logic=logic or "random", placement=placement)

        # Create obstacles
        obstacles = Obstacle.Bench.create_agents(model=self, n=num_obstacles, space=self.space, logic=logic or "random", placement=placement)

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
        # Random agent activation order - consider replacing with simultaneous activation, .do("step") then .do("advance")
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

    def set_environment(self, particle):
        """
        Set the environment based on the particle's parameters.
        Assume particle contains positions for obstacles and agents.
        """

        for agent in list(self.agents):
            agent.remove()       
        # Set new positions for obstacles and agents based on particle
        # Example: particle[0:num_obstacles] for obstacle positions
        #          particle[num_obstacles:] for agent positions
        obstacle_positions = particle[:self.num_obstacles]
        pedestrian_positions = particle[self.num_obstacles: self.num_obstacles + self.num_pedestrians]
        bicycle_positions = particle[len(particle) - self.num_bicycles: ]
        
        for pos in obstacle_positions:
            obstacle = Obstacle.Bench(self, self.space)
            obstacle.init_position("placed", placement=pos)
        
        for pos in pedestrian_positions:
            pedestrian = Pedestrian(self, self.space) 
            pedestrian.init_position(model=pedestrian.model, logic="placed", placement=pos)
        for pos in bicycle_positions: 
            bicycle = Bicycle(self, self.space)
            bicycle.init_position(model=bicycle.model, logic="placed", placement=pos)
        

    def count_collisions(self):
        """
        Count the number of collisions in the current step.
        """
        return self.collision_count

    def count_near_misses(self):
        """
        Count the number of near misses in the current step.
        """
        return self.near_miss_count




