import socket
from .parallel_processing import multi_thread


@multi_thread('mpu_read')
def save_udp_packets_to_file(file_name):
    UDP_IP = "192.168.43.13"
    UDP_PORT = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))
    print("%s Listening on %d" % (UDP_IP, UDP_PORT))
    fd = open(file_name, 'a')
    try:
        while True:
            data = sock.recv(1000).decode()
            fd.write(data + '\n')
            # print(data)
    except KeyboardInterrupt:
        fd.close()


@multi_thread('mpu_read')
def read_udp_packets(num_packets=4):
    UDP_IP = "192.168.43.13"
    UDP_PORT = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))
    print("%s Listening on %d" % (UDP_IP, UDP_PORT))
    while num_packets:
        data = sock.recv(1000).decode()
        num_packets -= 1