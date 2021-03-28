from paho.mqtt import client as mqtt_client
import csv
import time

#__________________________GLOBAL VARIABLES_____________________________________________________________________________________________

broker = '103.10.133.104'   #------------------------ IP Address of server
port = 8081            #------------------------ port number to access server
topic = "cache_data"          #------------------------ MQTT topic to be published
client_id = 'python-mqtt_cache' #----------------- client-ID of code
username = 'surya'    #------------------------ MQTT username
password = 'Mqtt@itc'  #------------------------ MQTT password

Connect_Status = False #------------------------ Flag which sets "True" when connected
#_______________________________________________________________________________________________________________________________________


#-----------------------FUNCTION TO CONNECT TO MQTT SERVER--------------------------------------------------------------------------------
def connect_mqtt():
    #------on_connect() function to be called when connected------------------
    def on_connect(client, userdata, flags, rc):
        global Connect_Status
        if rc == 0:    #---------------------- --RETURN CODE: 0 means connected, Turn Connect_Status to "True"
            print("Connected to Surya's MQTT!")
            Connect_Status = True
        else:
            print("Failed to connect, return code %d\n", rc)
            Connect_Status = False
    #--------------------------------------------------------------------------

    #------on_disconnect() function to be called when disconnected ------------
    def on_disconnect(client, userdata, rc):
        print("client disconnected")
        global Connect_Status
        Connect_Status = False
        if rc == 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
        else:
            print("Failed to connect, return code %d, auto-reconnecting"%rc)                
    #---------------------------------------------------------------------------

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)

    # declare the functions to be called on connection and disconnection
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(broker, port)
    return client
#--------------------------------------------------------------------------------------------------------------------------------------


#------------------------ FUNCTION TO PUBLISH DATA TO SERVER ----------------------------------------------------------------------------
def publish(client, client_ID, Serial_no, Time_stamp, Rand_str):
    #print(msg)
    msg = "{'client_id': '%s', 'serial_no': '%s', 'time': '%s', 'value': '%s'}"%(client_ID, Serial_no, Time_stamp, Rand_str)
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    for count in range(0,10):   #------if failed to publish, retry upto 10 times
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
            break
        else:
            print(f"Failed to send message to topic {topic}")
            result = client.publish(topic, str(msg))
            status = result[0]
#-------------------------------------------------------------------------------------------------------------------------------------


#---------------------- run() function to execute the whole in loop -----------------------------------------------------------------
def run():
    global row_count  #----------- variable to store the index of last published row
    row_count = 0
    while(1):
        try:
            time.sleep(1)
            client = connect_mqtt()
            client.loop_start()
            file = open("/home/surya/Downloads/mqtt-iot/client_side/cache.csv", "r")
            file_content = file.read()
            file.close()
            #---------------Start publishing if cache file is not empty and connected to server------
            if(Connect_Status & (not file_content=="")):
                with open('/home/surya/Downloads/mqtt-iot/client_side/cache.csv', 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    #-----------continue from where it stopped to publish----------------------
                    for i in range(row_count):
                        next(csvreader)
                    for row in csvreader:
                        #----------if connected, publish the row and increment row_count------
                        if(Connect_Status):
                            publish(client, row[0], row[1], row[2], row[3])
                            row_count += 1

                        #----------if disconnected, try restarting the connection----------
                        else:
                            client.loop_stop()
                            client = connect_mqtt()
                            client.loop_start()
                            break
                
                #-----------if whole csv data is published, empty the file----------------
                with open('/home/surya/Downloads/mqtt-iot/client_side/cache.csv', 'w') as csvfile:
                    csvfile.truncate()
            else:
                client.loop_stop()

        except Exception as e:
            print(e)
        time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    run()        
