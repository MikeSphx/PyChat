import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-sp', dest='server_port', action='store', help='UDP port to listen on', required=True, type=int)
    arguments = parser.parse_args()

    # Test
    print "SP: " + str(arguments.server_port)

    # Saving agruments passed from command line
    sp = arguments.server_port

if __name__ == "__main__":
    main()