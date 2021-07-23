from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from mini2 import Ui_MainWindow
import sys
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import re
from wordcloud import WordCloud
import pandas as pd
import os
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',160)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    def run(self):
        self.taskexe()
    def greetme(self):
        hours=int(datetime.datetime.now().hour)
        if hours>=0 and hours<=12:
            speak("Good morning Sir ")
        elif hours>12 and hours<=18:
            speak("Good afternoon Sir")
        else:
            speak("good evening rythem")
    def takecommand(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold=1
            r.energy_threshold=100
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio=r.listen(source)
        try:
            print("Recognizing....")
            query=r.recognize_google(audio,language='en-in')
            print("user said "+query)
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query
    def playmusic(self):
        loc="D:\\B tech IV sem\\New folder\\song"
        songs=os.listdir(loc)
        os.startfile(os.path.join(loc,songs[0]))
    def analysis(self):
        pd.set_option('display.max_columns',None)
        pd.set_option('display.max_rows',None)
        consumer_key = "zvghpJLaBrHdUqloJDlcV7rum"
        consumer_sec = "BKvbGtBlMBUPn9ONG1x7LrYkLclA2sRXT5G4KuGZiPgGlnNq2R"
        access_token = "1383703955218132994-lz4OavJh4DLABqVo4SBnjzqSWw72vE"
        access_token_sec = "oj254ngv1FjYnVveQOL1SQuRxOtR88xkROqaXSm8zalPQ"
    # create an authentication object
        auth = tweepy.OAuthHandler(consumer_key, consumer_sec)
    # set the access token and access token secret
        auth.set_access_token(access_token, access_token_sec)
    # create an API object
        api_connect = tweepy.API(auth)
        speak("sir please enter the subject")
        text1 = input("enter the subject")
        tweet_data = api_connect.search(text1, count=100)
        speak("tweets have been successfully fetched")
        df = pd.DataFrame([tweet.text for tweet in tweet_data], columns=['Tweets'])
        def cleantxt(text):
            text = re.sub(r'@[A-Za-z0-9]+', '', text)
            text = re.sub(r'#', '', text)
            text = re.sub(r'RT[\s]+', '', text)
            text = re.sub(r'https?:\/\/\S+', '', text)
            return text

        df['Tweets'] = df['Tweets'].apply(cleantxt)
        speak("text has been cleaned by")
    # function to get subjectivity
        def getsubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

    # function to get polarity
        def getpolarity(text):
            return TextBlob(text).sentiment.polarity

        df['Subjectivity'] = df['Tweets'].apply(getsubjectivity)
        df['Polarity'] = df['Tweets'].apply(getpolarity)

    # function to get analysis
        def getAnalysis(x):
            if (x < 0):
                return 'Negative'
            elif (x == 0):
                return 'Neutral'
            elif (x > 0):
                return 'Positive'

        df['Analysis'] = df['Polarity'].apply(getAnalysis)
    # plot the graph between Subjectivity and polarity
        speak("do you want the graph between Subectivity and polarity analysis")
        op = self.takecommand().lower()
        print("user said "+op)
        if 'yes' == op or 'sure' == op:
            plt.figure(figsize=(8, 6))
            for i in range(0, df.shape[0]):
                plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')
            plt.title('Sentiment Analysis')
            plt.xlabel('Polarity')
            plt.ylabel('Subjectivity')
            plt.show()
            df['Analysis'].value_counts()
            plt.title('Sentiment Analysis')
            plt.xlabel('Sentiment')
            plt.ylabel('Counts')
            df['Analysis'].value_counts().plot(kind='bar')
            plt.show()
        elif 'no'==op:
            speak('okay sir! no problem')

    # plotting of wordcloud
        speak("do you want the wordcloud analysis")
        op=self.takecommand().lower()
        print("user said "+op)
        if 'yes'==op or 'sure'==op:
            wrds = ' '.join([twts for twts in df['Tweets']])
            wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(wrds)
            plt.imshow(wordCloud, interpolation="bilinear")
            plt.axis('off')
            plt.show()
            print(df)
        elif 'no'==op:
            speak("okay sir")
        speak("sentiment analysis has been successfully done")
        speak("Sir please have a look on your summarised data frame")
        print(df)

    def taskexe(self):
        self.greetme()
        speak("how may i help you"+"Sir")
        speak("before starting it is adivsed to setup he microphone setting")
        while(True):
            self.query=self.takecommand().lower()
            if "wikipedia" in self.query:
             print("Searching Wikipedia....")
             self.query=self.query.replace("wikipedia","")
             results=wikipedia.summary(self.query,sentences=2)
             speak("according to wikipedia"+results)
            elif "open youtube" in self.query:
                webbrowser.open("youtube.com")
            elif "open google" in self.query:
                webbrowser.open("google.com")
            elif "analysis" in self.query:
                self.analysis()
            elif "play music" in self.query:
                self.playmusic()
            elif "the time" in self.query:
                strtime=datetime.datetime.now().strftime("%H:%M:%S")
                speak("the time is"+strtime)
            elif"open whatsapp" in self.query:
                webbrowser.open("whatsappweb.com")
start_execution=MainThread()
class Gui_start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startFunct)
        self.ui.pushButton_2.clicked.connect(self.close)
    def startFunct(self):
        self.ui.movies_label_2=QtGui.QMovie("live.gif")
        self.ui.label_2.setMovie(self.ui.movies_label_2)
        self.ui.movies_label_2.start()

        self.ui.movies_label3=QtGui.QMovie("B.G_Template_1.gif")
        self.ui.label_3.setMovie(self.ui.movies_label3)
        self.ui.movies_label3.start()

        self.ui.movies_label6=QtGui.QMovie("Earth.gif")
        self.ui.label_6.setMovie(self.ui.movies_label6)
        self.ui.movies_label6.start()

        self.ui.movies_label7=QtGui.QMovie("Health_Template.gif")
        self.ui.label_7.setMovie(self.ui.movies_label7)
        self.ui.movies_label7.start()

        self.ui.movies_label8 = QtGui.QMovie("Jarvis_Gui (2).gif")
        self.ui.label_8.setMovie(self.ui.movies_label8)
        self.ui.movies_label8.start()
    start_execution.start()
Gui_App=QApplication(sys.argv)
Gui_mini=Gui_start()
Gui_mini.show()
exit(Gui_App.exec_())
