import socket
def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    udp_socket.sendto(send_data.encode("utf-8"),

    udp_socket.close
if __name__=="__main__":
    main()