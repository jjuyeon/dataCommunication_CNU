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

while True:
	data,addr = server_sock.recvfrom(1045)
	recv_checksum = data[0:20] #받은 암호 저장
	recv_data = data[20:]

	#받은 데이터 checksum 생성
	data_checksum = hashlib.sha1() #160bit 해시 암호
	data_checksum.update(recv_data)
	
	seqNum = recv_data[0]
	if (recv_checksum == data_checksum.digest()) and (seqNum == 0):
		file_name = recv_data[1:12].decode()
		file_size = struct.unpack("!I",recv_data[12:16])[0]
		print("File Name = ",file_name)
		print("File Size = ",file_size)

		if seqNum % 2 == 0:
			ACK=1
		elif seqNum % 2 == 1:
			ACK=0
		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr)
		prev_seqNum = seqNum #seqNum검사 위해 저장
		break #정확한 정보를 받으면 종료
	
	#elif seqNum == 1: #seqNum 잘못된 경우:NAK전송 (다음주구현)
	#elif recv_checksum != data_checksum.digest(): #checksum 잘못된 경우:NAK전송 (다음주구현)

#파일 데이터 받기	
output_path = "./received_dir/"

if not os.path.isdir("received_dir/"): #디렉토리 유무 확인
	print("received_dir 디렉토리가 없으므로 생성합니다.")
	os.mkdir("received_dir/") #없으면 생성

file = open(output_path+file_name,"wb")
current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수

while True:
	total_message,addr = server_sock.recvfrom(1045)
	output_checksum = total_message[0:20] #checksum
	output_seqNum = total_message[20]
	output_message = total_message[21:]

	#받은 데이터 checksum 생성
	data_checksum = hashlib.sha1() #160bit 해시 암호
	data_checksum.update(total_message[20:])
	
	if(output_checksum == data_checksum.digest()) and (prev_seqNum != output_seqNum):
		#파일 쓰기 시작
		file.write(output_message)
		current_size += len(output_message)
		resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(file_size)+ " , "+  str(round(100 * (current_size / file_size), 3))+ " %"
		print(resend_message)
		
		if output_seqNum % 2 == 0:
			ACK=1
		elif output_seqNum % 2 == 1:
			ACK=0
		server_sock.sendto(ACK.to_bytes(1,byteorder="big"), addr) 
		prev_seqNum = output_seqNum
		
	#elif prev_seqNum == output_seqNum: #seqNum 잘못된 경우:NAK전송 (다음주구현)
	#elif output_checksum != data_checksum.digest(): #checksum 잘못된 경우:NAK전송 (다음주구현)
	
	if current_size==file_size : #종료조건
		break

file.close()
server_sock.close()
