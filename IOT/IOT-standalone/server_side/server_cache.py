
import random
import time
import demjson
from paho.mqtt import client as mqtt_client

import mysql.connector

#---------------connect to mysql database--------------------------------------------------------------------------------------------
mydb = mysql.connector.connect(
    user='surya',
    password='Mysql@1234',
    host='localhost',
    port=3306,
    database='itc-iot-log',
    auth_plugin='mysql_native_password'
    )

mycursor = mydb.cursor()
sqlformula = "INSERT INTO CACHE_DATA (CLIENT_ID, SERIAL_NO, TIME, VALUE) VALUE (%s, %s, %s, %s)"
#-----------------------------------------------------------------------------------------------------------------------------------


#__________________________GLOBAL VARIABLES_____________________________________________________________________________________________

broker = 'localhost'   #------------------------ IP Address of server
port = 1883            #------------------------ port number to access server
topic = "cache_data"          #------------------------ MQTT topic to be published
client_id = 'python-mqtt_sub_cache' #----------------- client-ID of code
username = 'surya'    #------------------------ MQTT username
password = 'Mqtt@itc'  #------------------------ MQTT password
#_______________________________________________________________________________________________________________________________________


#-----------------------FUNCTION TO CONNECT TO MQTT SERVER--------------------------------------------------------------------------------
def connect_mqtt():
    #------on_connect() function to be called when connected------------------
    def on_connect(client, userdata, flags, rc):
        if rc == 0:    #---------------------- --RETURN CODE: 0 means connected, Turn Connect_Status to "True"
            print("Connected to Surya's MQTT!")
        else:
            print("Failed to connect, return code %d\n", rc)
    #--------------------------------------------------------------------------

    #------on_disconnect() function to be called when disconnected ------------
    def on_disconnect(client, userdata, rc):
        print("client disconnected")
        if rc == 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
        else:
            print("Failed to connect, return code %d, auto-reconnecting"%rc)  
        run()              
    #---------------------------------------------------------------------------

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)

    # declare the functions to be called on connection and disconnection
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(broker, port)
    return client
#--------------------------------------------------------------------------------------------------------------------------------------


#----------------------------SUBSCRIBER CODE(also apends subscribed data to database)---------------------------------------------------
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = demjson.decode(str(msg.payload.decode()))   #----------------decode the message from utf-8 encoding
        data = (message['client_id'], message['serial_no'], message['time'], message['value'])
        while(1):
            try:
                mycursor.execute(sqlformula, data)
                mydb.commit()
                print("appended to database")
                print(".............................")
                break
            except:
                print("error appending..trying again")    
    client.subscribe(topic)
    client.on_message = on_message
#---------------------------------------------------------------------------------------------------------------------------------------


#---------------------- run() function to execute the whole in loop --------------------------------------------------------------------
def run():
    while(1):
        try:
            client = connect_mqtt()
            subscribe(client)
            client.loop_forever()
        except Exception as e:
            print(e)
        time.sleep(1)        
#----------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    run()
