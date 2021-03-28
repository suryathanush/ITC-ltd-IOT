import random
import time
from paho.mqtt import client as mqtt_client
import csv
import string
from datetime import datetime


#__________________________GLOBAL VARIABLES_____________________________________________________________________________________________

broker = '103.10.133.104'   #------------------------ IP Address of server
port = 8081            #------------------------ port number to access server
topic = "live_data"          #------------------------ MQTT topic to be published
client_id = 'python-mqtt_data' #----------------- client-ID of code
username = 'surya'    #------------------------ MQTT username
password = 'Mqtt@itc'  #------------------------ MQTT password

Connect_Status = False #------------------------ Flag which sets "True" when connected
prev_time = 0          #------------------------ valriable to store disconnected time 
#__________________________________________________________________________________________________

#-----------------------FUNCTION TO BEE CALLED WHEN DISCONNECTED------------------------------------------------------------------------
   #--(funtion argumeents : bool (True/False))
   #-- whenever disconnected , store the live data into csv file -----
def Call_On_Disconnect(state):
    if(not state):
        with open('/home/surya/Downloads/IOT-standalone/client_side/cache.csv', 'a') as f_object:
            writer_object = csv.writer(f_object)
            writer_object.writerow([client_id, i, datetime.now(), val])
            f_object.close()
#----------------------------------------------------------------------------------------------------------------------------------------


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
            global prev_time        #------------when not connected store the time in prev_time
            prev_time = time.time()
    #--------------------------------------------------------------------------

    #------on_disconnect() function to be called when disconnected ------------
    def on_disconnect(client, userdata, rc):
        print("client disconnected")
        global Connect_Status
        Connect_Status = False
        global prev_time
        prev_time = time.time()
        #print(prev_time)
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


#------------------------ FUNCTIO TO PUBLISH DATA TO SERVER ----------------------------------------------------------------------------
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


#--------------------------- MAIN FUNCTION WHERE IMAGE PROCESSING RUNS ---------------------------------------------------------------
i1 = 0
i = i1
def main_func():
    '''
    .
    .
    MAIN FUNCTION WHERE IMAGE PROCESSING CODE RESITES
    .
    .
    .
    '''
    global i
    global i1
    global val
    val = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)) #---generate random string
    i1 = i
    i+=1
#------------------------------------------------------------------------------------------------------------------------------------


#---------------------- run() function to execute the whole in loop -----------------------------------------------------------------
def run():
    while(1):
        try:
            client = connect_mqtt()
            client.loop_start()
            while(1):
                global prev_time
                #----if disconnected for more than 10sec then restart the connection-----------
                if(((time.time()-prev_time)>10)&(not Connect_Status)):
                    prev_time = time.time()
                    client.loop_stop()
                    client = connect_mqtt()
                    client.loop_start()
                main_func()
                publish(client, client_id, i, datetime.now(), val)
                if(Connect_Status):
                    print("published : %s"%i)
                else:
                    print("failed to publish : %s"%i)
                Call_On_Disconnect(Connect_Status)
                time.sleep(1)
                print("-------------------------")
        except Exception as e:
            print(Connect_Status)
            print(e)
            print(i)
            main_func()
            Call_On_Disconnect(False)
        time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    run()