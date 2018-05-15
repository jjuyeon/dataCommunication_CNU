import socket
import struct
import os
import hashlib
import time

ip_address = '127.0.0.1'
port_number = 3333

def make_checksum(data): #checksum을 생성하는 함수
	checksum = hashlib.sha1() #160bit 해시 암호
	checksum.update(data)
	return checksum

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))

print("Server socket open...")
print("Send file info ACK..")

while True:
	data,addr = server_sock.recvfrom(1045)
	output_checksum = data[0:20] #받은 암호 저장
	output_data = data[20:]

	#받은 데이터 checksum 생성
	data_checksum = make_checksum(output_data)

	output_seqNum = output_data[0]
	if (output_checksum == data_checksum.digest()) and (output_seqNum == 0): #정상전송
		file_name = output_data[1:12].decode()
		file_size = struct.unpack("!I",output_data[12:16])[0]
		file_path = "./received_dir/"
		
		if not os.path.isdir("received_dir/"): #디렉토리 유무 확인
			print("received_dir 디렉토리가 없으므로 생성합니다.")
			os.mkdir("received_dir/") #없으면 생성

		file = open(file_path+file_name,"wb")

		print("File Name = ",file_name)
		print("File Size = ",file_size)
		print("received file Path = ",file_path+file_name)

		if output_seqNum % 2 == 0:
			ACK=1
		elif output_seqNum % 2 == 1:
			ACK=0
		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr)
		prev_seqNum = output_seqNum #seqNum검사 위해 저장
		break #정확한 정보를 받으면 종료
	
	elif output_seqNum == 1: #seqNum 잘못된 경우:ACK전송 + packet discard
		if output_seqNum % 2 == 0:
			ACK=1
		elif output_seqNum % 2 == 1:
			ACK=0
		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr)

	elif output_checksum != data_checksum.digest(): #checksum 잘못된 경우:NAK전송
		print("* Packet corrupted!! *** - Send To Sender NAK(2)")
		NAK=2
		server_sock.sendto(NAK.to_bytes(1,byteorder="big"), addr)

#파일 데이터 받기
current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수
receive_count = 0 #오류검사를 하기 위한 변수
while True:
	total_message,addr = server_sock.recvfrom(1045)
	output_checksum = total_message[0:20] #checksum
	output_seqNum = total_message[20]
	output_message = total_message[21:]

	#받은 데이터 checksum 생성
	data_checksum = make_checksum(total_message[20:])

	if(output_checksum == data_checksum.digest()) and (prev_seqNum != output_seqNum): #정상전송
		#파일 쓰기 시작
		file.write(output_message)
		current_size += len(output_message)
		receive_count += 1 #파일을 몇번 receive하는지 저장

		if (receive_count == 20) or (receive_count == 25):#timeout error 검사하기 위함 (20번째,25번째 전송일 때 검사)
			print("wait for 5...")
			time.sleep(5)

		resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
		print(resend_message)
		
		if output_seqNum % 2 == 0:
			ACK=1
		elif output_seqNum % 2 == 1:
			ACK=0

		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr) #ACK전송
		prev_seqNum = output_seqNum

	elif prev_seqNum == output_seqNum: #seqNum 잘못된 경우:ACK전송 + packet discard
		if output_seqNum % 2 == 0:
			ACK=1
		elif output_seqNum % 2 == 1:
			ACK=0

		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr)
	
	elif output_checksum != data_checksum.digest(): #checksum 잘못된 경우:NAK전송
		print("* Packet corrupted!! *** - Send To Sender NAK(2)")
		NAK = 2
		server_sock.sendto(NAK.to_bytes(1,byteorder="big"), addr)

	if current_size==file_size : #종료조건
		break

file.close()
server_sock.close()
print("File receive end.")
