import sys
import argparse
import socket
import json
import thread



def receive_messages(socket):
    """




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
            print '<- <From '+ip+':'+port+':'+user+'>: '+msg
        
        # Handler for receiving the response to SIGN_IN from server
        elif data['packet_type'] == 'SIGN_IN_RESPONSE':
            print data['msg']

        # Handler for receiving the response to FIND_DEST from server
        elif data['packet_type'] == 'SEND_DEST':
            print 'Received SEND_DEST command'
            print data['dest']
            #global dest_sip
            #dest_sip = data['sip']
            #global dest_sp
            #dest_sp = data['sp']
        
        # Handler for receiving any ERROR messages from the server
        elif data['packet_type'] == 'ERROR':
            print data['error']
            sys.exit()

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

    # Test TODO remove
    print "User: " + arguments.user
    print "SIP: " + arguments.server_ip
    print "SP: " + str(arguments.server_port)

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

    # Code for SIGN-IN message to the server
    # Build packet for SIGN_IN command
    sign_in_packet_dict = {
                              'packet_type': 'SIGN_IN',
                              'username': user
                          }
    sign_in_packet_string = json.dumps(sign_in_packet_dict)
    # Send the packet to server for sign-in command
    s.sendto(sign_in_packet_string, (sip, sp))

    # Start new thread for listening for messages
    thread.start_new_thread(receive_messages, (s,))

    # Code for list and send commands
    while True:
        msg = raw_input('+> ')
        cmd = msg.split(' ')

        # Handling list command from client
        if cmd[0] == 'list':
            # Build packet for list command
            list_packet_dict = {
                                   'packet_type': 'LIST'
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
                msg = cmd[2:]

                # Check arguments for errors
                

                # Building initial FIND_DEST packet
                send_addr_packet_dict = {
                                            'packet_type': 'FIND_DEST',
                                            'name': receiver
                                        }
                send_addr_packet_string = json.dumps(send_addr_packet_dict)
                s.sendto(send_addr_packet_string, (sip, sp))

                # Building and sending SEND command packet
                send_packet_dict = {
                                       'packet_type': 'MESSAGE',
                                       'sender': user,
                                       'msg': msg
                                   }
                send_packet_string = json.dumps(send_packet_dict)
                print (str(dest_sip), dest_sp)
                s.sendto(send_packet_string, (str(dest_sip), dest_sp))

        # Handling invalid command from client
        else:
            print "Invalid user command. Use one of the following:\nlist\nsend USERNAME MESSAGE"

        #try:
            #s.sendto(msg, (sip, sp))

            #d = s.recvfrom(1024)
            #reply = d[0]
            #addr = d[1]
         
            #print 'Server reply : ' + reply
     
        #except socket.error, msg:
            #print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            #sys.exit()

if __name__ == "__main__":
    main()
