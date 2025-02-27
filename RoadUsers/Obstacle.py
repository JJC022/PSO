from mesa.experimental.continuous_space import ContinuousSpaceAgent
import numpy as np

class Bench(ContinuousSpaceAgent): 
    def __init__(self, model, space): 
        super().__init__(space, model)
        self.space = space
        self.init_size
        self.init_location

        self.position = np.random.randint(0, model.space.x_max), np.random.randint(0, model.space.y_max)
    
    def init_size(self):
        self.length = np.random.randint(5, 15)
        self.width = np.random.randint(2, 6)


    def init_location(self, placement="random", specific_location=None): 
        if placement == "random":
            self.location = [np.random.randint(0, self.model.space.dimensions[0]), np.randint(0, self.model.space.dimensions[1])]

        if placement == "specific":
            if specific_location is not None: 
                self.location = specific_location
            else: 
                raise ValueError("must provide specific_location when placement == 'specific'")
            
    def agent_portrayal(self):
        portrayal = {
                "Shape": "rectangle",
                "color": "tab:green",
                "size": 5
            }
        
        return portrayal


