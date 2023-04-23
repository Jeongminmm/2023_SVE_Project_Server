# 2023_SVE_Project_Server

## ROS_TO_SERVER
### 흐름

Ros → Kafka → 인포메이션 시스템

### 스마트폰에서 로버 실시간 위치 수신

- Kafka Topic

```jsx
{
	"state" : "called", // called : 호출되어 이동중, wait : 대기 주행 중, stop : 주행 불가 상태
										// called 일때는 호출 불가, wait 일때는 호출 가능, stop일때는 호출 불가
	"is_move" : "moving", // moving : 움직이는 중, stop : 멈춤 상태 
	"lat" : 위도(double),
	"lng" : 경도(double),
	"goal" : "EngA", //EngA , Chungsim, None(호출 대기중) 둘 중 하나
}
```

## SERVER_TO_ROS
### 흐름

인포메이션 시스템 → Kafka → ROS 

### 스마트폰에서 로버 호출 토픽

- Kafka Topic
    
    ```jsx
    {
    	"mode" : "Onsite" //Onsite : 현장구매 요청 , Online : 호출 구매 요청
    	"location" : "EngA" // EngA : 공대 a동 앞, Chungsim : 청심대 앞, None:현장구매
    }
    ```
