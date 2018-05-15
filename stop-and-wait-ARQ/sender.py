import socket
import struct
import os
import hashlib

serverIP = '127.0.0.1'
serverPort = 3333

def make_checksum(data): #checksum을 생성하는 함수
	checksum = hashlib.sha1() #160bit 해시 암호
	checksum.update(data)
	return checksum

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP통신
clnt_sock.settimeout(3) #응답시간 제한 설정(3초)

print("Sender Socket open..")
print("Receiver IP = ",serverIP)
print("Receiver Port = ", serverPort)
print("Send File Info(file Name, file Size, seqNum) to Server...")

#파일 정보(파일명,파일크기) 전송 : 초기설정
file_name = "ex.jpg"

# file open for read
file = open("./"+file_name, "rb")

file_size = os.path.getsize(file_name) #파일 크기 구하기
file_name = file_name.ljust(11) #파일 이름을 11byte로 왼쪽정렬
seqNum = 0 #초기설정(초기 seqNum는 0으로 설정)

total_data = seqNum.to_bytes(1,byteorder = "big") + file_name.encode() + file_size.to_bytes(4,byteorder = "big")

#checksum 생성
checksum = make_checksum(total_data)

#sending
while True:
	clnt_sock.sendto(checksum.digest()+total_data, (serverIP, serverPort))
	current_response = clnt_sock.recv(1)[0]
	
	if current_response == 1:
		prev_response = current_response
		prev_seqNum = seqNum
		break

#파일 데이터 읽어서 보내기
print("Start File send")
current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수
send_count = 0 #오류검사를 하기 위한 변수

while True:
	try:
		if (current_response == 0) or (current_response == 1): #ACK일때 전송
			if current_response % 2 == 0:
				seqNum = 0
			elif current_response % 2 == 1: 
				seqNum = 1

			if (prev_seqNum != seqNum): #정상 전송
				send_data = file.read(1024) #파일을 읽음
				if not send_data: #종료조건
					break
				send_message = seqNum.to_bytes(1,byteorder="big") + send_data
				
				#checksum 생성
				checksum = make_checksum(send_message)
	
				if (send_count == 9) or (send_count == 14): #checksum error 검사하기 위함 (10, 15번째 전송일 때 검사)
					addError = "error"
					checksum = make_checksum(send_message + addError.encode())
	
				clnt_sock.sendto(checksum.digest()+send_message, (serverIP, serverPort))			
				send_count+=1 #파일을 몇번 send하는지 저장
				current_size += len(send_data)
				resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
				
				print(resend_message)
				prev_response = current_response
				prev_seqNum = seqNum
				current_response = clnt_sock.recv(1)[0]	

			elif (prev_response == current_response): #ACK받고 아무것도 하지않음 (empty)
				prev_response =current_response			
				current_response = clnt_sock.recv(1)[0]
				continue

		elif current_response == 2: #NAK일때 전송
			print("* Received NAK - Retransmit!")
			checksum = make_checksum(send_message) #checksum 다시 검사
			clnt_sock.sendto(checksum.digest()+send_message, (serverIP, serverPort)) #데이터 재전송
			print("Retransmission : "+resend_message)
			prev_response = current_response
			prev_seqNum = seqNum
			current_response = clnt_sock.recv(1)[0]
	
	except socket.timeout: #timeout 걸렸을 때
		print("* TimeOut!! **")
		clnt_sock.sendto(checksum.digest()+send_message, (serverIP, serverPort)) #데이터 재전송
		print("Retransmission : "+resend_message)
		prev_response = current_response
		prev_seqNum = seqNum
		current_response = clnt_sock.recv(1)[0]


file.close() #파일 닫아줌
clnt_sock.close() #socket닫아줌
print("File send end.")
