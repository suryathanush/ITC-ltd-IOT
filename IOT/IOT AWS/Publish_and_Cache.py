

import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import csv

#flag changes to 1 when connection is interrupted
class timeflag:
    flag=0


parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
#If not using command line enter endpoint details after default=""
parser.add_argument('--endpoint',default="a1d31vc1xczakc-ats.iot.us-west-2.amazonaws.com")
#If not using command line enter path to device certicate after default =
parser.add_argument('--cert',default="device.pem.crt")
#If not using command line enter path to private key after default =
parser.add_argument('--key',default="private.pem.key")
# If not using command line enter path to Root certificate after default =
parser.add_argument('--root-ca',default="Amazon-root-CA-1.pem")
#If you want to make a custom client ID please change after default = or enter thru command line
parser.add_argument('--client-id', default="test-" + str(uuid4()))
#If not using command line enter topic after default =
parser.add_argument('--topic', default="test/topic")
#If not using command line enter count after default =""
parser.add_argument('--count', default=10, type=int)
#parser.add_argument('--message', default="Hello World!") #This line of code can be activated to send message via command line
#Arguements below these need to be considered if an only if we connect with mqtt via websockets
parser.add_argument('--use-websocket', default=False, action='store_true')
parser.add_argument('--signing-region', default='us-east-1')
parser.add_argument('--proxy-host')
parser.add_argument('--proxy-port', type=int, default=8080)
parser.add_argument('--verbosity', choices=[x.name for x in io.LogLevel], default=io.LogLevel.NoLogs.name,)


# Using globals to simplify sample code
args = parser.parse_args()

io.init_logging(getattr(io.LogLevel, args.verbosity), 'stderr')


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))
    timeflag.flag=1



# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))
    timeflag.flag=0





if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    if args.use_websocket == True:
        proxy_options = None
        if (args.proxy_host):
            proxy_options = http.HttpProxyOptions(host_name=args.proxy_host, port=args.proxy_port)

        credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
        mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            endpoint=args.endpoint,
            client_bootstrap=client_bootstrap,
            region=args.signing_region,
            credentials_provider=credentials_provider,
            websocket_proxy_options=proxy_options,
            ca_filepath=args.root_ca,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=args.client_id,
            clean_session=False,
            keep_alive_secs=6)

    else:
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=args.endpoint,
            cert_filepath=args.cert,
            pri_key_filepath=args.key,
            client_bootstrap=client_bootstrap,
            ca_filepath=args.root_ca,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=args.client_id,
            clean_session=False,
            keep_alive_secs=6)

    print("Connecting to {} with client ID '{}'...".format(
        args.endpoint, args.client_id))

    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")
    message="Sample" #Equate message to function that recieves sensor data

    if args.count == 0:
        print ("Sending messages until program killed")
    else:
        print ("Sending {} message(s)".format(args.count))

    publish_count = 1
    while (publish_count <= args.count ) or (args.count == 0):
        if(timeflag.flag==0):

            print("Publishing message to topic")
            mqtt_connection.publish(
                topic=args.topic,
                payload=message,
                qos=mqtt.QoS.AT_LEAST_ONCE)

        else:
            print("Waiting for connection")
            cachefile=open('cache.csv',"a",newline="")
            cache=csv.writer(cachefile)
            cache.writerow([message])
            cachefile.close()

        publish_count += 1
        time.sleep(1)


    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
