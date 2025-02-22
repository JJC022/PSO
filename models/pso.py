import numpy as np

class PSO:
    def __init__(self, n_particles, dimensions, bounds, model_class, model_params, steps=10):
        """
        Particle Swarm Optimization (PSO) for optimizing obstacle and path placement 
        in a pedestrian and bicycle movement model to minimize collisions and near misses.

        Parameters:
        - n_particles: int -> Number of particles (solutions)
        - dimensions: int -> Number of parameters to optimize
        - bounds: tuple -> (lower_bound, upper_bound) for each dimension
        - model_class: class -> The agent-based model class
        - model_params: dict -> Parameters to initialize the model
        - steps: int -> Number of simulation steps per fitness evaluation
        """
        self.n_particles = n_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.model_class = model_class
        self.model_params = model_params
        self.steps = steps  # Number of steps to run the model per evaluation

        # Initialize particles (candidate solutions) and their velocities
        self.particles = np.random.uniform(bounds[0], bounds[1], (n_particles, dimensions))
        self.velocities = np.random.uniform(-1, 1, (n_particles, dimensions))

        # Personal best positions and scores
        self.best_positions = self.particles.copy()
        self.best_scores = np.array([self.fitness(p) for p in self.particles])

        # Global best position (across all particles)
        best_idx = np.argmin(self.best_scores)
        self.global_best_position = self.best_positions[best_idx]
        self.global_best_score = self.best_scores[best_idx]

    def fitness(self, particle):
        """
        Evaluates the fitness of a given particle by running the model 
        and measuring the number of collisions and near misses.

        Lower fitness score is better (fewer collisions/near misses).
        """
        # Configure the model with the particle's parameters (e.g., obstacle placement)
        model = self.model_class(**self.model_params)
        model.set_environment(particle)  # Assume model has a method to apply changes

        total_collisions = 0
        total_near_misses = 0

        for _ in range(self.steps):
            model.step()
            total_collisions += model.count_collisions()
            total_near_misses += model.count_near_misses()

        # Weighted fitness score (adjust weights as needed)
        fitness_score = total_collisions + (0.5 * total_near_misses)
        return fitness_score

    def optimize(self, n_iterations, inertia=0.5, cognitive_weight=2.0, social_weight=2.0):
        """
        Runs the PSO algorithm to optimize obstacle/path placement.
        
        Parameters:
        - n_iterations: int -> Number of iterations to update particle positions
        - inertia: float -> Influence of previous velocity (momentum)
        - cognitive_weight: float -> Attraction to a particle's own best position
        - social_weight: float -> Attraction to the global best position
        """
        for _ in range(n_iterations):
            for i in range(self.n_particles):
                # Generate random coefficients
                r1, r2 = np.random.rand(2)

                # Update velocity using the PSO formula
                self.velocities[i] = (
                    inertia * self.velocities[i] +  # Maintain momentum
                    cognitive_weight * r1 * (self.best_positions[i] - self.particles[i]) +  # Personal best
                    social_weight * r2 * (self.global_best_position - self.particles[i])   # Global best
                )

                # Update particle position
                self.particles[i] += self.velocities[i]

                # Ensure particles stay within bounds
                self.particles[i] = np.clip(self.particles[i], self.bounds[0], self.bounds[1])

                # Evaluate fitness
                score = self.fitness(self.particles[i])

                # Update personal best
                if score < self.best_scores[i]:
                    self.best_positions[i] = self.particles[i]
                    self.best_scores[i] = score

                    # Update global best
                    if score < self.global_best_score:
                        self.global_best_position = self.particles[i]
                        self.global_best_score = score
