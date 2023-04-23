import rospy
import json
from kafka import KafkaConsumer
from std_msgs.msg import String

Kafka_bootstrap_servers = 'IP:PORT'
# Kafka에서 메시지를 수신하고 ROS 토픽으로 발행하는 함수
def kafka_to_ros():
    # Kafka Consumer 생성
    consumer = KafkaConsumer(
        'rover_call',
        bootstrap_servers=Kafka_bootstrap_servers,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    # ROS 노드 및 발행자 초기화
    rospy.init_node('kafka_to_ros_node', anonymous=True)
    pub = rospy.Publisher('rover_call_ros_topic', String, queue_size=10)

    # Kafka에서 메시지를 수신하고 ROS 토픽으로 발행
    for msg in consumer:
        if rospy.is_shutdown():
            break

        # 메시지를 JSON 문자열로 변환
        json_msg = json.dumps(msg.value)

        # ROS 메시지 생성 및 발행
        ros_msg = String(data=json_msg)
        pub.publish(ros_msg)

        rospy.loginfo('Received message from Kafka and published to ROS: %s', json_msg)

if __name__ == '__main__':
    try:
        kafka_to_ros()
    except rospy.ROSInterruptException:
        pass