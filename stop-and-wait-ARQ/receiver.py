import socket
import struct
import os
import hashlib

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))

print("Server socket open...")
print("Send file info ACK..")

data,addr = server_sock.recvfrom(5000)
recv_checksum = data[0:20] #받은 암호 저장
recv_data = data[20:]
print(recv_checksum)
print(recv_data) #check

#받은 데이터 checksum 생성
data_checksum = hashlib.sha1() #160bit 해시 암호
data_checksum.update(recv_data)
print(data_checksum.digest())

if recv_checksum == data_checksum.digest() :
	seqNum = data[20]
	file_name = data[21:32].decode()
	file_size = struct.unpack("!I",data[32:36])[0]
	print(seqNum)
	print(file_name)
	print(file_size)
	ACK='1'
	server_sock.sendto(ACK.encode(), addr) #수정





