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

def main():
    """
    Main entry point of the program, handles the UDP socket connection for the
    server side of the chat protocol

    """
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
            # If so, return an error package
            else:
                reply = {
                            'packet_type': 'ERROR',
                            'error': '<- Username is already taken'
                        }
                reply = json.dumps(reply)
                s.sendto(reply, addr)
        # Handling the list command
        elif data['packet_type'] == 'LIST':
            # Build reply packet to send back to client
            reply = {
                        'packet_type' : 'SIGN_IN_RESPONSE',
                        'msg' : '<- Signed In Users: ' + ', '.join([user['name'] for user in users])
                    }
            reply = json.dumps(reply)
            s.sendto(reply, addr)
        # Handling the send_addr command, which asks for the address of the given user
        elif data['packet_type'] == 'FIND_DEST':
            print 'Received FIND_DEST command to user: '+data['name'] 
            print get_user_by_name(users, data['name'])
            dest_user = get_user_by_name(users, data['name'])
            # If user exists, send delivery information to client
            if dest_user != None:
                dest_addr = dest_user['addr']

                print dest_addr

                reply = {
                            'packet_type': 'SEND_DEST',
                            'dest': dest_addr
                        }
                reply = json.dumps(reply)
                s.sendto(reply, addr)
            # If the user does not exist, send error to client
            else:
                reply = {
                            'packet_type': 'ERROR',
                            'error': 'User does not exist, therefore cannot send message'
                        }
                reply = json.dumps(reply)
                s.sendto(reply, addr)
        # Handling invalid commands
        else:
            print 'Client has sent invalid command'
            continue

        #if not data:
        #    break

        #reply = 'OK...' + data

        #s.sendto(reply, addr)
        #print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

        #print 'Connected with ' + address[0] + ':' + str(address[1])
        #start_new_thread( , conn)

    s.close()


if __name__ == "__main__":
    main()
