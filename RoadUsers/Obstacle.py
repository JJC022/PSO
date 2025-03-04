from mesa.experimental.continuous_space import ContinuousSpaceAgent
import numpy as np

class Bench(ContinuousSpaceAgent): 
    def __init__(self, model, space, logic='random', placement=None, index=None):
        super().__init__(space, model)
        self.space = space
        self.model = model
        self.init_size()
        self.position = self.init_position()
    
    def init_size(self):
        self.length = np.random.randint(5, 15)
        self.width = np.random.randint(2, 6)


    def init_position(self, logic="random", placement=None): 
        """
        Should I change this to be the same as the one for MovingAgent? 
        """
        x_min, x_max = self.model.space.x_min, self.model.space.x_max
        y_min, y_max = self.model.space.y_min, self.model.space.y_max
        if logic == "random":
            return[np.random.randint(x_min, x_max), np.random.randint(y_min, y_max)]

        if logic == "placed":
            if placement is not None: 
                return placement
            else: 
                raise ValueError("must provide specific_location when placement == 'specific'")
            
    def remove(self): 
        super().remove()
            
    def agent_portrayal(self):
        portrayal = {
                "marker": "s",
                "color": "tab:green",
                "size": 5
            }
        
        return portrayal


