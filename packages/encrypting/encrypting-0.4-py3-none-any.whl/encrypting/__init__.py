from random import getrandbits
from hashlib import sha256

def generate_pair(root_len=16, prime_len=1024):
	return getrandbits(root_len), getrandbits(prime_len)

class Encrypt:
	def __init__(self, pair, secret_len=256):
		self.root, self.prime = pair

		self.dh_secret = getrandbits(secret_len)
		self.mixture = pow(self.root, self.dh_secret, self.prime)

	def init(self, mixture):
		self.key = pow(mixture, self.dh_secret, self.prime)
		self.hkey = sha256(str(self.key).encode()).digest()

	def crypt(self, data):
		return bytes([data[x] ^ self.hkey[x % 32] for x in range(len(data))])

from socket import socket
from json import dumps, loads
from threading import Thread

class EncryptedSocket:
	def __init__(self, socket_args={}, root_len=16, prime_len=1024):
		self.socket = socket(**socket_args)
		self.root_len = root_len
		self.prime_len = prime_len

	def connect(self, addr):
		self.socket.connect((addr))

		data = loads(self.socket.recv(1024).decode())

		encrypt = Encrypt((data['root'], data['prime']))
		encrypt.init(data['mixture'])

		self.socket.send(dumps({'mixture': encrypt.mixture}).encode())

		return EncryptedClient(self.socket, encrypt)

	def serve(self, bind_addr, handler):
		self.socket.bind(bind_addr)
		while True:
			self.socket.listen()
			clSock, clAddr = self.socket.accept()
			Thread(target=self.server_thread, args=(clSock, clAddr, handler)).start()

	def server_thread(self, clSock, clAddr, handler):
		pair = generate_pair(self.root_len, self.prime_len)
		encrypt = Encrypt(pair)

		payload = dumps({'root': pair[0], 'prime': pair[1], 'mixture': encrypt.mixture}).encode()
		clSock.send(payload)

		data = clSock.recv(1024).decode()
		mixture = loads(data)['mixture']

		encrypt.init(mixture)

		handler(EncryptedClient(clSock, encrypt), clAddr)
		clSock.close()

		exit()


class EncryptedClient:
	def __init__(self, client_socket, encrypt):
		self.socket = client_socket
		self.encrypt = encrypt

	def send(self, data):
		enc = self.encrypt.crypt(data)
		self.socket.send(enc)

	def recv(self, num):
		data = self.socket.recv(num)
		return self.encrypt.crypt(data)

	def close(self):
		self.socket.close()