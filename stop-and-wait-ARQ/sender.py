import socket
import struct
import os
import hashlib

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP통신

print("Sender Socket open.")
print("Receiver IP = ",serverIP)
print("Receiver Port = ", serverPort)
print("Send File Info(file Name, file Size, seqNum) to Server...")

#파일 정보(파일명,파일크기) 전송
file_name = "example.jpg"
file_size = os.path.getsize(file_name)
seqNum = 0

total_data = seqNum.to_bytes(4,byteorder = "big") + file_name.encode() + file_size.to_bytes(4,byteorder = "big")

#checksum 생성
checksum = hashlib.sha1() #160bit 해시 암호
checksum.update(total_data)

#sending
while True:
	send_message = checksum.digest()+total_data
	clnt_sock.sendto(send_message, (serverIP, serverPort))
	recv_ACK = clnt_sock.recv(1024).decode()
	print(recv_ACK)
	if recv_ACK == '1':
		break

