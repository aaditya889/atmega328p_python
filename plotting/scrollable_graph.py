import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random


class ScrollableGraph:

  colors = plt.get_cmap('coolwarm', 100)
  subplots = []
  graphs = []
  animations = []

  def __init__(self, axb_plots: list, plot_limits: list, plot_line_width: float = 1.5, plot_colours: list = None,
               subplot_generator_functions: list = [], sublot_intervals_in_ms: list = [], data_queue: list = [],
               in_sync=True):
    # General plot parameters
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['xtick.major.size'] = 10
    mpl.rcParams['xtick.major.width'] = 2
    mpl.rcParams['ytick.major.size'] = 10
    mpl.rcParams['ytick.major.width'] = 2

    subplots = list()
    if axb_plots[0] == 1 or axb_plots[1] == 1:
      self.fig, axs = plt.subplots(axb_plots[0], axb_plots[1])
      subplots.extend(axs)
    else:
      self.fig, axs = plt.subplots(axb_plots[0], axb_plots[1])
      for idx1 in range(axb_plots[0]):
        for idx2 in range(axb_plots[1]):
          subplots.append(axs[idx1][idx2])

    for subplot_idx in range(0, axb_plots[0] * axb_plots[1]):
      subplots[subplot_idx].set_xlim(plot_limits[subplot_idx][0], plot_limits[subplot_idx][1])
      subplots[subplot_idx].set_ylim(plot_limits[subplot_idx][2], plot_limits[subplot_idx][3])
      colour = plot_colours[subplot_idx] if plot_colours else self.colors(random.randint(1, 99))
      subplots[subplot_idx].grid(True)
      self.graphs.append(subplots[subplot_idx].plot([], [], linewidth=plot_line_width)[0])
      self.graphs[subplot_idx].set_color(colour)
      if not in_sync:
        self.animations.append(FuncAnimation(fig=self.fig,
                                           func=self.animate_wrapper(
                                             subplot_generator_functions[subplot_idx],
                                             self.graphs[subplot_idx],
                                             plot_limits[subplot_idx][0],
                                             plot_limits[subplot_idx][1],
                                             data_queue[subplot_idx]
                                           ), frames=plot_limits[subplot_idx][1],
                                           interval=sublot_intervals_in_ms[subplot_idx], repeat=True))

    if in_sync:
      self.animations.append(FuncAnimation(fig=self.fig,
                                           func=self.animate_insync_wrapper(
                                             subplot_generator_functions,
                                             self.graphs,
                                             plot_limits,
                                             data_queue
                                           ),
                                           frames=plot_limits[0][1],
                                           interval=sublot_intervals_in_ms[0], repeat=True))
    plt.show()

  def animate_wrapper(self, generator_function, graphs, xrange_low, xrange_high, data_queue):
    def animate(i):
      generator_function()
      x = np.linspace(xrange_low, xrange_high, xrange_high)
      graphs.set_data(x, data_queue)
    return animate

  def animate_insync_wrapper(self, generator_functions, graphs, xrange, data_queue):
    def animate(i):
      for idx in range(len(graphs)):
        generator_functions[idx]()
        x = np.linspace(xrange[idx][0], xrange[idx][1], xrange[idx][1])
        graphs[idx].set_data(x, data_queue[idx])
    return animate


def test_gen():
  dq.extend([random.randint(1,100)])
  del dq[0]


def test_gen2():
  dq2.extend([random.randint(1, 100)])
  del dq2[0]


dq = [50] * 20
dq2 = [50] * 20
s = ScrollableGraph([2, 2], [[1, len(dq), 1, 100], [1, len(dq2), 1, 100], [1, len(dq), 1, 100], [1, len(dq2), 1, 100]], subplot_generator_functions=[test_gen, test_gen2, test_gen, test_gen2], plot_colours=['cyan', 'red', 'blue', 'green'], sublot_intervals_in_ms=[1, 1, 1, 1],
                    data_queue=[dq, dq2, dq, dq2])
