from tkinter import *  
import mysql.connector

#-------------------------------mysql db credentials-----------------------------------------------------------------------------------
mydb = mysql.connector.connect(
    user='surya',
    password='Suryamysql@1234',
    host='localhost',
    port=3306,
    database='test',
    auth_plugin='mysql_native_password'
    )

mycursor = mydb.cursor()
sql_select_Query = "select * from register_values_em6400" #---------------quiry to select data from em6400 table

mycursor.execute(sql_select_Query)
#variable to store the data from em6400 table
records = mycursor.fetchall()

#--------------------------------------creating a tkinter window----------------------------------------------------------------
Window = Tk()   
Window.geometry("1080x600")  #-------set window size
Window.title('Database GUI') #-----------window name

# label widget for average current value
Label(Window, text = "Average current :", anchor=CENTER, fg='black', relief=RAISED, font=('Helvetica', 15, 'bold'), pady=5).place(x = 40,y = 60) 
current_val = Label(Window, text = "12334345567 A", anchor=CENTER, fg='red', relief=RIDGE, font=('Helvetica', 25, 'bold'), bg='black')
current_val.place(x = 40,y = 90) 

#label widget for average voltage value
Label(Window, text = "Average voltage :", anchor=CENTER, fg='black', relief=RAISED, font=('Helvetica', 15, 'bold'), pady=5).place(x = 40,y = 150) 
voltage_val = Label(Window, text = "66453678696 V", anchor=CENTER, fg='red', relief=RIDGE, font=('Helvetica', 25, 'bold'), bg='black')
voltage_val.place(x = 40,y = 180) 

#label widget for power factor
Label(Window, text = "Power factor :", anchor=CENTER, fg='black', relief=RAISED, font=('Helvetica', 15, 'bold'), pady=5).place(x = 40,y = 240) 
power_fac_val = Label(Window, text = "1.1100023", anchor=CENTER, fg='red', relief=RIDGE, font=('Helvetica', 25, 'bold'), bg='black')
power_fac_val.place(x = 40,y = 270) 

#label widget for output power
Label(Window, text = "Power output :", anchor=CENTER, fg='black', relief=RAISED, font=('Helvetica', 15, 'bold'), pady=5).place(x = 40,y = 330) 
power_out_val = Label(Window, text = "233468876 Kw", anchor=CENTER, fg='red', relief=RIDGE, font=('Helvetica', 25, 'bold'), bg='black')
power_out_val.place(x = 40,y = 360)

#label widget for enery
Label(Window, text = "Energy :", anchor=CENTER, fg='black', relief=RAISED, font=('Helvetica', 15, 'bold'), pady=5).place(x = 40,y = 420) 
enery_val = Label(Window, text = "233468876 Kw", anchor=CENTER, fg='red', relief=RIDGE, font=('Helvetica', 25, 'bold'), bg='black')
enery_val.place(x = 40,y = 450)

#----------------itirating function for updating widgets-------------------------------
def Run():
    global i
    text_input = [records[i][5], records[i][13], records[i][21], records[i][17], records[i][1]]
    current_val.config(text=str(text_input[0])+" A")
    voltage_val.config(text=str(text_input[1])+" V")
    power_fac_val.config(text=text_input[2])
    power_out_val.config(text=str(text_input[3])+" Kw")
    enery_val.config(text=str(text_input[4])+" Kwh")
    i+=1
    current_val.after(1000, Run) #--------generating 1000ms interval
i = 0

Run() #-------------starting Run() fucntion
Window.mainloop() #--------tkinter loop to keep window active


