# -*- coding: utf-8 -*-
"""
 Project: Bachelor thesis
 Theme: Physiological Data to Analyze and Improve the User Experience
 Author: Daniel Stepanek
 License: GPL 3.0

 VUT FIT Brno 2021

"""

import os
import sys
import socket
import re
import threading as th
import time
from pathlib import Path


keep_going = True
def key_capture_thread():
    #https://stackoverflow.com/questions/13180941/how-to-kill-a-while-loop-with-a-keystroke
    global keep_going
    input()
    keep_going = False

def transform_date_to_name(date):
    tmp = date.replace(" ", "")
    return tmp.replace(":", "_")

class Client():
    """
    TCP Client for Empatica E4.
    """

    def __init__(self, device_id='1A37CD' ,host='127.0.0.1', port=28000, folder='./data'):

        """
        TCP Client for Empatica E4.

        Parameters
        ----------

        device_id : str
            Empatice E4 device ID.

        host : str
            ip address of the TCP Empatica server.

        port : int
            TCP server port.

        folder : str
            Folder where received data will be stored.

        """

        self.host = host
        self.port = port
        self.device_id = device_id
        self.folder = folder

        p = Path(self.folder)
        p.mkdir(exist_ok=True)

        date = time.ctime(time.time())
        self.filename = '_{}'.format(transform_date_to_name(date))

    def connect(self):
        """
            Connect to Empatica E4 TCP server
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (self.host, self.port)
        try:
            print('Connecting to {}:{}'.format(self.host, self.port))
            sock.connect(server_address)
        except Exception as e:
            print(e)
            return

        self.session(sock)

    def session(self, sock):
        """
            Session handler. Connect to device, subscribe required signals,
            receive data until 'Enter' key is pressed.

            Parameters
            ----------

            sock : socket

        """

        try:
            #connect to E4
            message = 'device_connect {}\r\n'.format(self.device_id)
            print('sending {}'.format(message))
            sock.sendall(str.encode(message))

            response = sock.recv(50)
            print('received {}'.format(str(response, 'utf-8')))

            if not re.match('(R device_connect OK).*', str(response, 'utf-8')):
                return

            #pause data stream
            message = 'pause ON\r\n'
            print('sending {}'.format(message))
            sock.sendall(str.encode(message))
            response = sock.recv(1024)
            print('received {}'.format(str(response, 'utf-8')))

            #set stream subscriptions ON
            messages = ['device_subscribe bvp ON\r\n',
                        'device_subscribe gsr ON\r\n',
                        'device_subscribe ibi ON\r\n',
                        'device_subscribe tmp ON\r\n',
                        'device_subscribe tag ON\r\n']
            for msg in messages:
                print('sending {}'.format(msg))
                sock.sendall(str.encode(msg))

                response = sock.recv(1024)
                print('received {}'.format(str(response, 'utf-8')))

            message = 'pause OFF\r\n'
            print('sending {}'.format(message))
            sock.sendall(str.encode(message))
            response = sock.recv(1024)
            print('received {}'.format(str(response, 'utf-8')))

            print('Receiving data')

            #start thread for key interruption (Enter)
            th.Thread(target=key_capture_thread, args=(),
                      name='key_capture_thread', daemon=True).start()

            #write received data to file until key is pressed
            with open('{}/{}.txt'.format(self.folder, self.filename),'wb') as f:
                while keep_going:
                    response = sock.recv(2048)
                    f.write(response)

        except Exception as e:
            print(e)
            sys.exit(-1)

        finally:
            self.close(sock)

    def close(self, sock):
        """
        Close session.

        Parameters
        ----------

        sock : socket

        """

        message = 'device_disconnect\r\n'
        try:
            print('sending {}'.format(message))
            sock.sendall(str.encode(message))

        finally:
            print('closing socket')
            sock.close()
            print('Data received and saved\n')


if __name__ == '__main__':
    path = os.path.dirname(os.getcwd())
    path = '{}/data'.format(path)

    client = Client(folder=path)
    client.connect()
