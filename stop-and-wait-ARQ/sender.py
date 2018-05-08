import socket
import struct
import os
import hashlib

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP통신

print("Sender Socket open..")
print("Receiver IP = ",serverIP)
print("Receiver Port = ", serverPort)
print("Send File Info(file Name, file Size, seqNum) to Server...")

#파일 정보(파일명,파일크기) 전송 : 초기설정
file_name = "ex.jpeg"

# file open for read
file = open("./"+file_name, "rb")

file_size = os.path.getsize(file_name) #파일 크기 구하기
file_name = file_name.ljust(11) #파일 이름을 11byte로 왼쪽정렬
seqNum = 0 #초기설정(초기 seqNum는 0으로 설정)

total_data = seqNum.to_bytes(1,byteorder = "big") + file_name.encode() + file_size.to_bytes(4,byteorder = "big")

#checksum 생성
checksum = hashlib.sha1() #160bit 해시 암호
checksum.update(total_data)

#sending
while True:
	send_message = checksum.digest()+total_data
	clnt_sock.sendto(send_message, (serverIP, serverPort))
	currentACK = clnt_sock.recv(1)[0]

	if currentACK == 1:
		prevACK = currentACK
		break

#파일 데이터 읽어서 보내기
print("Start File send")
current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수

while True:
	if currentACK % 2 == 0:
		seqNum = 0
	elif currentACK % 2 == 1:
		seqNum = 1

	send_data = file.read(1024) #파일을 읽음
	if not send_data : #종료조건
		break

	#checksum 생성
	checksum = hashlib.sha1() #160bit 해시 암호
	checksum.update(seqNum.to_bytes(1,byteorder="big") + send_data)

	send_message = checksum.digest()+seqNum.to_bytes(1,byteorder="big") + send_data
	clnt_sock.sendto(send_message, (serverIP, serverPort))
	
	current_size += len(send_data)
	resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
	print(resend_message)

	currentACK = clnt_sock.recv(1)[0]		
	prevACK = currentACK
	
	

file.close() #파일 닫아줌
clnt_sock.close() #socket닫아줌
