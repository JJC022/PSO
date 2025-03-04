from Optimizer.pso import PSO
from models.PedestrianBicycleModel import PedestrianBicycleModel
model_params = {
    "width": 100,
    "height": 100,
    "num_pedestrians": 10,
    "num_bicycles": 10,
    "num_obstacles": 3
}
dimensions = 2* (model_params["num_pedestrians"] + model_params["num_bicycles"] + model_params["num_obstacles"])
pso = PSO(
    n_particles=30,
    dimensions=dimensions,  
    bounds=(0, 100),  # Assuming positions are within the 100x100 grid
    model_class=PedestrianBicycleModel,
    model_params=model_params,
    steps=100
)

pso.optimize(n_iterations=50)
print("Best position:", pso.global_best_position)
print("Best score:", pso.global_best_score)