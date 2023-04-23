
import rospy
import json
import time
#gps
from sensor_msgs.msg import NavSatFix
#state
from geometry_msgs.msg import Pose  # state 토픽의 메시지 유형을 임포트합니다.
#pip install kafka-python
from kafka import KafkaProducer
#pip install jsonmerge
from jsonmerge import merge

Kafka_bootstrap_servers = 'IP:PORT'
# GPS 데이터와 State 데이터를 저장하는 변수
last_received_gps_data = None
last_received_state_data = None

# GPS 데이터를 받아 저장하는 콜백 함수
def gps_callback(data):
    global last_received_gps_data
    last_received_gps_data = {
        'lat': data.latitude,
        'lng': data.longitude
    }

# State 데이터를 받아 저장하는 콜백 함수
def state_callback(data):
    global last_received_state_data
    last_received_state_data = {
        'state' : data.called, #  called : 호출되어 이동중, wait : 대기 주행 중, stop : 주행 불가 상태
							# called 일때는 호출 불가, wait 일때는 호출 가능, stop일때는 호출 불가
        'is_move' : data.is_move, # moving : 움직이는 중, stop : 멈춤 상태 
        'goal' :  data.goal #EngA , Chungsim, None
    }

# GPS 및 State 데이터를 1초마다 Kafka로 전송하는 함수
def send_data_to_kafka():
    # Kafka Producer 생성
    producer = KafkaProducer(bootstrap_servers=Kafka_bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    while not rospy.is_shutdown():
        if last_received_gps_data is not None and last_received_state_data is not None:
            # GPS와 State 데이터를 결합
            combined_data = merge(last_received_gps_data,last_received_state_data)

            # Kafka topic에 데이터 전송
            producer.send('gps_and_state_topic', combined_data)
            producer.flush()

            rospy.loginfo('Sent GPS and State data to Kafka: %s', json.dumps(combined_data))

        # 1초마다 전송
        time.sleep(1)

def main():
    # 노드 초기화
    rospy.init_node('gps_and_state_to_kafka_node', anonymous=True)

    # GPS 및 State 토픽 구독
    rospy.Subscriber('/fix', NavSatFix, gps_callback)
    rospy.Subscriber('/state', Pose, state_callback)  # state 토픽 구독 추가

    # GPS 및 State 데이터를 1초마다 Kafka로 전송
    send_data_to_kafka()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass