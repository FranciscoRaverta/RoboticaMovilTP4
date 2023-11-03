""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np

from utils import minimized_angle


class ExtendedKalmanFilter:
    def __init__(self, mean, cov, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.reset()

    def reset(self):
        self.mu = self._init_mean
        self.sigma = self._init_cov

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        matrixG = env.G(self.mu, u)
        matrixV = env.V(self.mu, u)

        matrixM = np.array([[self.alphas[0] * u[0,0] * u[0,0] + self.alphas[1] * u[1,0] * u[1,0], 0, 0],
                            [0, self.alphas[2] * u[1,0] * u[1,0] + self.alphas[3] * (u[0,0] * u[0,0] + u[2,0] * u[2,0] ), 0],
                            [0, 0, self.alphas[0] * u[2,0] * u[2,0] + self.alphas[1] * u[1,0] * u[1,0]]])
        
        
        mu_rayita = self.mu + np.array([[u[1,0]*np.cos(self.mu[2,0]+u[0,0])],
                                     [u[1,0]*np.sin(self.mu[2,0]+u[0,0])],
                                     [u[0,0]+u[2,0]]])

        sigma_rayita = np.dot(np.dot(matrixG , self.sigma), matrixG.T) + np.dot(np.dot(matrixV , matrixM), matrixV.T)

        
        dx = env.MARKER_X_POS[marker_id] - mu_rayita[0,0]
        dy = env.MARKER_Y_POS[marker_id] - mu_rayita[1,0]

        z_est = np.array([[minimized_angle(np.arctan2(dy,dx) - mu_rayita[2,0])]])

        matrixH = np.reshape(env.H(mu_rayita, marker_id),(1,3))

        matrixQ = self.beta

        matrixS = np.dot(np.dot(matrixH , sigma_rayita), matrixH.T) + matrixQ
        matrixK = np.dot(np.dot(sigma_rayita , matrixH.T), np.linalg.inv(matrixS)) 
        
        mu_rayita = mu_rayita + np.dot(matrixK, z-z_est)

        sigma_rayita = np.dot(np.eye(3) - np.dot(matrixK, matrixH), sigma_rayita)

        self.mu = mu_rayita
        self.sigma = sigma_rayita

        return self.mu, self.sigma
