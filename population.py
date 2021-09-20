# Import
import numpy as np
from particle import Particle

# Population class
class Population:
  # Constructor
  def __init__(self, parent):
    self.parent = parent                        # Parent (Optimizer)
    self.particles = np.zeros(self.parent.size) # Particles

    for i in range(self.parent.size):
      self.particles[i] = Particle(self, i)

  # Iterate function
  def iterate(self):
    self.best().search()
    for i in range(self.parent.size):
      self.particles[i].eval()
      self.particles[i].move()

  # Find best particle
  def best(self):
    b = self.particles[0]
    for i in range(self.parent.size):
      if self.parent.f(self.positions()[i]) < self.parent.f(self.positions()[b]):
        b = i
    return self.particles[b]

  # Get position of all particles
  def positions(self):
    return np.array([p.position for p in self.particles])

  # Get objective function value of all particles
  def values(self):
    return np.array([p.value for p in self.particles])

  # Get total force vector of all particles
  def forces(self):
    # Calculate denominator sum
    d = 0
    for i in range(self.parent.size):
      d += self.parent.f(self.positions()[i]) - self.parent.f(self.best().position)

    # Calculate particle charge
    q = np.zeros(self.parent.size)
    f = np.zeros(self.parent.size)
    for i in range(self.parent.size):
      t = self.parent.f(self.positions()[i]) - self.parent.f(self.best().position)
      q[i] = np.exp(-self.parent.dim * t / d)

    # Calculate force by Coulomb's law
    for i in range(self.parent.size):
      for j in range(self.parent.size):
        if i is not j:
          s = np.subtract(self.positions()[i], self.positions()[j])
          for k in range(self.parent.dim):
            if self.parent.f(self.positions()[j]) < self.parent.f(self.positions()[i]):
              f[k] += (self.positions()[j][k] - self.positions()[i][k]) * q[i] * q[j] / np.square(np.dot(s, s))
            else:
              f[k] -= (self.positions()[j][k] - self.positions()[i][k]) * q[i] * q[j] / np.square(np.dot(s, s))

    return f

  # Get maximum range of the space
  def max_range(self):
    m = 0
    for k in range(self.parent.dim):
      m = np.max(self.parent.upper[k] - self.parent.lower[k], m)
    return m

