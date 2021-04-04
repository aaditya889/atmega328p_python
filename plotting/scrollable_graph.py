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

    self.fig = None

  def init_subplots(self, axb_plots: list, plot_size_ratios: dict):

    subplots = list()
    self.fig, axs = plt.subplots(axb_plots[0], axb_plots[1], figsize=(16, 7.7), gridspec_kw=plot_size_ratios)
    if axb_plots[0] == 1 or axb_plots[1] == 1:
      try:
        subplots.extend(axs)
      except TypeError:
        subplots.extend([axs])
    else:
      for idx1 in range(axb_plots[0]):
        for idx2 in range(axb_plots[1]):
          subplots.append(axs[idx1][idx2])
    self.subplots = subplots
    self.n_plots = axb_plots[0] * axb_plots[1]

  def init_graphs(self, plot_limits: list, plot_line_width: float = 1.5, graph_colours: list = None,
                  graph_mapping: list = None, graph_labels: list[list[str]] = [], graph_legends: list = []):
    subplots = self.subplots
    self.n_graphs = len(graph_mapping)
    self.graph_mapping = graph_mapping
    # CHECK THIS AGAIN
    assert self.n_plots == len(graph_labels)

    for graph_idx in range(self.n_graphs):
      assert graph_mapping[graph_idx] < self.n_plots
      colour = graph_colours[graph_idx] if graph_colours else self.colors(random.randint(1, 99))
      self.graphs.append(subplots[graph_mapping[graph_idx]].plot([], [], linewidth=plot_line_width)[0])
      self.graphs[graph_idx].set_color(colour)

    for subplot_idx in range(self.n_plots):
      subplots[subplot_idx].set_xlim(plot_limits[subplot_idx][0], plot_limits[subplot_idx][1])
      subplots[subplot_idx].set_ylim(plot_limits[subplot_idx][2], plot_limits[subplot_idx][3])
      subplots[subplot_idx].grid(True)
      subplots[subplot_idx].set_title(graph_labels[subplot_idx][0])
      subplots[subplot_idx].set_xlabel(graph_labels[subplot_idx][1])
      subplots[subplot_idx].set_ylabel(graph_labels[subplot_idx][2])
      legend = graph_legends[subplot_idx] if graph_legends else None
      if legend:
        subplots[subplot_idx].legend(legend, bbox_to_anchor=(1., 1), loc=2)

    self.plot_limits = plot_limits
    self.plot_colours = graph_colours
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
        x = np.linspace(xrange[graph_mapping[idx]][0], xrange[graph_mapping[idx]][1], xrange[graph_mapping[idx]][1])
        graphs[idx].set_data(x, data_queue[idx])
    return animate

  def show_plots(self, **kwargs):
    plt.subplots_adjust(**kwargs)
    plt.show()