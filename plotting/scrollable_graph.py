import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random
from lib.parallel_processing import *


class ScrollableGraph:

  colors = plt.get_cmap('coolwarm', 100)
  subplots = list()
  plot_limits = list()
  plot_colours = list()
  plot_line_width = 1.5
  graphs = []
  animations = []
  n_plots = int()
  n_graphs = int()
  graph_mapping = list()

  def __init__(self):
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

  def init_subplots(self,  axb_plots: list):

    subplots = list()
    if axb_plots[0] == 1 or axb_plots[1] == 1:
      self.fig, axs = plt.subplots(axb_plots[0], axb_plots[1])
      try:
        subplots.extend(axs)
      except TypeError:
        subplots.extend([axs])
    else:
      self.fig, axs = plt.subplots(axb_plots[0], axb_plots[1])
      for idx1 in range(axb_plots[0]):
        for idx2 in range(axb_plots[1]):
          subplots.append(axs[idx1][idx2])
    self.subplots = subplots
    self.n_plots = axb_plots[0] * axb_plots[1]

  def init_graphs(self, plot_limits: list, plot_line_width: float = 1.5, plot_colours: list = None,
                  graph_mapping: list = None):
    subplots = self.subplots
    self.n_graphs = len(graph_mapping)
    self.graph_mapping = graph_mapping

    for subplot_idx in range(self.n_plots):
      subplots[subplot_idx].set_xlim(plot_limits[subplot_idx][0], plot_limits[subplot_idx][1])
      subplots[subplot_idx].set_ylim(plot_limits[subplot_idx][2], plot_limits[subplot_idx][3])
      subplots[subplot_idx].grid(True)

    for graph_idx in range(self.n_graphs):
      assert graph_mapping[graph_idx] < self.n_plots
      colour = plot_colours[graph_idx] if plot_colours else self.colors(random.randint(1, 99))
      self.graphs.append(subplots[graph_mapping[graph_idx]].plot([], [], linewidth=plot_line_width)[0])
      self.graphs[graph_idx].set_color(colour)

    self.plot_limits = plot_limits
    self.plot_colours = plot_colours
    self.plot_line_width = plot_line_width

  @multi_thread('22222')
  def init_graph_generators(self, generator_functions: list = None, intervals_in_ms: list = None,
                            data_queue: list = None, in_sync=True):

    plot_limits = self.plot_limits
    for graph_idx in range(self.n_graphs):
      if not in_sync:
        try:
            generator_function = generator_functions[graph_idx]
        except IndexError:
            generator_function = None
        self.animations.append(FuncAnimation(fig=self.fig,
                                             func=self.animate_wrapper(
                                             generator_function,
                                             self.graphs[graph_idx],
                                             plot_limits[self.graph_mapping[graph_idx]][0],
                                             plot_limits[self.graph_mapping[graph_idx]][1],
                                             data_queue[graph_idx]
                                           ), frames=plot_limits[graph_idx][1],
                                             interval=intervals_in_ms[graph_idx], repeat=True))

    if in_sync:
      self.animations.append(FuncAnimation(fig=self.fig,
                                           func=self.animate_insync_wrapper(
                                             generator_functions,
                                             self.graphs,
                                             plot_limits,
                                             data_queue
                                           ),
                                           frames=plot_limits[0][1],
                                           interval=intervals_in_ms[0], repeat=True))

  def animate_wrapper(self, generator_function, graphs, xrange_low, xrange_high, data_queue):
    def animate(i):
      if generator_function is not None:
        generator_function()
      x = np.linspace(xrange_low, xrange_high, xrange_high)
      graphs.set_data(x, data_queue)
    return animate

  def animate_insync_wrapper(self, generator_functions, graphs, xrange, data_queue):

    graph_mapping = self.graph_mapping
    def animate(i):
      for idx in range(len(graphs)):
        # try:
        #     generator_functions[idx]()
        # except IndexError:
        #     pass
        # print(data_queue)
        x = np.linspace(xrange[graph_mapping[idx]][0], xrange[graph_mapping[idx]][1], xrange[graph_mapping[idx]][1])
        graphs[idx].set_data(x, data_queue[idx])
    return animate

  def show_graphs(self):
    plt.show()


# def test_gen():
#   dq.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq[0:4]
#   dq6.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq6[0:4]
#   dq5.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq5[0:4]
#   dq4.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq4[0:4]
#   dq3.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq3[0:4]
#   dq2.extend([random.randint(1,100), random.randint(1,100), random.randint(1,100), random.randint(1,100)])
#   del dq2[0:4]

# print([random.randint(1, 100)])
# print([random.randint(1, 100)])

# dq = [0] * 20
# dq2 = [50] * 20
# dq3 = [50] * 20
# dq4 = [50] * 20
# dq5 = [50] * 20
# dq6 = [50] * 20
#
# s = ScrollableGraph()
# s.init_subplots([2, 2])
# s.init_graphs([[1, len(dq), -100, 100], [1, len(dq2), 1, 100], [1, len(dq3), 1, 100], [1, len(dq4), 1, 100],  [1, len(dq5), 1, 100],  [1, len(dq6), 1, 100]],
#               plot_colours=['cyan', 'red', 'blue', 'green', 'yellow', 'black'], graph_mapping=[0, 0, 1, 1, 2, 2])
# s.init_graph_generators(generator_functions=[test_gen], intervals_in_ms=[1, 1, 1, 1, 1, 1],
#                         data_queue=[dq, dq2, dq3, dq4, dq5, dq6], in_sync=True)
# s.show_graphs()
