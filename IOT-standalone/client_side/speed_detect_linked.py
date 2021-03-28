# USAGE
# python speed-detect.py -ff <first File> -nf <No of files to be processed>

# import the necessary packages
import pytesseract
import argparse
import cv2
import sys
import os
import time
import datetime
import csv
from paho.mqtt import client as mqtt_client


#__________________________GLOBAL VARIABLES_____________________________________________________________________________________________

broker = '103.10.133.104'   #---- -------------- IP Address of server
port = 8081            #------------------------ port number to access server
topic = "live_data"          #------------------- MQTT topic to be published
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
        "!!!!!!!!!!!!!!!!!!! need to change the file path with that in your PC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        with open('/home/surya/Downloads/IOT-standalone/client_side/cache.csv', 'a') as f_object:  
            writer_object = csv.writer(f_object)
            writer_object.writerow([client_id, frame_speed["S.No"], frame_speed["Time Stamp"], frame_speed["Speed"]])
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

def data_cleanup(data):
    data = data.strip("\n\x0c").replace(",", "")
    data = ''.join([i for i in data if i.isdigit()])
    return data


def data_validation(input, lastValue=0):  # using a default value of 0
    # flag to check if the value is acceptable or not
    divisionCheck = False
    rangeCheck = False

    # chec for null value
    if input == "":
        print("Null check activated")
        return lastValue

    # speed should be a multiple of 10
    if int(input) % 10 == 0:
        print("Division by 10 dectedted")
        divisionCheck = True
    else:
        print("NO division by 10")
        divisionCheck = False

    # value should be between 0 and 18000
    if int(input) <= 18000 and int(input) >= 0:
        print("speed within limit")
        rangeCheck = True
    else:
        print("speed out of limit")
        rangeCheck = False

    # returning the correct value
    if divisionCheck and rangeCheck:
        print("input returned")
        return input
    else:
        print("last value returned")
        return lastValue


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ff", "--firstFile", required=True,
                help="name of first input image to be OCR'd")
ap.add_argument("-nf", "--numOfFiles", required=True,
                help="number of images to be OCR'd")
args = vars(ap.parse_args())

# Initializing variables to track no of files processed, OCR data of a frame and overall speed data stored in a dict
file_count = 0
frame_speed = {}
speed_data = []
lastSpeed = 0

#--------------------------- MAIN FUNCTION WHERE IMAGE PROCESSING RUNS ---------------------------------------------------------------
def main_func():

    global file_count
    global frame_speed
    global lastSpeed
    global speed_data

    start_time = datetime.datetime.now()

    # load the input image and convert it from BGR to RGB channel ordering
    read_filename = int(args["firstFile"][0:16]) + file_count
    filename = "{}.jpg".format(str(read_filename).zfill(16))

    print("[INFO] Reading Image No {}. File Name {}".format(file_count, filename))

    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extract the relevant segment from image carrying the speed data
    frame = image[240:340, 750:940]

    cv2.imshow("frame {}".format(read_filename), frame)

    # frame Pre processing before OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    cv2.imshow("gray", gray)

    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imshow("thresh {}".format(read_filename), thresh)

    # use Tesseract to OCR the image
    options = "--psm 9"
    ocr_text = pytesseract.image_to_string(frame, config=options)

    # Data cleanup and validation
    speed = data_validation(data_cleanup(ocr_text), lastSpeed)
    # saving for next cycle
    lastSpeed = int(speed)
    cv2.waitKey(0)

    # Preparing data extracted from each frame and then saving it to the dictionary
    frame_speed = {
        "S.No": file_count,
        "Speed": int(speed),
        "Time Stamp": datetime.datetime.now()
    }

    speed_data.append(frame_speed)

    file_count += 1
    # end_time = datetime.datetime.now()
    # elapsed_time = end_time - start_time
    # print(elapsed_time.total_seconds())
   #  print(speed_data)
    print(frame_speed)

# field_names = ['S.No', "Speed", "Time Stamp"]

# Writing data from dictionary to csv file all in one go
# with open('speed.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=field_names)
#     writer.writeheader()
#     writer.writerows(speed_data)
#------------------------------------------------------------------------------------------------------------------------------------


#---------------------- run() function to execute the whole in loop -----------------------------------------------------------------
def run():
    while(1):
        try:
            client = connect_mqtt()
            client.loop_start()
            while file_count < int(args["numOfFiles"]):
                global prev_time
                #----if disconnected for more than 10sec then restart the connection-----------
                if(((time.time()-prev_time)>10)&(not Connect_Status)):
                    prev_time = time.time()
                    client.loop_stop()
                    client = connect_mqtt()
                    client.loop_start()
                main_func()
                publish(client, client_id, frame_speed["S.No"], frame_speed["Time Stamp"], frame_speed["Speed"])
                if(Connect_Status):
                    print("published file_count: %s"%file_count)
                else:
                    print("failed to publish file_count : %s"%file_count)
                Call_On_Disconnect(Connect_Status)
                time.sleep(1)
                print("-------------------------")
        except Exception as e:
            print(e)
            if(file_count < int(args["numOfFiles"])):
                main_func()
            Call_On_Disconnect(False)
        time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    run()