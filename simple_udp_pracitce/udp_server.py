import socket

ip_address = '127.0.0.1'
port_number = 8888

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address,port_number))

print("Server socket open...")
print("----------------------------------------------------")
print("Listening....")

data,addr = server_sock.recvfrom(5000)
decode_data = data.decode()
message_type = decode_data[0]
recv_message = decode_data[1:]
send_message=''

print("Type of Message : ",message_type)
print("Received Message from client : ",recv_message)

if message_type is '0':
	send_message = recv_message.upper()
elif message_type is '1':
	send_message = recv_message.lower()
elif message_type is '2':
	send_message = recv_message.swapcase()
elif message_type is '3':
	send_message = recv_message[::-1]
else :
	send_message = "타입을 잘못 입력하셨습니다. 다시 시도해주세요."

print("Converted Message : ",send_message)

server_sock.sendto(send_message.encode(),addr)
print("Send to Client Converted Message ....")
print("----------------------------------------------------")
server_sock.close()
