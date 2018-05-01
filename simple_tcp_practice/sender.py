import socket
import struct
import os

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP, serverPort))

print("Connect to Server...")
print("Receiver IP = ",serverIP)
print("Receiver Port = ",serverPort)

file_name = input("Input File Name : ")
input_type = 0 #메시지 타입, 파일 정보(파일명, 파일 크기)를 전송할 때
file_size = os.path.getsize(file_name) 

input_message = input_type.to_bytes(1,byteorder = "big") + file_name.encode() + file_size.to_bytes(4,byteorder = "big")
clnt_sock.send(input_message)
clnt_sock.recv(1024)



input_type = 1 #데이터를 전송할 때
# file open for read
file = open("./"+file_name, "rb")
while True:
	input_data = file.read(1024) #파일을 읽음
	if not input_data : #종료조건
		break
	send_message = input_type.to_bytes(1,byteorder = "big") + input_data
	clnt_sock.send(send_message)
	print((clnt_sock.recv(1024)).decode('utf-8'))


file.close() #파일 닫아줌
clnt_sock.close() #socket닫아줌
print("File send end")
