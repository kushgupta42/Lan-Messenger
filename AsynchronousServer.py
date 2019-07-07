#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: root
# @Date:   2019-07-01 17:58:38
# @Last Modified by:   root
# @Last Modified time: 2019-07-07 17:44:55


# importin package for ip 
import netifaces as ni


# importing SocketServer module
import SocketServer
import socket

# iporting threading module
import threading

clients=[]
names={}

# broadcasting new connection joining 
def broadcast(client):
	for sock in clients:
		data = client+" has joined the chat\n"
		sock.send(data)
		
# broadcasting message to all
def broadcastMessage(client,message):
	for sock in clients:
		data = names[client]+":"+message
		sock.send(data)

# creating class AsynchronousHandler sub class of BaseRequestHandler
class AsynchronousHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		print("connection from: "),self.client_address[0]
		self.request.send("Enter your name: ")
		name = self.request.recv(1024)
		broadcast(name[:-1])
		
		# storing client object in list
		clients.append(self.request)
		names[self.request] = name[:-1]
		
		# loop to receive data
		while True:
			try:
				data = self.request.recv(1024)
				if data == "\n":
					pass
				elif data[:-1] == ":q":
					data = "bye guys...gtg!!"
					broadcastMessage(self.request,data)
					del names[self.request]
					clients.remove(self.request)
					break
					broadcastMessage(self.request,data)
					
				else:
					broadcastMessage(self.request,data)
				

			except:
				del names[self.request]
				clients.remove(self.request)
				break

			
		
		

# Threaded tcpserverclass
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass




ni.ifaddresses('wlan0')
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
serverAddr = ("0.0.0.0",8080)
server = ThreadedTCPServer(serverAddr,AsynchronousHandler)


# treading server
server_thread = threading.Thread(target=server.serve_forever)

# exiting the server when main threads terminate
server_thread.daemon = True

# starting server thread
server_thread.start()
print "Messenger server running on IP: "+ip+" PORT: "+str(serverAddr[1]) 
server_thread.join()
server.shutdown()
server.server_close()