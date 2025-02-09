import os 
import json 
import pandas as pd
from models import PedestrianBicycleModel 

def run_experiment(params, output_dir): 
    os.makedirs(output_dir, exist_ok=True) 
    # Run the simulation 
    model = PedestrianBicycleModel(**params) 
    for _ in range(100): 
        # Run for 100 steps 
        model.step() 
        # Save results 
        results = model.datacollector.get_model_vars_dataframe() 
        results.to_csv(os.path.join(output_dir, "results.csv")) 
        # Save parameters 
        with open(os.path.join(output_dir, "params.json"), "w") as f:
            json.dump(params, f) 
            # Example usage 
            params = { "width": 20, "height": 20, "num_pedestrians": 10, "num_bicycles": 5 } 
            run_experiment(params, "data/experiment_1")