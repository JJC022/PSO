from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from models import PedestrianBicycleModel
from RoadUsers import Pedestrian, Bicycle

model_params = {
    "width": 100, 
   "height": 100,
   "num_pedestrians": 10, 
   "num_bicycles": 10  
    
}

traffic_model = PedestrianBicycleModel.PedestrianBicycleModel(width=100, height=100, num_bicycles=10, num_pedestrians=10)
def traffic_model_portrayal(agent):
    if agent is None: 
        return 
    if isinstance(agent, Pedestrian): 
        portrayal = Pedestrian.agent_portrayal(agent)
    if isinstance(agent, Bicycle): 
        portrayal = Bicycle.agent_portrayal(agent)

    return portrayal

SpaceGraph = make_space_component(traffic_model_portrayal)
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
}
"""
if __name__ == "__main__":
    model = PedestrianBicycleModel.PedestrianBicycleModel(width=100, height=100, num_pedestrians=10, num_bicycles=10)
    for _ in range(10):
        model.step()
        print(f"position of first agent: {model.agents[0].pos} velocity of first agent: {model.agents[0].velocity}")


