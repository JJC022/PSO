from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from models import PedestrianBicycleModel
from RoadUsers import Pedestrian, Bicycle

model_params = {
    "width": 10, 
   "height": 10,
   "num_pedestrians": 10, 
   "num_bicycles": 10  
    
}

traffic_model = PedestrianBicycleModel(width=10, height=10, num_bicycles=10, num_pedestrians=10)
SpaceGraph = make_space_component((Pedestrian.agent_portrayal, Bicycle.agent_portrayal))
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