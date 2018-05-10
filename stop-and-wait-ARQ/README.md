# Stop-and-Wait 구현
Sender에서 프레임을 전송하면 Receiver에서 오류 점검

* Receiver
	* Sender가 보낸 프레임 수신 -> 응답(ACK/NAK) 전송
	- ACK전송 : 전상적인 데이터 수신할시 전송
	+ NAK전송 : 오류 발생시 전송

- Sender
	* Sequence Number, Checksum이 포함된 프레임 전송 -> 응답(ACK/NAK) 대기
	- ACK수신 : 다음 프레임 전송
	+ NAK수신 : 이전 프레임 재전송

## 요구사항

* Receiver 요구사항
	* 데이터를 수신하면 Checksum과 (Sequence Number + File Data)의 무결성 검사
	- Sequence Number를 확인하여 프레임의 순서 확인
	+ 일부 ACK 전송시 sleep을 걸어 타임아웃 발생 -> 타임아웃 처리 기능 테스트 목적

- Sender 요구사항
	* Sequence Number(1byte field) : 프레임 순서를 보장하기 위해 사용(0,1 번갈아가며 사용)
	- Checksum(20byte field) : 프레임의 무결성을 보장하기 위해 사용(Sequence Number+File Data를 해시 값으로 암호화)
	+ 프레임 전송 후 receiver로부터 응답 수신
	+ 타임아웃 발생시 데이터 재전송 -> 타임 아웃 시간은 3초로 지정함
	+ 일부 프레임 전송시 Checksum틀리게 보내기 -> 에러 처리 기능 테스트 목적 
