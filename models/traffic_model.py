from mesa import Agent, Model 
from mesa.space import MultiGrid 
from mesa.time import RandomActivation
from mesa.visualization import CanvasGrid, ModularServer 


class Pedestrian(Agent): 
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model) 
        self.speed = 1 # Example speed 
        self.direction = (1, 0) # Example direction 
    def step(self): 
        # Decision-making logic for pedestrians 
        new_position = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]) 
        if self.model.grid.is_cell_empty(new_position): 
            self.model.grid.move_agent(self, new_position) 
class Bicycle(Agent): 
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model) 
        self.speed = 2 # Example speed
        self.direction = (0, 1) # Example direction 

    def step(self):   
            # Decision-making logic for bicycles 
        new_position = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]) 
        if self.model.grid.is_cell_empty(new_position): 
            self.model.grid.move_agent(self, new_position) 
class PedestrianBicycleModel(Model): 
    def __init__(self, width, height, num_pedestrians, num_bicycles): 
        self.grid = MultiGrid(width, height, True) 
        self.schedule = RandomActivation(self) 
        
        # Create pedestrians 
        for i in range(num_pedestrians): 
            pedestrian = Pedestrian(i, self) 
            self.grid.place_agent(pedestrian, (0, i)) 
            self.schedule.add(pedestrian) 
            
            # Create bicycles 
        for i in range(num_bicycles): 
            bicycle = Bicycle(i + num_pedestrians, self) 
            self.grid.place_agent(bicycle, (i, 0)) 
            self.schedule.add(bicycle)

        def step(self): 
            self.schedule.step() 


        def agent_portrayal(agent): 
            portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0} 
            if isinstance(agent, Pedestrian): 
                portrayal["Color"] = "red" 
                portrayal["r"] = 0.5 
            elif isinstance(agent, Bicycle): 
                portrayal["Color"] = "blue" 
                portrayal["r"] = 0.8 
                return portrayal 
            grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500) 
            server = ModularServer(PedestrianBicycleModel, [grid], "Pedestrian-Bicycle Model", 10, 10, 5, 5) 
            server.launch()
