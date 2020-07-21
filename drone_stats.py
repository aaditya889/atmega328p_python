import os
import time
from plotting.scrollable_graph import ScrollableGraph
from lib.file_reader import *
# from lib.udp_read import *
import socket
from lib.parallel_processing import multi_thread


# key value pair below signifies the index in the data queue, for that key
# TO_CAPTURE = {'YX': 0, 'YY': 1, 'DTFA': 2, 'DTFB': 3, 'DTRA': 4, 'DTRB': 5}
TO_CAPTURE = {'YX': 0, 'YY': 1, 'DTFA': 2, 'DTFB': 3, 'DTRA': 4, 'DTRB': 5}

MAX_VALUES_TO_STORE = 400

UDP_IP = "192.168.43.13"
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
        # data = file_reader.__next__()
        data = sock.recv(200).decode()
        new_data.append(data + '\n')
        # if data is not None:
        #     new_data.extend([data])
    # for data in new_data:
        if not data.startswith('DBG::'):
            continue

        for capture in TO_CAPTURE:
            value = float(data.split(capture + ':')[1].lstrip().split(' ')[0])
            # print("Got value: %f, storing in %d (%s)" % (value, TO_CAPTURE[capture], capture))
            data_queues[TO_CAPTURE[capture]].extend([value])
            # del data_queues[TO_CAPTURE[capture]][0]
            data_queues[TO_CAPTURE[capture]].pop(0)
        if i > FLUSH_THRESHOLD:
            fd.writelines(new_data)
            del new_data
            new_data = []
            i = 0
    # print(data_queues)


# def generator_function():
#
#     # print("=============")
#     # generator_function(file_reader)
#     print("=============")
#     filter_stats(file_reader)
#
#     print(data_queues)

file_name = 'drone_stats'
# save_udp_packets_to_file(file_name)
stats_generator_function()
file_reader = read_file_indefinite(file_name)
data_queues = [[0 for i in range(MAX_VALUES_TO_STORE)] for j in range(len(TO_CAPTURE.keys()))]

s = ScrollableGraph()
s.init_subplots([3, 1])
graph_plot_limits = [[1, len(data_queues[i]), -100, 100] for i in range(len(data_queues))]
s.init_graphs(graph_plot_limits, plot_colours=['cyan', 'red', 'blue', 'green', 'yellow', 'black'],
              graph_mapping=[0, 0, 1, 1, 2, 2])

s.init_graph_generators(generator_functions=[stats_generator_function], intervals_in_ms=[1],
                        data_queue=[data_queues[i] for i in range(len(data_queues))], in_sync=True)
s.show_graphs()
