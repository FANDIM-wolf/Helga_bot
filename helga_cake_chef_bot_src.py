import telebot;
from telebot import types
import psycopg2
from psycopg2 import Error, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlite3 
import datetime
import random

bot = telebot.TeleBot('your token')

#data about cake



list_of_id=[]
list_of_key_words = []
list_of_cakes = []
#check data of subject
subject_call_back_data = []

    
class Cake(object):
    id = 0 
    name = " "
    recipe = ""
    key_words =[]
    power_for_process = 0
    photo_name = " "
    def print_data_about_cake(self):
        print(self.id , self.name , "Cake ." )   
        

def get_uniqe_id():
    id = random.randint(1,123453)
    if id in list_of_id :
        get_uniqe_id()
    else:
        return id    

def get_data_from_data_base():
    
    pk = get_uniqe_id()

    #firstly set connection to database 
    try:
    # Connection to current database
        connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # cursor is tool for working with Data Base
        cursor = connection.cursor()
        
        
        cursor.execute("SELECT * FROM recipes_of_cakes")
        for row in cursor:
            cake = Cake()
            cake.name = row[1]
            cake.recipe = row[2]
            cake.key_words = row[3]
            cake.power_for_process = 0
            cake.photo_name = row[5]
            list_of_cakes.append(cake)
            list_of_key_words.append(cake.key_words)
        print(list_of_cakes)
        print(list_of_key_words)
        
        #walk through all array key words and get any key_word
        for el in list_of_cakes:
            for subject in el.key_words:
                print(subject)

        connection.commit()
        
        print("Connection to DataBase : Successfully")
        
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

#get all data from db
get_data_from_data_base()




@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Вы можете выбрать 'Торт по индигриенту ' или просто написать название торта ")
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient = types.InlineKeyboardButton(text='Выбрать по индигриенту' , callback_data='get_indigrient')
        keyboard.add(key_indigrient)

        bot.send_message(message.from_user.id , text="Ваш выбор" , reply_markup=keyboard)
    elif message.text == "/search":
        bot.send_message(message.from_user.id , "Напишите названия торта")
        bot.register_next_step_handler(message,choice)     
    else:
        bot.send_message(message.from_user.id , "Я вас не понимаю , напишите /start поиск по индигриенту или /search свободный поиск")

#find cake in list in send to  user 
def choice(message):
    bot.send_message(message.from_user.id,"Ищу")
    name = message.text
    
    for el in list_of_cakes:
        if el.name == name:
                
            bot.send_message(message.from_user.id , 'Ваш торт :)')
            p = open(el.photo_name , 'rb')
            bot.send_photo(message.from_user.id,p)
            bot.send_message(message.from_user.id , el.name)
            bot.send_message(message.from_user.id , el.recipe)
    else:
        bot.send_message(message.from_user.id,"В целом поиск выдался хорошим. ")


@bot.callback_query_handler(func=lambda call:True)
def callback_work(call):
    if call.data == "get_indigrient":
        keyboard = types.InlineKeyboardMarkup() 

        for i in list_of_cakes:
            for subject in i.key_words:
                print(subject)
                key_name = types.InlineKeyboardButton(text=subject , callback_data=subject)

                keyboard.add(key_name)
                subject_call_back_data.append(subject)

                print("indigrient added")   
        bot.send_message(call.message.chat.id , text="Ваш индигриент " , reply_markup=keyboard) 
    

    elif call.data in subject_call_back_data:
        for el in list_of_cakes:
            for subject in el.key_words:
                if call.data in subject:
                    cake_for_user = Cake()
                    cake_for_user.name = el.name
                    cake_for_user.recipe = el.recipe
                    cake_for_user.photo_name = el.photo_name
                    
                    
        bot.send_message(call.message.chat.id , 'Ваш торт :)')
        p = open(cake_for_user.photo_name , 'rb')
        bot.send_photo(call.message.chat.id,p)
        bot.send_message(call.message.chat.id , cake_for_user.name)
        bot.send_message(call.message.chat.id , cake_for_user.recipe)

    
        

#start bot 
bot.polling(none_stop=True , interval=0)        
