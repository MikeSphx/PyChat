import sys
import argparse
import socket

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-sp', dest='server_port', action='store', help='UDP port to listen on', required=True, type=int)
    arguments = parser.parse_args()

    # Test
    #print "SP: " + str(arguments.server_port)

    # Saving agruments passed from command line
    sp = arguments.server_port
    # Initailizing host parameter for the socket
    host = ''

    # Create UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Attempt to associate the socket to a network interface and port
    try:
        s.bind((host, sp))
    except:
        print 'Failed to bind socket'
        sys.exit(-1)

    print 'Socket bind successful'

    while True:
        data, addr = s.recvfrom(1024)

        if not data:
            break

        reply = 'OK...' + data

        s.sendto(reply, addr)
        print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

        #print 'Connected with ' + address[0] + ':' + str(address[1])
        #start_new_thread( , conn)

    s.close()


if __name__ == "__main__":
    main()