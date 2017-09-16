import sys
import argparse
import socket
import json

def get_user_by_name(users, name):
    """
    Helper function for getting an object from an object array using name

    Args:
        users: Array of users
        name: Name to filter on
    
    Returns:
        The function will either return user if found or None if not found

    """
    for user in users:
        if user['name'] == name:
            return user
    return None

def update_all_clients(socket, users):
    """
    Upon a new user signing in, sends a message to all registered users with
    the updated list of all the new users

    Args:
        socket: Socket object for communicating back to the client
        users: Array of users registered in the server

    """
    for user in users:
        package = {
                      'packet_type':'SIGN_IN_RESPONSE',
                      'users':users
                  }
        package = json.dumps(package)
        socket.sendto(package, user['addr'])

def main():
    """
    Main entry point of the program, handles the UDP socket connection for the
    server side of the chat protocol

    """
    # Handle initial argument parsing from command line
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-sp', dest='server_port', action='store', help='UDP port to listen on', required=True, type=int)
    arguments = parser.parse_args()

    # Saving agruments passed from command line
    sp = arguments.server_port
    # Initailizing host parameter for the socket
    host = ''
    # Initializing the list of connected users
    users = []

    # Create UDP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print 'Failed to create socket'
        sys.exit()

    # Attempt to associate the socket to a network interface and port
    try:
        s.bind((host, sp))
    except:
        print 'Failed to bind socket'
        sys.exit(-1)

    print 'Server Initialized...'

    while True:
        data, addr = s.recvfrom(1024)

        # Deserialize the message into JSON
        data = json.loads(data)

        # Handling the sign-in command
        if data['packet_type'] == 'SIGN_IN':
            # Check if username is already taken
            if get_user_by_name(users, data['username']) == None:
                user = {
                           'name': data['username'],
                           'addr': addr
                       }
                users.append(user)
                update_all_clients(s, users)
            # If so, return an error package
            else:
                reply = {
                            'packet_type': 'ERROR',
                            'error': '\n<- Username is already taken'
                        }
                reply = json.dumps(reply)
                s.sendto(reply, addr)
        # Handling the list command
        elif data['packet_type'] == 'LIST':
            other_users = [user for user in users if user['name'] != data['sender']]
            # Build reply packet to send back to client
            reply = {
                        'packet_type' : 'LIST_RESPONSE',
                        'response' : '\n<- Signed In Users: ' + 
                                     ', '.join([user['name'] for user in other_users])
                    }
            reply = json.dumps(reply)
            s.sendto(reply, addr)
        # Handling invalid commands
        else:
            print 'Client has sent invalid command'
            continue
    s.close()

if __name__ == "__main__":
    main()

