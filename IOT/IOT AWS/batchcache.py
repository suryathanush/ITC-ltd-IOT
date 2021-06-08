import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from datetime import datetime
import sys
import threading
import time
from uuid import uuid4
import csv
import os
import json
import boto3
import multiprocessing

#flag changes to 1 when connection is interrupted
class timeflag:
    flag=0


cache = []


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
    timeflag.flag=2


def publisher(message):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    rcontent={}
    rcontent["timestamp"]=current_time
    rcontent["message"]=message
    acontent=json.dumps(rcontent)
    print(rcontent)
    mqtt_connection.publish(
    topic=args.topic,
    payload=acontent,
    qos=mqtt.QoS.AT_LEAST_ONCE)


def func1(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=0
        length=len(cache)
        while (x<length) and (x<5000):
            batch.put_item(Item={"timestamp":str(x),"message":x})
            x=x+1

def func2(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=5000
        length=len(cache)
        while (x<length) and (x<10000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func3(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=10000
        length=len(cache)
        while (x<length) and (x<15000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func4(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=15000
        length=len(cache)
        while (x<length) and (x<20000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func5(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=20000
        length=len(cache)
        while (x<length) and (x<=25000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1
def func6(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=25000
        length=len(cache)
        while(x<length) and (x<30000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func7(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=30000
        length=len(cache)
        while(x<length) and (x<35000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func8(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=35000
        length=len(cache)
        while (x<length) and (x<40000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func9(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=40000
        length=len(cache)
        while (x<length) and (x<45000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func10(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=45000
        length=len(cache)
        while (x<length) and (x<=50000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1
def func11(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=50000
        length=len(cache)
        while (x<length) and (x<55000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func12(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=55000
        length=len(cache)
        while (x<length) and (x<60000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func13(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=60000
        length=len(cache)
        while (x<length) and (x<65000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func14(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=65000
        length=len(cache)
        while (x<length) and (x<70000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func15(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=70000
        length=len(cache)
        while (x<length) and (x<=75000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1
def func16(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=75000
        length=len(cache)
        while (x<length) and (x<80000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func17(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=80000
        length=len(cache)
        while (x<length) and (x<85000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func18 (cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=85000
        length=len(cache)
        while (x<length) and (x<90000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func19(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=90000
        length=len(cache)
        while (x<length) and (x<95000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1

def func20(cache):
    dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
    table=dynamodb.Table("testing")
    with table.batch_writer() as batch:
        x=95000
        length=len(cache)
        while (x<length) and (x<=100000):
            batch.put_item(Item={"timestamp":str(x),"message":cache[x]})
            x=x+1
def func21(message):
        dynamodb=boto3.resource('dynamodb','us-west-2',aws_access_key_id="AKIAQVUL54UDNWROYH6U",aws_secret_access_key="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")
        table=dynamodb.Table("testing")
        with table.batch_writer() as batch:
            x=100000
            while (x<=105000):
                batch.put_item(Item={"timestamp":str(x),"message":message})
                print("Parallely Writing")
                x=x+1


if __name__ == '__main__':
    # Spin up resources
    i=0
    for i in range(99995):
        cache.append(i)

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
     #Equate message to function that recieves sensor data

    if args.count == 0:
        print ("Sending messages until program killed")
        
    else:
        print ("Sending {} message(s)".format(args.count))

    publish_count = 1
    while (publish_count <= args.count ) or (args.count == 0):
        if(timeflag.flag==0) or (timeflag.flag==2):
            if(timeflag.flag==0):
                print("Normally Sending")
                message="Sample"
                publisher(message)
            else:
                print("clearing cache")
#                p0 = multiprocessing.Process(target=parallelpublisher)
#                p0.start()
                p1 = multiprocessing.Process(target=func1,args=(cache,))
                p1.start()
                p2 = multiprocessing.Process(target=func2,args=(cache,))
                p2.start()
                p3 = multiprocessing.Process(target=func3,args=(cache,))
                p3.start()
                p4 = multiprocessing.Process(target=func4,args=(cache,))
                p4.start()
                p5 = multiprocessing.Process(target=func5,args=(cache,))
                p5.start()
                p6 = multiprocessing.Process(target=func6,args=(cache,))
                p6.start()
                p7 = multiprocessing.Process(target=func7,args=(cache,))
                p7.start()
                p8 = multiprocessing.Process(target=func8,args=(cache,))
                p8.start()
                p9 = multiprocessing.Process(target=func9,args=(cache,))
                p9.start()
                p10 = multiprocessing.Process(target=func10,args=(cache,))
                p10.start()
                p11 = multiprocessing.Process(target=func11,args=(cache,))
                p11.start()
                p12 = multiprocessing.Process(target=func12,args=(cache,))
                p12.start()
                p13 = multiprocessing.Process(target=func13,args=(cache,))
                p13.start()
                p14 = multiprocessing.Process(target=func14,args=(cache,))
                p14.start()
                p15 = multiprocessing.Process(target=func15,args=(cache,))
                p15.start()
                p16 = multiprocessing.Process(target=func16,args=(cache,))
                p16.start()
                p17 = multiprocessing.Process(target=func17,args=(cache,))
                p17.start()
                p18 = multiprocessing.Process(target=func18,args=(cache,))
                p18.start()
                p19 = multiprocessing.Process(target=func19,args=(cache,))
                p19.start()
                p20 = multiprocessing.Process(target=func20,args=(cache,))
                p20.start()
                p21 = multiprocessing.Process(target=func21,args=("Sample",))
                p21.start()
                p1.join()
                p2.join()
                p3.join()
                p4.join()
                p5.join()
                p6.join()
                p7.join()
                p8.join()
                p9.join()
                p10.join()
                p11.join()
                p12.join()
                p13.join()
                p14.join()
                p15.join()
                p16.join()
                p17.join()
                p18.join()
                p19.join()
                p20.join()
                p21.join()
                timeflag.flag=0
                cache.clear()
        else:
            print("Waiting for connection")
            cache.append("Sample")

        publish_count += 1
        time.sleep(1)



    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
