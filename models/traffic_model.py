from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.visualization import SolaraViz, make_space_component, make_plot_component

class Pedestrian(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
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
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
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
        self.agents = []  # Store all agents here instead of using scheduler
        
        # Create pedestrians
        for i in range(num_pedestrians):
            pedestrian = Pedestrian(i, self)
            self.agents.append(pedestrian)
            self.grid.place_agent(pedestrian, (0, i % height))
        
        # Create bicycles
        for i in range(num_bicycles):
            bicycle = Bicycle(i + num_pedestrians, self)
            self.agents.append(bicycle)
            self.grid.place_agent(bicycle, (i % width, 0))

    def step(self):
        # Randomize agent activation order
        self.random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()

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


if __name__ == "__main__":
    model = PedestrianBicycleModel(width=200, height=200, num_bicycles=10, num_pedestrians=10)
    for _ in range(10): 
        model.step