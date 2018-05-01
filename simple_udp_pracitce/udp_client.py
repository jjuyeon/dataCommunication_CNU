import socket

serverIP = '127.0.0.1'
serverPort = 8888

print("====================================================")
print("*	String Change Program")
print("====================================================")
print("* type = 0,1,2,3")
print("* if type == 0 : Change all letters to uppercase.")
print("* if type == 1 : Change all letters to lowercase.")
print("* if type == 2 : Change upper case to lower case and lower case to upper case.")
print("* if type == 3 : Change the sentence backwards.")
print("====================================================")

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
input_type = input("Input Type : ")

while len(input_type) is not 1:
	print("타입의 길이가 너무 깁니다. 다시 입력해주세요.")
	input_type = input("Input Type : ")
else: 
	input_message = input("Input your Message : ")
	client_msg = input_type + input_message

	clnt_sock.sendto(client_msg.encode(), (serverIP,serverPort))
	print("Send Message to Server..")
	print("ReceivedMessage from Server : ",(clnt_sock.recv(1024)).decode())

print("----------------------------------------------------")
