import socket
import os
import hashlib

serverIP = '127.0.0.1'
serverPort = 3333

def make_checksum(data): #checksum을 생성하는 함수
	checksum = hashlib.sha1() #160bit 해시 암호
	checksum.update(data)
	return checksum

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP통신

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

window=[0,0,0,0] #window 초기설정(size = 4)
seqNum = 0 #초기설정(초기 seqNum는 0으로 설정)
ACK = seqNum #ACK은 seqNum과 동일

bSeqNum = seqNum << 4 #4bit
ACK = ACK & 0b1111 #4bit

total_data = (bSeqNum|ACK).to_bytes(1,byteorder = "big") + file_name.encode() + file_size.to_bytes(4,byteorder = "big")

#checksum 생성
checksum = make_checksum(total_data)

#sending
window[0] = checksum.digest()+total_data
clnt_sock.sendto(window[0], (serverIP, serverPort))
prev_seqNum = seqNum

#파일 데이터 읽어서 보내기
print("Start File send")
current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수
send_count = 1 #오류검사를 하기 위한 변수

for i in range(3): #처음 4개의 데이터는 연속으로 보냄
	send_data = file.read(1024) #파일을 읽음
	
	send_count+=1

	seqNum = seqNum+1 #seqNum update
	seqNum = seqNum % 8 #0~7사이의 seqNum이 나오게 함
	ACK = seqNum #ACK은 seqNum과 동일

	bSeqNum = seqNum << 4 #4bit
	ACK = ACK & 0b1111 #4bit

	send_message = (bSeqNum|ACK).to_bytes(1,byteorder = "big") + send_data
				
	#checksum 생성
	checksum = make_checksum(send_message)

	#sending
	window[i+1] = checksum.digest()+send_message
	clnt_sock.sendto(window[i+1], (serverIP, serverPort))

	current_size += len(send_data)

	resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
	print(resend_message)

	prev_seqNum = seqNum

prev_ACK = 0 #초기값 설정
while True:
	if current_size == file_size: #마지막 검사
		while True:
			if (seqNum+1)%8 == recv_ACK: #종료조건 
				break
			response = clnt_sock.recv(1)[0]
			recv_ACK = response & 15
			recv_seqNum = response >> 4
		break

	response = clnt_sock.recv(1)[0]
	recv_ACK = response & 15
	recv_seqNum = response >> 4

	if recv_ACK == 15: #NAK
		print("* Received NAK - Retransmit!")
		#recv_seqNum 프레임부터 window에 있는 4개의 frame 보내줌
		for i in range(4):
			clnt_sock.sendto(window[(recv_seqNum-1+i)%4], (serverIP, serverPort))
	
		print("* window[0,1,2,3] transmit clear!")
		resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
		print(resend_message)
		print("============================================")

	else: #ACK
		if recv_ACK == 0:
			cal_ACK = 8
		else:
			cal_ACK = recv_ACK
	
		for i in range(cal_ACK - prev_ACK):
			current_window = (prev_ACK) % 4	
			send_data = file.read(1024) #파일을 읽음
	
			send_count += 1

			seqNum = seqNum+1 #seqNum update
			seqNum = seqNum % 8 #0~7사이의 seqNum이 나오게 함
			ACK = seqNum #ACK은 seqNum과 동일
			bSeqNum = seqNum << 4 #4bit
			ACK = ACK & 0b1111 #4bit
	
			send_message = (bSeqNum|ACK).to_bytes(1,byteorder = "big") + send_data

			#checksum 생성
			checksum = make_checksum(send_message)
	
			#sending
			window[current_window] = checksum.digest()+send_message
			
			if (send_count == 10) or (send_count == 20): #checksum error 검사하기 위함(잘못된 checksum으로 변경)
				clnt_sock.sendto((window[current_window][0:19]+("A").encode()+window[current_window][20:]), (serverIP, serverPort))

			else:
				clnt_sock.sendto(window[current_window], (serverIP, serverPort))
			
			current_size += len(send_data)
			resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
			print(resend_message)

			prev_seqNum = recv_seqNum
			prev_ACK = (prev_ACK+1)%8

file.close() #파일 닫아줌
clnt_sock.close() #socket닫아줌
print("File send end.")
