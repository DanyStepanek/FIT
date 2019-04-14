#!/usr/bin/python 3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 21:58:01 2019

@author: Daniel Stepanek xstepa61
"""


import sys
import socket
import json



def Main():
  
    if(len(sys.argv) == 3):
        city = (sys.argv[2]).lower()
        api_key = sys.argv[1]
                
        host = "api.openweathermap.org"
        port = 80
        
        request = "GET /data/2.5/weather?q="+city+"&APPID="+api_key+"&units=metric HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n"
        #str to byte
        request = request.encode()
        
        #connect to the server        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(request)

        #get data from server        
        result = s.recv(4096)
        
        #data decoding
        result = result.decode("utf-8")
        result = result.split("\n")[-1]
       
        #output 
        info = json.loads(result)
        degree_sign = '\u2103'
                
        if 'name' in info.keys():
            print ("{}".format(info['name']))
        if 'weather' in info.keys():    
            print ("{}".format(info['weather'][0]['description']))
        if 'main' in info.keys():
            print ("temp:{}".format(info['main']['temp'])+degree_sign)
            print ("humidity:{}".format(info['main']['humidity'])+"%")
            print ("preassure:{}".format(info['main']['pressure'])+" hPa")
        if 'wind' in info.keys():    
            print ("wind-speed:{}".format(info['wind']['speed'])+"km/h")
            if 'deg' in info['wind'].keys():
                print ("wind-deg:{}".format(info['wind']['deg']))
            else:
                print("wind-deg: N/A")
		
        s.close()


if __name__ == "__main__":
	Main()

