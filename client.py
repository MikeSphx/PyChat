import sys
import os
import argparse
import socket
import json
import thread

def get_user_by_name(users, name):
    """
    Searches given array for user with given name

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

def receive_messages(socket):
    """
    Function that runs on its own thread for receiving messages from server
    as well as other clients

    Args:
        socket: Socket object to communicate through
    """
    s = socket

    # Continually listens for new messages
    while True:
        data, addr = s.recvfrom(1024)
        
        try:
            data = json.loads(data)
        except:
            print 'Unable to deserialize packet received from server'
            continue
        
        # Handler for receiving message packet from server
        if data['packet_type'] == 'MESSAGE':
            ip = addr[0] 
            port = addr[1]
            user = data['sender']
            msg = data['msg']
            print '\n<- <From '+ip+':'+str(port)+':'+user+'>: '+msg
            sys.stdout.write('+> ')
            sys.stdout.flush()
        
        # Handler for receiving the response to SIGN_IN from server
        elif data['packet_type'] == 'SIGN_IN_RESPONSE':
            # When a new user signs in, give that user a list of
            # all the connected users he/she can send msgs to
            global users
            users = data['users']

        # Handler for receiving the response to LIST from server
        elif data['packet_type'] == 'LIST_RESPONSE':
            print data['response']
	    sys.stdout.write('+> ')
            sys.stdout.flush()
        
        # Handler for receiving any ERROR messages from the server
        elif data['packet_type'] == 'ERROR':
            print data['error']
            os._exit(1)

def main():
    """
    Main entry point of the program, handles the client side of the socket connection
    that is behind this simple chat protocol

    """
    # Parsing arguments from command line using the argparse library
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-u', dest='user', action='store', help='Username to sign in with', required=True, type=str)
    required.add_argument('-sip', dest='server_ip', action='store', help='Server IP to connect to', required=True, type=str)
    required.add_argument('-sp', dest='server_port', action='store', help='Server port to connect to', required=True, type=int)
    arguments = parser.parse_args()

    # Saving agruments passed from command line
    user = arguments.user
    sip = arguments.server_ip
    sp = arguments.server_port

    # Create UDP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    # Start new thread for listening for messages
    thread.start_new_thread(receive_messages, (s,))
     
    # Code for SIGN-IN message to the server
    # Build packet for SIGN_IN command
    sign_in_packet_dict = {
                              'packet_type': 'SIGN_IN',
                              'username': user
                          }
    sign_in_packet_string = json.dumps(sign_in_packet_dict)
    # Send the packet to server for sign-in command
    s.sendto(sign_in_packet_string, (sip, sp))

    # Code for list and send commands
    while True:
        user_input = raw_input('+> ')
        cmd = user_input.split(' ')

        # Handling list command from client
        if cmd[0] == 'list':
            # Build packet for list command
            list_packet_dict = {
                                   'packet_type': 'LIST',
                                   'sender':user
                               }
            list_packet_string = json.dumps(list_packet_dict)
            # Send the packet to server for list command
            s.sendto(list_packet_string, (sip, sp))
        
        # Handling send command from client
        elif cmd[0] == 'send':
            # Error handling arguments for send
            if len(cmd) < 3:
                print "Incorrect number of arguments for send command"
                print "send USERNAME MESSAGE"
                continue
            else:
                # Parsing arguments for building send command
                receiver = cmd[1]
                msg = ' '.join(cmd[2:])

                # Check arguments for errors
                if get_user_by_name(users, receiver) == None:
                    print "User does not exist"
                    continue
                
                # Setup the address to send the message to
                receiving_user = get_user_by_name(users, receiver)
                receiving_ip = receiving_user['addr'][0]
                receiving_port = receiving_user['addr'][1]
                # Setup the message to be sent
                message_packet = {
                                     'packet_type': 'MESSAGE',
                                     'sender': user,
                                     'msg': msg
                                 }
                message_packet = json.dumps(message_packet)
                s.sendto(message_packet, (receiving_ip, receiving_port))

        # Handling invalid command from client
        else:
            print "Invalid user command. Use one of the following:\nlist\nsend USERNAME MESSAGE"

if __name__ == "__main__":
    main()

