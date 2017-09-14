import sys
import argparse

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

if __name__ == "__main__":
    main()