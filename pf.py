""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np
import scipy.stats

from utils import minimized_angle


class ParticleFilter:
    def __init__(self, mean, cov, num_particles, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.num_particles = num_particles
        self.reset()
        

    def reset(self):
        self.particles = np.zeros((self.num_particles, 3))
        for i in range(self.num_particles):
            self.particles[i, :] = np.random.multivariate_normal(
                self._init_mean.ravel(), self._init_cov)
        self.weights = np.ones(self.num_particles) / self.num_particles

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        # Implementation of Partcile Filter following the explanations from Probabilistic Robotics
        # new_particles, new_weights = self.particles, self.weights
        new_particles = np.zeros((self.num_particles, 3))
        new_weights = np.ones(self.num_particles) / self.num_particles
        for j in range(self.num_particles):
            new_particles[j, :] = self.particles[j, :]
            new_weights[j] = self.weights[j]
            
        for m in range(0,self.num_particles):
            u_noisy = env.sample_noisy_action(u)
            #print(u_noisy)
            # new_particles[m,:] = self.particles[m,:] + np.array([u_noisy[1,0]*np.cos(self.particles[m,2]+u_noisy[0,0]),
            #                                                      u_noisy[1,0]*np.sin(self.particles[m,2]+u_noisy[0,0]),
            #                                                      u_noisy[0,0]+u_noisy[2,0]])
            new_particles[m,:] = env.forward(self.particles[m,:], u_noisy).reshape((3,))
            # Observation we would make if x is the real state and we had no observation noise:
            z_est = env.observe(new_particles[m,:], marker_id)
            new_weights[m] = env.likelihood(z_est-z, self.beta)
        # print(min(new_weights), max(new_weights))
        # print("new: \n", new_weights)
        # print("self: \n", self.weights)
        new_weights = new_weights / np.sum(new_weights)
        # print("new - weighted: \n", new_weights)

        # self.particles, self.weights = self.resample(new_particles, new_weights)
        new_particles, new_weights = self.resample(new_particles, new_weights)
        # print("new-new: \n", new_weights)

        # mean, cov = self.mean_and_variance(self.particles)
        mean, cov = self.mean_and_variance(new_particles)

        self.particles = new_particles
        self.weights = new_weights
        return mean, cov

    def resample(self, particles, weights):
        """Sample new particles and weights given current particles and weights. Be sure
        to use the low-variance sampler from class.

        particles: (n x 3) matrix of poses
        weights: (n,) array of weights
        """
        new_particles = np.zeros((self.num_particles, 3))
        new_weights = np.ones(self.num_particles) / self.num_particles
        for j in range(self.num_particles):
            new_particles[j, :] = particles[j, :]
            new_weights[j] = weights[j]
        
        # Implementation of the Low-Variance Resampling from Table 4.4 of Probabilistic Robotics
        r = np.random.uniform(0,1/self.num_particles)
        c = weights[0]
        i = 0

        for m in range(0,self.num_particles):
            U = r + m /self.num_particles
            while U > c:
                i += 1
                c = c + weights[i]
            new_particles[m,:] = particles[i, :]
            new_weights[m] = weights[i] # DUDA: por qué?
        new_weights = new_weights / np.sum(new_weights)
        
        return new_particles, new_weights

    def mean_and_variance(self, particles):
        """Compute the mean and covariance matrix for a set of equally-weighted
        particles.

        particles: (n x 3) matrix of poses
        """
        mean = particles.mean(axis=0)
        mean[2] = np.arctan2(
            np.cos(particles[:, 2]).sum(),
            np.sin(particles[:, 2]).sum()
        )

        zero_mean = particles - mean
        for i in range(zero_mean.shape[0]):
            zero_mean[i, 2] = minimized_angle(zero_mean[i, 2])
        cov = np.dot(zero_mean.T, zero_mean) / self.num_particles

        return mean.reshape((-1, 1)), cov
