import sys
import argparse
import socket

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-u', dest='user', action='store', help='Username to sign in with', required=True, type=str)
    required.add_argument('-sip', dest='server_ip', action='store', help='Server IP to connect to', required=True, type=str)
    required.add_argument('-sp', dest='server_port', action='store', help='Server port to connect to', required=True, type=int)
    arguments = parser.parse_args()

    # Test
    print "User: " + arguments.user
    print "SIP: " + arguments.server_ip
    print "SP: " + str(arguments.server_port)

    # Saving agruments passed from command line
    user = arguments.user
    sip = arguments.server_ip
    sp = arguments.server_port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    while True:
        msg = raw_input('+> ')

        try:
            s.sendto(msg, (sip, port))

            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
         
            print 'Server reply : ' + reply
     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

if __name__ == "__main__":
    main()