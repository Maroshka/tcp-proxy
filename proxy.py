import socket
import sys
import threading

def proxy_handler(client_sock, remote_host, remote_port, recieve_first):
	remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_sock.connect((remote_host, remote_port))

	if recieve_first:
		remote_buffer = recieve_from(remote_sock)
		if len(remote_buffer):
			# hexdump(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			print "Recieving from remotehost..."
			client_sock.send(remote_buffer)
			print "Sending to localhost..."

	while 1:

		local_buffer = recieve_from(client_sock)
		if len(local_buffer):
			# hexdump(local_buffer)
			local_buffer = request_handler(local_buffer)
			print "Recieving from localhost..."
			remote_sock.send(local_buffer)
			print "Sending to remotehost..."

		remote_buffer = recieve_from(remote_sock)
		if len(remote_buffer):
			# hexdump(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			print "Recieving from remotehost..."
			client_sock.send(remote_buffer)
			print "Sending to localhost..."

def recieve_from(sock):

	buff = ""
	sock.settimeout(10)
	try:
		while 1:
			data = sock.recv(4096)
			if not data:
				break
			buff +=data	 
	except:
		pass
	
	return buff



def response_handler(buff):
	# nothing special
	buff = 'He says: '+buff

	return buff

def request_handler(buff):
	# nothing special
	buff = buff.lower().replace('rm', 'ls')
	buff = buff.lower().replace('no', 'yes')
	buff = buff.lower().replace('yes', 'no')
	buff = 'She says: '+buff

	return buff

def srvLoop(local_host, local_port, remote_host, remote_port, recieve_first):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))
	except:
		print "Failed to listen to %s:%r" % (local_host, local_port)
		sys.exit(0)
	print "Listening to %s:%d ..." % (local_host, local_port)

	""" The server listens for connection, and when a connection request comes it, it hands it to the proxy,
	 which does the sending and recieving to either side of the data stream """

	server.listen(5)
	while 1:
		# client_sock is a new socket object, usable for recieving and sending data on the esablished connection
		client_sock, addr = server.accept()
		print ">>> Recieving incoming data from %s:%d ..." % (addr[0], addr[1])

		proxy_thrd = threading.Thread(target=proxy_handler, args = (client_sock, remote_host, remote_port, recive_first))
		proxy_thrd.start()

def main():
	if len(sys.argv[1:]) != 5:
		print "Usage: ./tcpProxy.py [local_host] [local_port] [remote_host] [remote_port] [recieve_first] \n"
		print "Example: ./tcpProxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
		sys.exit(0)
	rcvFirst = True if ("True" in sys.argv[5]) else False
	srvLoop(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), rcvFirst)

if __name__ == '__main__':
	main()