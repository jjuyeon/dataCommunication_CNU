# 파일 전송 프로그램 구현
<br>
a. 프로토콜 TCP
<br>
b. 파일 전송 방향 : 클라이언트(sender.py) -> 서버(receiver.py)
<br>
c. sender 프로그램에서 사용자는 저농할 파일의 이름을 입력
<br>
d. 파일 수신 폴더를 별도로 만들어 지정된 포맷으로 메시지 전송
<br>
f. 전송 시 보내는 파일 데이터 크기 : 1024 바이트
<br><br>
# 메시지 포맷:
Type(1 byte), File Name(11 byte), File Size(4 byte), Data(1024 byte)
