# Go-back-n 구현
슬라이딩 윈도우 흐름제어 기법<br>
Sender에서 프레임을 window크기만큼 전송하면 Receiver에서 오류 점검 <br>
모든 프레임에 대한 ACK검사 진행할 필요 없음 : ACK2를 받으면 프레임1까지 전송이 잘 되었다고 보장<br>
에러(타임아웃, 프레임 손실, 손상) 발생시 해당 프레임 이후로 모든 프레임을 재전송 <br>

## 요구사항

* Receiver 요구사항
	* Receiver의 sliding window 크기는 1
	-체크섬 검사 (일치 -> seqNum확인 후 ACK전송, 불일치 -> NAK전송)
	+ 순서가 뒤바뀐 프레임 수신 : ACK은 전송 & 받은 프레임은 Discard

- Sender 요구사항
	* Window Size = 4 -> seqNum : 0~7
		* 4개의 프레임 연속 전송
	- ACK 수신
		* ACK 넘버 확인하여 전송 완료된 프레임 수를 확인
		- 전송 완료된 프레임 수만큼 새로운 프레임 전송
	+ NAK 수신 : SeqNum 확인 후, 해당 프레임부터 재전송(Window size만큼 프레임 연속 전송)
	+ 타임아웃 발생 : 타임아웃이 발생한 프레임 확인, 해당 프레임부터 재전송(Window size만큼 프레임 연속 전송)
