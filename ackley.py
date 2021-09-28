# Import
import numpy as np
from interface import Interface
from optimizer import Optimizer

# Ackley function with dimension 4 as objective function
def ackley4(pos):
  s = np.sum(np.array([v * v for v in pos]))
  c = np.sum(np.array([np.cos(v) for v in pos]))
  return -20 * np.exp(-0.2 * np.sqrt(s / 4)) - np.exp(1 / 4 * c) + 20 + np.exp(1)

def ackley4V(x, y, z, w):
  s = x * x + y * y + z * z + w * w
  c = np.cos(x) + np.cos(y) + np.cos(z) + np.cos(w)
  return -20 * np.exp(-0.2 * np.sqrt(s / 4)) - np.exp(1 / 4 * c) + 20 + np.exp(1)

# Execution script
if __name__ == '__main__':
  o = Optimizer(4, [-5, -5, -5, -5], [5, 5, 5, 5], 20, ackley4, step=0.025)
  i = Interface(o, 'Ackley function', 'ackley')
  i.plot_posbar(ackley4V)

  while i.opt.gen < 50:
    i.opt.iterate()
    i.record()
    i.plot_posbar(ackley4V)
  i.plot_ofv()
