#!/bin/bash 
# Define the project directory 
PROJECT_DIR="C:\Users\SmotP\Documents\COGS199" 
# Create the main project directory 
mkdir -p $PROJECT_DIR 
# Create subdirectories 
mkdir -p $PROJECT_DIR/data/experiment_1 
mkdir -p $PROJECT_DIR/data/experiment_2 
mkdir -p $PROJECT_DIR/models 
mkdir -p $PROJECT_DIR/experiments 
mkdir -p $PROJECT_DIR/visualization
mkdir -p $PROJECT_DIR/utils

 # Create empty files 
touch $PROJECT_DIR/models/__init__.py 
touch $PROJECT_DIR/models/traffic_model.py 
touch $PROJECT_DIR/models/pso.py 
touch $PROJECT_DIR/experiments/__init__.py 
touch $PROJECT_DIR/experiments/run_experiment.py 
touch $PROJECT_DIR/experiments/parameter_sweep.py 
touch $PROJECT_DIR/visualization/__init__.py 
touch $PROJECT_DIR/visualization/plot_results.py 
touch $PROJECT_DIR/utils/__init__.py 
touch $PROJECT_DIR/utils/helpers.py 
touch $PROJECT_DIR/requirements.txt 
touch $PROJECT_DIR/README.md 
touch $PROJECT_DIR/main.py 

# Print success message 
echo "Project file structure created successfully in the '$PROJECT_DIR' directory."