import socket
import struct
import os

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening....")
server_sock.listen() #sender의 연결요청을 대기실로 보냄
client_sock,addr = server_sock.accept() #sender의 연결요청 수락

current_size = 0 #만들어지는 파일의 현재 상태 확인하기 위한 변수

while True:
	output_message = client_sock.recv(5000)
	if not output_message: #종료조건
		break

	output_type = output_message[0]
	output_path = "./received_dir/"
	
	if output_type == 0:
		output_name = output_message[1:12].decode()
		output_size = struct.unpack("!I",output_message[12:16])[0]
		print("File Name = ",output_name)
		print("File Size = ",output_size)
		print("File Path = ",output_path+output_name)
		file = open(output_path+output_name,"wb")
		client_sock.send("initial setting complete".encode())	

	elif output_type == 1:
		real_data = output_message[1:]
		file.write(real_data)

		current_size += len(real_data)
		resend_message = "(current size / total size) = "+ str(current_size)+ "/"+ str(output_size)+ " , "+  str(round(100 * (current_size / output_size), 3))+ " %"
		print(resend_message)
		client_sock.send(resend_message.encode())
		
	else: #예외처리 
		print("타입을 잘못입력하셨습니다. 다시 연결하세요.")
		break


file.close()
client_sock.close()
server_sock.close()
print("File receive end")
