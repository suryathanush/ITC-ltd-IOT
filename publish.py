#Open Terminal, Enter the following command to clone the “AWS IoT Python SDK” from GitHub.
#     git clone https://github.com/aws/aws-iot-device-sdk-python
#This Should create the following directory in Filesystem.
#      "aws-iot-device-sdk-python"

#Now Enter the following the command to install the SDK
#     "sudo python setup.py install"( for linux)   "python setup.py install"( for windows)

#That’s it, AWS IoT Python SDK is successfully installed.



import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


myMQTTClient = AWSIoTMQTTClient("pcClientID")
myMQTTClient.configureEndpoint("a1d31vc1xczakc-ats.iot.us-east-2.amazonaws.com", 8883)

myMQTTClient.configureCredentials("C:/Users/surya/Downloads/AmazonRootCA1.pem", "C:/Users/athma/Downloads/10a100330b-private.pem.key", "C:/Users/athma/Downloads/10a100330b-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer')
myMQTTClient.connect()

while True:
    myMQTTClient.publish(
    topic="<topic_name>",
    QoS=1,
    payload='{"message_name":"'<messsage in string format>'"}')

