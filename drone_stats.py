import os
import time
from plotting.scrollable_graph import ScrollableGraph
from lib.file_reader import *

# key value pair below signifies the index in the data queue, for that key
TO_CAPTURE = {'YX': 0, 'YY': 1, 'DTFA': 2, 'DTFB': 3, 'DTRA': 4, 'DTRB': 5}
MAX_VALUES_TO_STORE = 50


def stats_generator_function(num_data_points=4):

    new_data = []
    for i in range(num_data_points):
        data = file_reader.__next__()
        if data is not None:
            new_data.extend([data])
    for data in new_data:
        if not data.startswith('DBG::'):
            continue

        for capture in TO_CAPTURE:
            value = float(data.split(capture + ':')[1].lstrip().split(' ')[0])
            # print("Got value: %f, storing in %d (%s)" % (value, TO_CAPTURE[capture], capture))
            data_queues[TO_CAPTURE[capture]].extend([value])
            del data_queues[TO_CAPTURE[capture]][0]


# def generator_function():
#
#     # print("=============")
#     # generator_function(file_reader)
#     print("=============")
#     filter_stats(file_reader)
#
#     print(data_queues)

file_mame = 'drone_stats'
file_reader = read_file_indefinite(file_mame)
data_queues = [[0 for i in range(MAX_VALUES_TO_STORE)] for j in range(len(TO_CAPTURE.keys()))]

s = ScrollableGraph()
s.init_subplots([2, 2])
graph_plot_limits = [[1, len(data_queues[i]), -180, 180] for i in range(len(data_queues))]
s.init_graphs(graph_plot_limits, plot_colours=['cyan', 'red', 'blue', 'green', 'yellow', 'black'],
              graph_mapping=[0, 0, 1, 1, 2, 2])

s.init_graph_generators(generator_functions=[stats_generator_function], intervals_in_ms=[1, 1, 1, 1, 1, 1],
                        data_queue=[data_queues[i] for i in range(len(data_queues))], in_sync=True)
s.show_graphs()
