import numpy as np 

class PSO: 
    def __init__(self, n_particles, dimensions, bounds, model_class, model_params): 
        self.n_particles = n_particles 
        self.dimensions = dimensions 
        self.bounds = bounds 
        self.model_class = model_class 
        self.model_params = model_params 
        # Initialize particles and velocities 
        self.particles = np.random.uniform(bounds[0], bounds[1], (n_particles, dimensions)) 
        self.velocities = np.random.uniform(-1, 1, (n_particles, dimensions)) 
        self.best_positions = self.particles.copy() 
        self.best_scores = np.array([self.fitness(p) for p in self.particles])
        self.global_best_position = self.best_positions[np.argmin(self.best_scores)] 
        self.global_best_score = np.min(self.best_scores) 
    def fitness(self, particle): 
        # Use the particle to configure the map (e.g., adjust lanes or obstacles) 
        # # Run the simulation and return the number of collisions 
        model = self.model_class(**self.model_params) 
        for _ in range(10): 
            # Run for 10 steps 
            model.step() 
            return model.count_collisions() 
    def optimize(self, n_iterations): 
        for _ in range(n_iterations): 
            for i in range(self.n_particles): 
                # Update velocity and position 
                r1, r2 = np.random.rand(2) 
                self.velocities[i] = ( 0.5 * self.velocities[i] + 2.0 * r1 * (self.best_positions[i] - self.particles[i]) + 2.0 * r2 * (self.global_best_position - self.particles[i]) ) 
                self.particles[i] += self.velocities[i] 
                # Enforce bounds 
                self.particles[i] = np.clip(self.particles[i], self.bounds[0], self.bounds[1]) 
                # Evaluate fitness 
                score = self.fitness(self.particles[i]) 
                if score < self.best_scores[i]: 
                    self.best_positions[i] = self.particles[i] 
                    self.best_scores[i] = score 
                    if score < self.global_best_score: 
                        self.global_best_position = self.particles[i] 
                        self.global_best_score = score