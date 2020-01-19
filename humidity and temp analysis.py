#!/usr/bin/python3
# Author: Prasandeep Singh

# Import packages/modules
import tkinter as tk
from tkinter.constants import *
from tkinter import messagebox
from sense_hat import SenseHat
import datetime
import sqlite3
import csv

# Creation of our base class

class myProjectClass():
     
            
    def __init__(self, master):     # Initialization of application; attributes and widgets
        master.title('Python Project')
        master.geometry("780x500")

        

        sense = SenseHat()      #instantiate the object for sensehat()
        
        self.humidity = sense.get_humidity()        #using the attributes of the class to get the humidity, this wil give humidity on GUI as soon as you run the program 
        self.temp = sense.get_temperature()         #using the attributes of the class to get the temperature, this wil give temperature on GUI as soon as you run the program 
    
        self.myDate = datetime.datetime.now()       #to get the time and the date

        self.var1 = self.myDate.strftime("%d/%m/%Y")    #assign the date to a variable, self.var1
        self.var2 = self.myDate.strftime("%H:%M:%S")    #assign the time to a variable, self.var2

        self.myProjectLabel1 = tk.Label(master, text = "Today's date:") #creation of label widget for date
        self.myProjectLabel1.grid(row=2, column=0,padx=5, pady=5)  #placing the widget on Window


        self.myProjectLabel2 = tk.Label(master, text = self.var1)#creation of label widget to show date
        self.myProjectLabel2.grid(row=2, column=1,padx=5, pady=5)  #placing the widget on Window

        self.myProjectLabel3 = tk.Label(master, text = "Current Time:") #creation of label widget for time
        self.myProjectLabel3.grid(row=3, column=0,padx=5, pady=5)  #placing the widget on Window

        
        self.myProjectLabel4 = tk.Label(master, text = self.var2) #creation of label widget to show time
        self.myProjectLabel4.grid(row=3, column=1,padx=5, pady=5)  #placing the widget on Window
        

        self.myProjectLabel5 = tk.Label(master, text = "temperature outside is:") #creation of label widget for temperature
        self.myProjectLabel5.grid(row=7, column=0,padx=5, pady=5)  #placing the widget on Window

        self.myProjectLabel6 = tk.Label(master, text = self.temp) #creation of label widget to show temperature
        self.myProjectLabel6.grid(row=7, column=1,padx=5, pady=5)  #placing the widget on Window

        self.myProjectLabel7 = tk.Label(master, text = "humidity outside is:") #creation of label widget for humidity
        self.myProjectLabel7.grid(row=8, column=0,padx=5, pady=5)  #placing the widget on Window

        self.myProjectLabel8 = tk.Label(master, text = self.humidity) #creation of label widget to show humidity
        self.myProjectLabel8.grid(row=8, column=1,padx=5, pady=5)  #placing the widget on Window


        self.mySaveFileFileButton = tk.Button(master, 
                                       text="Press to process", 
                                       command= self.myProcessFileClick) #button widget to process the file
        self.mySaveFileFileButton.grid(row=9, column=1,padx=5, pady=5)

        self.mySaveFileFileButton2 = tk.Button(master, 
                                       text="Press to save to CSV", 
                                       command= self.saveToCSV) #button widget to save the file as CSV
        self.mySaveFileFileButton2.grid(row=10, column=1,padx=5, pady=5)

        self.myWindowsExitButton = tk.Button(master, text="Exit",command= root.destroy) #adding exit button to widget
        self.myWindowsExitButton.grid(row=11, column=1,padx=5, pady=5) #placing the widget on window

 
        


    def myProcessFileClick(self):

        conn = sqlite3.connect('myDatabase1.db')    #making a connection to database called myDatabase1.db

        c = conn.cursor()       #intializing cursor


        # Creating a table named projectTable
        c.execute('''CREATE TABLE IF NOT EXISTS projectTable
                    (date text, time text, temperature real, humidity real)''')

        sense = SenseHat()          #used this again to get the refresh value everytime you click press to process button
        
        sense.clear()
        self.humidity = sense.get_humidity()
        self.temp = sense.get_temperature()
        x = str(self.temp)          #converting the temperature value into string to insert into table created
        y = str(self.humidity)      #converting the humidity value into string

        self.var1 = self.myDate.strftime("%d/%m/%Y")    #assign the time to a variable, self.var1
        self.var2 = self.myDate.strftime("%H:%M:%S")    #assign the time to a variable, self.var2

        t = str(self.var1)      #converting date variable into string
        p = str(self.var2)      #converting time variable into string

        self.myProjectLabel1.config(text = self.var1)           #this will show the refreshed value of date
        self.myProjectLabel4.config(text = self.var2)           #this will show the refreshed value of time
        self.myProjectLabel6.config(text = self.temp)           #this will show the refreshed value of temperature
        self.myProjectLabel8.config(text = self.humidity)       ##this will show the refreshed value of humidity


        
        # Insert the data into row
        c.execute('''INSERT INTO projectTable (date, time, temperature, humidity) VALUES (?,?,?,?)''',(t, p, x, y))

        print(c.execute('''select * from projectTable'''))
        print(c.fetchmany(10))



        # Save the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.

        conn.close()
        


            
    def saveToCSV(self):

            conn = sqlite3.connect('myDatabase1.db')    #making a connection to database called myDatabase1.db

            c = conn.cursor()           #intializing cursor

            c.execute('SELECT * FROM projectTable')

            myRowHeader = c.description

            myRowsData = c.fetchmany(10)


            
            with open('myProjectResult.csv', 'w') as myOutputFile:              #read the data from Databse and store it into CSV file
                csvOutput = csv.writer(myOutputFile)
                csvOutput.writerow([myDescriptionIndex[0] for myDescriptionIndex in c.description])
                for result in c:
                    csvOutput.writerow(result)
                    



            conn.close()
            

            

                
# Creating application
root = tk.Tk()   
app = myProjectClass(root)

# Starting application
root.mainloop()

#reference: links from class lectures weeks
