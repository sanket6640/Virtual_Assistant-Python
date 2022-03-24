import os
import random
import re
import mysql.connector
from geopy.geocoders import Nominatim
import pyautogui
import speech_recognition as sr
import pyttsx3
import pywhatkit
import flask
import datetime
import wikipedia
import pyjokes
import webbrowser
import ctypes
import sys
import requests, json
import time
import screen_brightness_control as sbc
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def database():
    global db, cursor
    User = os.getenv('user')
    Password = os.getenv('password')

    db = mysql.connector.connect(host='localhost', user=User, password=Password, database='shree')
    cursor = db.cursor()


listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    global command
    try:

        with sr.Microphone() as source:

            print("listening....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:

        talk('turning off')

        sys.exit()

    except sr.RequestError:
        print('error')

    return command


def greet_user():
    hour = datetime.datetime.now().hour
    if (hour >= 1) and (hour < 12):
        talk('hi. Good Morning sanket. I am your personal assistant.  How may i help you')
    elif (hour >= 12) and (hour < 17):
        talk('hi. Good afternoon sanket. I am your personal assistant.  How may i help you')
    elif (hour >= 17) and (hour < 24):
        talk('hi. Good Evening sanket.  I am your personal assistant.  How may i help you.')


def save_number():
    database()
    Cursor = cursor
    name = input("Enter name: ")
    number = input("Enter number")
    data = "Insert into contact(Name, Number) value(%s,%s)"
    contact = (name, number)
    Cursor.execute(data, contact)
    db.commit()
    talk("saved successfully")


def chk_weather():
    api_key = os.getenv('Api_Key')
    city_name = os.getenv('City_Name')
    location = city_name
    full_id = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + api_key
    api_link = requests.get(full_id)
    api_data = api_link.json()
    temp_city = ((api_data['main']['temp']) - 275.15)
    dis = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_sd = api_data['wind']['speed']

    talk('Current Temperature is.  {:.2f} deg C'.format(temp_city))
    talk('Weather is. ' + dis)
    talk('humidity. {:.2f} % '.format(hmdt))
    talk('wind speed. {:.2f} KMPH'.format(wind_sd))
    if temp_city < 20:
        talk('Its cold. wear hot clothes.')
    elif temp_city < 15:
        talk('Its very cold. wear hot clothes and stay at home.')
    elif temp_city < 10:
        talk('Its Extremely cold. wear hot clothes and dont go outside without hot clothes.')


def set_brightness():
    if '25' in command:
        talk('brightness level 25 %')
        level = '25'
        sbc.set_brightness(level)
    elif '50' in command:
        talk('brightness level 50 %')
        level = '50'
        sbc.set_brightness(level)
    elif '75' in command:
        talk('brightness level 75 %')
        level = '75'
        sbc.set_brightness(level)

    elif '100' in command:
        talk('brightness level 100 %')
        level = '100'
        sbc.set_brightness(level)
    elif '0' in command:
        talk('brightness level 0 %')
        level = '0'
        sbc.set_brightness(level)


def chk_time():
    t = datetime.datetime.now().strftime('%I:%M %p')
    talk('Current time is' + t)


def run_shree():
    global command
    global time

    command = take_command()
    print(command)

    if 'hello' in command:
        greet_user()

    elif 'save number' in command:
        save_number()

    elif 'play' in command:
        song = command.replace('play', '')
        talk(song + 'playing')
        pywhatkit.playonyt(song)

    elif 'morning' in command:
        talk('Good Morning Sanket')
        chk_weather()
    elif 'weather' in command:
        chk_weather()
    elif 'brightness' in command:
        set_brightness()

    elif 'time' in command:
        chk_time()
    elif 'music' in command:
        talk('playing')
        Music = os.getenv('music')
        music_dir = Music
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, random.choice(songs)))

    elif 'information about' in command:
        person = command.replace('information about', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk('according to Wikipedia' + info)

    elif "where is" in command:

        command = command.replace("where is", "")

        location = command

        talk('Here is ')

        talk(location)

        webbrowser.open('https://www.google.nl/maps/place/' + location + '')

    elif 'who i am' in command:
        Name = os.getenv('name')
        talk(Name)
    elif 'you do' in command:
        talk(
            'i tell you joke, time, play youtube videos & music, open whatsapp, telegram, word, google, pycharm, exel, notepad, vlc, instagram, i search a location ')

    elif 'who are you' in command:
        talk('I am your personal assistant')

    elif 'who is your best friend' in command:
        talk('Wifi is my best friend.')
    elif 'screenshot' in command:
        pyautogui.screenshot(str(time.time()) + '.png').show()

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'open google' in command:
        talk('Opening Google')
        Gurl = os.getenv('gurl')
        webbrowser.open(Gurl)

    elif 'open email' in command:
        talk('Opening email')
        Email = os.getenv('email')
        webbrowser.open(Email)

    elif 'send email' in command:
        talk('Opening email compose')
        Mail = os.getenv('mail')
        webbrowser.open(Mail)

    elif 'take a photo' in command:
        ec.capture(0, 'Shree Camera', 'img.jpg')

    elif 'open excel' in command:
        talk('Opening excel')
        Exel = os.getenv('exelid')
        webbrowser.open_new(Exel)

    elif 'word' in command:
        talk('Opening word')
        Word = os.getenv('wordid')
        webbrowser.open_new(Word)

    elif 'notepad' in command:
        talk('Opening notepad')
        os.system('NOTEPAD')
    elif 'cmd' in command:
        talk('Opening cmd')
        os.system('cmd')
    elif 'whatsapp' in command:
        talk('Opening whatsapp')
        App_idw = os.getenv('app_idw')
        os.startfile(App_idw)
    elif 'open vlc' in command:
        talk('Opening vlc player')
        App_idv = os.getenv('app_idv')
        os.startfile(App_idv)
    elif 'news' in command:
        talk('here is some news')
        News = os.getenv('news')
        webbrowser.open_new(News)
    elif 'instagram' in command:
        talk('enjoy')
        Insta = os.getenv('instaId')
        webbrowser.open_new(Insta)
    elif 'code' in command:
        talk('learn')
        webbrowser.open_new('https://www.w3schools.com/')
    elif 'pycharm' in command:
        talk('Opening pycharm')
        app_id = r'F:\Pycharm\PyCharm Edu 2021.2.1\bin\pycharm64.exe'
        os.startfile(app_id)
    elif 'telegram' in command:
        talk('Opening telegram')
        App_idt = os.getenv('app_idt')
        os.startfile(App_idt)

    elif 'search' in command:
        talk('searching...')
        webbrowser.open_new_tab(command)
    elif 'stop' in command:
        talk('ok. thank you.')
        sys.exit()
    elif 'thank you' in command:
        talk('ok. enjoy.')
        sys.exit()


while 1:
    run_shree()
