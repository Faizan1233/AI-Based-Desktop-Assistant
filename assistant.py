import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import pyjokes
from password import a # Password is a python file which contains 'a' variable in which password is stored of 
#                       your email address "youremail@gmail.com"
from threading import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jojo import Ui_MainWindow
import sys

#
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am your Assistant Sir. Please tell me how may I help you")
    
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'a') # 'a' is the password imported from password python file.
    server.sendmail('xyz@gmail.com', to, content)
    server.close()
#
class MainThread(QThread):

    def __init__(self): 
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()
#   
        
    def takeCommand(self): 
            #It takes microphone input from the user and returns string output

            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print("Recognizing...")    
                self.query = r.recognize_google(audio, language='en-in')
                print(f"You said: {self.query}\n")

            except Exception as e:
                # print(e)    
                print("Say that again please...")  
                return "None"
            return self.query
    
    def TaskExecution(self):
        wishMe()
        while True:
        # if 1:
            self.query =self.takeCommand().lower()

            # Logic for executing tasks based on query
            if 'wikipedia' in self.query:
                speak('Searching Wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in self.query:
                print("Opening Youtube...")
                speak("Opening you tube")
                webbrowser.open("youtube.com")

            elif 'open google' in self.query:
                print("Opening Google...")
                speak("Opening Google")
                webbrowser.open("google.com")

            elif 'open stackoverflow' in self.query:
                print("Opening stackoverflow...")
                speak("Opening stackoverflow")
                webbrowser.open("stackoverflow.com")   

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%I:%M:%S")    
                print(strTime)
                speak(f"Sir, the time is {strTime}")

            elif 'open code' in self.query:
                print("Opening Code...")
                speak("Opening Code")
                codePath = "C:\\Users\\..\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)

            elif 'joke' in self.query:
                
                speak(pyjokes.get_joke())
                

            elif 'email to xyz' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takeCommand()
                    to = "xyz@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry Sir, I am not able to send this email")    

            elif 'bye' in self.query:
                speak("Good Bye Sir, See you soon")
                exit()
# Last Part (after TaskExecution)           
startExecution=MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/faiza/Desktop/Projects/JOJO/Bot.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.run() 

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.label_2.setText(label_date)
        self.ui.label_3.setText(label_time)


    
        
app = QApplication(sys.argv)
assistant = Main()
assistant.show()
exit(app.exec_())
#