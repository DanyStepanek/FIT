# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""

import socket
import re
import threading as th
import time
from pathlib import Path

#https://stackoverflow.com/questions/13180941/how-to-kill-a-while-loop-with-a-keystroke
keep_going = True
def key_capture_thread():
    global keep_going
    input()
    keep_going = False
    
def transform_date_to_name(date): 
    tmp = date.replace(" ", "") 
    return tmp.replace(":", "_") 
   
"""
    TCP Client for Empatica E4.            
"""
class Client():
    
    def __init__(self, device_id='1A37CD' ,host='127.0.0.1', port=28000, e_name='', 
            folder='.\\data'):
       
        self.host = host
        self.port = port
        self.device_id = device_id
        self.folder = folder
        self.e_name = e_name
        
        p = Path(self.folder)
        p.mkdir(exist_ok=True)

        date = time.ctime(time.time())
        self.filename = '_{}'.format(transform_date_to_name(date))
    
    """
        Connect to Empatica E4 TCP server
    """        
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (self.host, self.port)
        print('Connecting to {}:{}'.format(self.host, self.port))
        try:
            sock.connect(server_address)
        except Exception as e:
            print(e)
            return
        
        self._session(sock)
    
    """
        Session handler
    """
    def _session(self, sock):
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
            with open('{}\{}.txt'.format(self.folder, self.filename),'wb') as f:
                while keep_going:
                    response = sock.recv(2048)
                    f.write(response)
                    
        except Exception as e:
            print(e)
            return            
        
        finally:
            self.close(sock)
    
    """
        Close session.
    """
    def close(self, sock):
        message = 'device_disconnect\r\n'
        try:
            print('sending {}'.format(message))
            sock.sendall(str.encode(message))
        
        finally:    
            print('closing socket')
            sock.close()
            print('Data received and saved\n')
            
            
if __name__ == '__main__':
    client = Client()
    client.connect()