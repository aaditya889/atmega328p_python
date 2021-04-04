from plotting.scrollable_graph import ScrollableGraph
from lib.file_reader import *
import socket
from lib.parallel_processing import multi_thread


# key value pair below signifies the index in the data queue, for that key
TO_CAPTURE = {'YX': 0, 'YY': 1, 'DTFA': 2, 'DTFB': 3, 'DTRA': 4, 'DTRB': 5}

MAX_VALUES_TO_STORE = 400

UDP_IP = "192.168.1.31"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

FLUSH_THRESHOLD = 500


@multi_thread('randommmm')
def stats_generator_function(num_data_points=50):

    fd = open(file_name, 'a+')
    new_data = []
    i = 0
    while True:
        i += 1
        data = sock.recv(200).decode()
        new_data.append(data + '\n')
        if not data.startswith('DBG::'):
            print(data)
            continue

        for capture in TO_CAPTURE:
            value = float(data.split(capture + ':')[1].lstrip().split(' ')[0])
            data_queues[TO_CAPTURE[capture]].extend([value])
            data_queues[TO_CAPTURE[capture]].pop(0)
        if i > FLUSH_THRESHOLD:
            fd.writelines(new_data)
            del new_data
            new_data = []
            i = 0


file_name = 'drone_stats'
stats_generator_function()
file_reader = read_file_indefinite(file_name)
data_queues = [[0 for i in range(MAX_VALUES_TO_STORE)] for j in range(len(TO_CAPTURE.keys()))]

# Rows and Columns of the subplots in the figure (RxC signifies the number of graphs)
subplots_in_figure = [3, 1]

# Every plot can have a Title, an X label and a Y label, in the same sequence, passed as a list of lists
graph_labels = [['Angles', 'Time', 'Angle (Theta)'], ['Front Thrust', 'Time', 'Intensity'],
                ['Rear Thrust', 'Time', 'Intensity']]

# Names for the individual graphs
graph_legends = [['Roll(X)', 'Pitch(Y)'], ['Thrust A', 'Thrust B'], ['Thrust A', 'Thrust B']]

graph_plot_limits = [[1, len(data_queues[i]), -100, 100] for i in range(len(data_queues))]

# Colour for all the graphs
graph_colours = ['cyan', 'red', 'blue', 'green', 'blue', 'green']

# Each index signifies in which subplot the data will go. For eg. in this case, the first two data streams will
# go in the first subplot (0), and so on (there are 3 subplots in total for this monitoring tool, namely 0, 1 and 2).
graph_mapping = [0, 0, 1, 1, 2, 2]

# Ratio of the subplots' heights and widths
plot_size_ratios = {'height_ratios': [1.5, 1, 1], 'width_ratios': [1]}

# Extra subplot/figure properties
plot_properties = {'hspace': 0.9, 'wspace': 0.8, 'left': 0.1, 'right': 0.85, 'top': 0.95}

# Generator function/s interval/s in ms
interval_in_ms = [1]

# Whether the data in all the plots change in synchronisation with each other
is_in_sync = True

s = ScrollableGraph()
s.init_subplots(subplots_in_figure, plot_size_ratios=plot_size_ratios)

s.init_graphs(graph_plot_limits, graph_colours=graph_colours, graph_mapping=graph_mapping, graph_labels=graph_labels,
              graph_legends=graph_legends)

s.init_graph_generators(generator_functions=[stats_generator_function], intervals_in_ms=interval_in_ms,
                        data_queue=[data_queues[i] for i in range(len(data_queues))], in_sync=is_in_sync)

s.show_plots(**plot_properties)
