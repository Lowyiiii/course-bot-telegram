API_TOKEN = '1357728588:AAGE0AdG08zTFxJ_0ZhfPWQB4r4bFwZWL7U'

WEBHOOK_HOST = '51.195.19.117'
WEBHOOK_PORT = 80
WEBHOOK_LISTEN = '51.195.19.117'

WEBHOOK_SSL_CERT = '/home/lowyi/myprojectdir/telegram/course/webhook_cert.pem'
WEBHOOK_SSL_PRIV = '/home/lowyi/myprojectdir/telegram/course/webhook_pkey.pem'
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
import cherrypy
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telecontext.bot.types.Update.de_json(json_string)
            context.bot.process_new_updates([update])
            return ''
        else:
            
	        raise cherrypy.HTTPError(403)


from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackQueryHandler,CallbackContext
from telegram import ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup,ForceReply,ReplyKeyboardRemove
import telegram
import requests
import json
import sqlite3
from time import sleep

# MAIN,FATHER,FATHER_QUEST,FATHER_REG,WIVES,WIVE_QUEST,WIVE_REG, SONS,BOYS,BOY_QUEST,BOY_REG,GIRLS,GIRL_QUEST,GIRL_REG ,QA,CONTACT = range(16)
MAIN,QA,CONTACT,WIVES,WIVE_QUEST,WIVE_REG,FATHER,FATHER_QUEST,FATHER_REG,BOYS,BOY_QUEST,BOY_REG,GIRLS,GIRL_QUEST,GIRL_REG,SONS = range(16)

db_path = r'course.db'
conn = sqlite3.connect(db_path,check_same_thread=False)
c = conn.cursor()


def insert_day(name):
    c.execute(''' INSERT into Day (name) values ("{}");'''.format(name))
    c.execute('''DELETE FROM Day WHERE rowid NOT IN (SELECT min(rowid) FROM Day GROUP BY name)''')
    conn.commit()

def get_day_from_api():
    i=1
    while(True):
        r = requests.get('http://51.195.19.117:8000/api/day/{}'.format(i))
        if (r.status_code) == 200:
            day_name = r.json()[str("name")]
            print(day_name)
            insert_day(day_name)
            i+=1
        else:
            break


def get_course_from_api():

    i=1
    while(True):
        r = requests.get('http://51.195.19.117:8000/api/course/{}'.format(i))
        if (r.status_code) == 200:
            course_name = r.json()[str("name")]
            print(course_name)
            insert_day(course_name)
            i+=1
        else:
            break
    



def insert_course_quest_mother(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,link):

    c.execute('''INSERT into Mother(title,quest,choice1,choice2,choice3,choice4,answer,score,day,link) values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'''.format(title, quest, choice_1, choice_2, choice_3, choice_4, answer, score, day,link))
    c.execute('''DELETE FROM Mother WHERE rowid NOT IN (SELECT min(rowid) FROM Mother GROUP BY quest)''')

    conn.commit()
    print("\n")

def get_mother_quest_from_api():
    i=1
    while(True):

        r = requests.get('http://51.195.19.117:8000/api/mother/{}'.format(i))
        if (r.status_code) == 200:
            title = r.json()[str('Title')]
            quest = r.json()[str("Quest")]
            choice_1 = r.json()[str("Choice_1")]
            choice_2 = r.json()[str("Choice_2")]
            choice_3 = r.json()[str("Choice_3")]
            choice_4 = r.json()[str("Choice_4")]
            answer = r.json()[str("Answer")]
            score = r.json()[str("Score")]
            
            # course = r.json()[str('Courses')]
            day = r.json()[str('Days')]
            document  = r.json()[str("link")]
            print(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,document)
            insert_course_quest_mother(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,document)
            i+=1
        else:
            break


def insert_course_quest_father(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,link):

    c.execute('''INSERT into Father(title,quest,choice1,choice2,choice3,choice4,answer,score,day,link) values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'''.format(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,link))
    c.execute('''DELETE FROM Father WHERE rowid NOT IN (SELECT min(rowid) FROM Father GROUP BY quest)''')

    conn.commit()
    print("\n")

        
def get_father_quest_from_api():
    i=1
    while(True):

        r = requests.get('http://51.195.19.117:8000/api/father/{}'.format(i))
        if (r.status_code) == 200:
            title = r.json()[str('Title')]
            quest = r.json()[str("Quest")]
            choice_1 = r.json()[str("Choice_1")]
            choice_2 = r.json()[str("Choice_2")]
            choice_3 = r.json()[str("Choice_3")]
            choice_4 = r.json()[str("Choice_4")]
            answer = r.json()[str("Answer")]
            score = r.json()[str("Score")]
            # course = r.json()[str('Courses')]
            day = r.json()[str('Days')]
            document  = r.json()[str("link")]
            print(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,document)
            insert_course_quest_father(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day,document)
            i+=1
        else:
            break



def insert_course_quest_boy(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day):

    c.execute('''INSERT into Boy(title,quest,choice1,choice2,choice3,choice4,answer,score,day) values("{}","{}","{}","{}","{}","{}","{}","{}","{}");'''.format(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day))
    c.execute('''DELETE FROM Boy WHERE rowid NOT IN (SELECT min(rowid) FROM Boy GROUP BY quest)''')

    conn.commit()
    print("\n")

        
def get_boy_quest_from_api():
    i=1
    while(True):

        r = requests.get('http://51.195.19.117:8000/api/boy/{}'.format(i))
        if (r.status_code) == 200:
            title = r.json()[str('Title')]
            quest = r.json()[str("Quest")]
            choice_1 = r.json()[str("Choice_1")]
            choice_2 = r.json()[str("Choice_2")]
            choice_3 = r.json()[str("Choice_3")]
            choice_4 = r.json()[str("Choice_4")]
            answer = r.json()[str("Answer")]
            score = r.json()[str("Score")]
            # course = r.json()[str('Courses')]
            day = r.json()[str('Days')]
            print(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day)
            insert_course_quest_boy(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day)
            i+=1
        else:
            break




def insert_course_quest_girl(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day):

    c.execute('''INSERT into Girl(title,quest,choice1,choice2,choice3,choice4,answer,score,day) values("{}","{}","{}","{}","{}","{}","{}","{}","{}");'''.format(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day))
    c.execute('''DELETE FROM Girl WHERE rowid NOT IN (SELECT min(rowid) FROM Girl GROUP BY quest)''')

    conn.commit()
    print("\n")

        
def get_girl_quest_from_api():
    i=1
    while(True):

        r = requests.get('http://51.195.19.117:8000/api/girl/{}'.format(i))
        if (r.status_code) == 200:
            title = r.json()[str('Title')]
            quest = r.json()[str("Quest")]
            choice_1 = r.json()[str("Choice_1")]
            choice_2 = r.json()[str("Choice_2")]
            choice_3 = r.json()[str("Choice_3")]
            choice_4 = r.json()[str("Choice_4")]
            answer = r.json()[str("Answer")]
            score = r.json()[str("Score")]
            # course = r.json()[str('Courses')]
            day = r.json()[str('Days')]
            print(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day)
            insert_course_quest_girl(title,quest,choice_1,choice_2,choice_3,choice_4,answer,score,day)
            i+=1
        else:
            break



def listToString(s):  
    
    # initialize an empty string 
    str1 = "," 
    # return string   
    return (str1.join(s)) 


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update,context):
    user = update.message.from_user
    username = user['username']
    text = """
    کاربر گرامی {} به ربات دوره بصیرت مجازی خوش آمدید:\n
     دوره بصیرت مجازی به مدت ۷ روز برگزار خواهد شد، لذا تا پایان دوره، از این ربات و کانال مصباح ۴۰۵  خارج نشوید.
    \n

🔸 دوره بصیرت مجازی ویژه  مادران بوده و برابر گروه بندی زیر اجرا خواهد شد:


☜ برای شرکت در دوره بصیرت لطفاً شروع را انتخاب نمایید: 👇
    """.format(username)

    
    custom_keyboard = [["🟢شروع🟢"]]
                       
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard = True)
    context.bot.send_message(chat_id = update.message.chat_id,text = text,reply_markup=reply_markup)
    return MAIN



                    # [["🟢پدران🟢"],
                    #    ["🔵مادران🔵"],
                    #    ["🟡فرزندان🟡"],
                    #    ["❓پرسش و پاسخ❓",
                    #    "💬ارتباط با ما💬"]]


def battery(update,context):
    custom_keyboard = [["🟢جنگ نرم و تحلیل سیاسی🟢"],
                       ["🔵سبک زندگی اسلامی و تربیت فرزند🔵"],
                       ["💬ارتباط با ما💬"]]
                       
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,text="لطفا یک گزینه را انتخاب کنید", reply_markup=reply_markup)
    
def low(update,context):

    if (update.message.text == "🟢شروع🟢"):
        battery(update,context)
    elif (update.message.text == "🟢جنگ نرم و تحلیل سیاسی🟢"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "🔈شما گزینه مسابقه جنگ نرم و تحلیل سیاسی را انتخاب کرده اید🔈",reply_markup=None)
        father_section(update,context)
    elif (update.message.text == "🔵سبک زندگی اسلامی و تربیت فرزند🔵"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "🔈شما گزینه مسابقه سبک زندگی اسلامی و تربیت فرزند را انتخاب کرده اید🔈",reply_markup=None)
        wives_section(update,context)
    elif (update.message.text == "🟡فرزندان🟡"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "🔈شما گزینه مسابقه فرزندان را انتخاب کرده اید🔈",reply_markup=None)
        sons_section(update,context)
    elif (update.message.text == "❓پرسش و پاسخ❓"):
        qa(update,context)
        return QA
    elif (update.message.text == "💬ارتباط با ما💬"):
        contact(update,context)
        return CONTACT
    elif (update.message.text == "🔵ثبت نام🔵"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "✅ گروه «سبک زندگی اسلامی و تربیت فرزند» برای شما با موفقیت ثبت گردید. برای شرکت در دوره کافیست یک بار ثبت نام کنید و سپس با انتخاب «روز مورد نظر» کلیپ و سوال را مشاهده نمایید.",reply_markup=None)
        wive_register(update,context)
    elif (update.message.text == "🔵سوالات🔵"):        
        wive_quest(update,context)
    elif (update.message.text == "🔵بازگشت🔵"):
        battery(update,context)
    elif (update.message.text == "🟢ثبت نام🟢"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "✅ گروه «جنگ نرم و تحلیل سیاسی» برای شما با موفقیت ثبت گردید. برای شرکت در دوره کافیست یک بار ثبت نام کنید و سپس با انتخاب «روز مورد نظر» کلیپ و سوال را مشاهده نمایید.",reply_markup=None)
        father_register(update,context)
    elif (update.message.text == "🟢سوالات🟢"):
        father_quest(update,context)
    elif (update.message.text == "🟢بازگشت🟢"):
        battery(update,context)
    elif (update.message.text == "🟣ثبت نام🟣"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "✅ گروه «پسران» برای شما با موفقیت ثبت گردید. برای شرکت در دوره کافیست یک بار ثبت نام کنید و سپس با انتخاب «روز مورد نظر» کلیپ و سوال را مشاهده نمایید.",reply_markup=None)

        boy_register(update,context)
    elif (update.message.text == "🟣سوالات🟣"):
        boy_quest(update,context)
    elif (update.message.text == "🟣بازگشت🟣"):
        sons_section(update,context)
    elif (update.message.text == "🟠ثبت نام🟠"):
        context.bot.send_message(chat_id = update.message.chat_id,text = "✅ گروه «دختران» برای شما با موفقیت ثبت گردید. برای شرکت در دوره کافیست یک بار ثبت نام کنید و سپس با انتخاب «روز مورد نظر» کلیپ و سوال را مشاهده نمایید.",reply_markup=None)

        girl_register(update,context)
    elif (update.message.text == "🟠سوالات🟠"):
        girl_quest(update,context)
    elif (update.message.text == "🟠بازگشت🟠"):
        sons_section(update,context)
    
    ################################

    elif (update.message.text == "🔵روزاول🔵"):
        
        sql_query = '''SELECT d1 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 1'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        context.bot.send_message(chat_id=update.message.chat_id,text=".",reply_markup=None)
        record = '''SELECT quest FROM Mother WHERE day = 1 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        mamad = c.fetchone()[0]
        conn.commit()
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 1""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 1""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 1""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 1""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-1-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-1-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-1-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-1-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)

        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video="https://video-17.dalfak.com/31/31227-577761959812_360.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)
        
    elif (update.message.text == "🔵روزدوم🔵"):

        sql_query = '''SELECT d2 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 2'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))



        record = '''SELECT quest FROM Mother WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 2""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 2""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 2""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 2""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-2-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-2-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-2-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-2-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)

    elif (update.message.text == "🔵روزسوم🔵"):

        sql_query = '''SELECT d3 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 3'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        record = '''SELECT quest FROM Mother WHERE day = 3 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 3""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 3""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 3""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 3""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-3-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-3-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-3-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-3-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)
    
    elif (update.message.text == "🔵روزچهارم🔵"):


        sql_query = '''SELECT d4 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 4'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        record = '''SELECT quest FROM Mother WHERE day = 4 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 4""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 4""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 4""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 4""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-4-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-4-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-4-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-4-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)

        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)


    elif (update.message.text == "🔵روزپنجم🔵"):


        sql_query = '''SELECT d5 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 5'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        record = '''SELECT quest FROM Mother WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 5""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 5""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 5""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 5""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-5-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-5-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-5-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-5-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)

    elif (update.message.text == "🔵روزششم🔵"):



        sql_query = '''SELECT d6 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 6'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Mother WHERE day = 6 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 6""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 6""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 6""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 6""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-6-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-6-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-6-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-6-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)


    elif (update.message.text == "🔵روزهفتم🔵"):



        sql_query = '''SELECT d7 from Mother_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Mother where day = 7'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Mother WHERE day = 7 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Mother WHERE day = 7""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Mother WHERE day = 7""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Mother WHERE day = 7""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Mother WHERE day = 7""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-7-Mother")],
            [InlineKeyboardButton(Choice2, callback_data="2-7-Mother")],
            [InlineKeyboardButton(Choice3, callback_data="3-7-Mother")],
            [InlineKeyboardButton(Choice4, callback_data="4-7-Mother")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            wive_quest(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            wive_quest(update,context)

    elif (update.message.text == "🔵منواصلی🔵"):
        wives_section(update,context)

    elif (update.message.text == "🔴پایان🔴"):
        battery(update,context)

    ###############################################


    elif (update.message.text == "🟢روزاول🟢"):

        sql_query = '''SELECT d1 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 1'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        record = '''SELECT quest FROM Father WHERE day = 1 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        mamad = c.fetchone()[0]
        conn.commit()
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 1""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 1""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 1""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 1""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-1-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-1-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-1-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-1-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video="https://video-17.dalfak.com/31/31227-577761959812_360.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)

    elif (update.message.text == "🟢روزدوم🟢"):

        
        sql_query = '''SELECT d2 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 2'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Father WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 2""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 2""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 2""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 2""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-2-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-2-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-2-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-2-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)

    elif (update.message.text == "🟢روزسوم🟢"):


        sql_query = '''SELECT d3 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 3'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        
        record = '''SELECT quest FROM Father WHERE day = 3 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 3""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 3""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 3""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 3""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-3-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-3-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-3-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-3-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)
    
    elif (update.message.text == "🟢روزچهارم🟢"):


        sql_query = '''SELECT d4 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 4'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))


        record = '''SELECT quest FROM Father WHERE day = 4 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 4""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 4""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 4""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 4""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-4-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-4-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-4-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-4-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)


    elif (update.message.text == "🟢روزپنجم🟢"):



        sql_query = '''SELECT d5 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 5'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Father WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 5""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 5""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 5""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 5""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-5-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-5-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-5-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-5-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)


    elif (update.message.text == "🟢روزششم🟢"):


        sql_query = '''SELECT d6 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 6'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Father WHERE day = 6 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 6""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 6""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 6""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 6""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-6-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-6-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-6-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-6-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)


    elif (update.message.text == "🟢روزهفتم🟢"):


        sql_query = '''SELECT d7 from Father_Members where chat_id = ?'''

        data = (str(update.message.chat_id))
        c.execute(sql_query, (data,))

        conn.commit()
        mamads = c.fetchone()[0]
        print(mamads)
        print(type(mamads))

        link_query = '''SELECT link from Father where day = 7'''
        c.execute(link_query)
        conn.commit()
        linked = c.fetchone()[0]
        print(linked)
        print(type(linked))

        record = '''SELECT quest FROM Father WHERE day = 7 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Father WHERE day = 7""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Father WHERE day = 7""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Father WHERE day = 7""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Father WHERE day = 7""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-7-Father")],
            [InlineKeyboardButton(Choice2, callback_data="2-7-Father")],
            [InlineKeyboardButton(Choice3, callback_data="3-7-Father")],
            [InlineKeyboardButton(Choice4, callback_data="4-7-Father")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        if(mamads =="0"):

            context.bot.send_video(chat_id=update.message.chat_id,video=linked,timeout=10000,caption=mamad,reply_markup=reply_markup)
            father_section(update,context)
        elif(mamads == "1"):
            context.bot.send_message(chat_id= update.message.chat_id,text="شما به این سوال پاسخ داده اید و مجاز به انتخاب دوباره نیستید")
            father_section(update,context)
    
    if (update.message.text == "🟢منواصلی🟢"):
        father_section(update,context)



    if (update.message.text == "🟣روزاول🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 1 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        mamad = c.fetchone()[0]
        conn.commit()
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 1""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 1""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 1""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 1""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-1-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-1-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-1-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-1-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)

    if (update.message.text == "🟣روزدوم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 2""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 2""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 2""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 2""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-2-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-2-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-2-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-2-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)

    if (update.message.text == "🟣روزسوم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 3 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 3""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 3""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 3""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 3""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-3-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-3-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-3-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-3-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)
    
    if (update.message.text == "🟣روزچهارم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 4 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 4""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 4""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 4""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 4""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-4-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-4-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-4-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-4-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)


    if (update.message.text == "🟣روزپنجم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 5""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 5""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 5""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 5""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-5-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-5-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-5-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-5-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)


    if (update.message.text == "🟣روزششم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 6 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 6""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 6""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 6""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 6""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-6-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-6-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-6-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-6-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        boy_section(update,context)


    if (update.message.text == "🟣روزهفتم🟣"):

        record = '''SELECT quest FROM Boy WHERE day = 7 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Boy WHERE day = 7""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Boy WHERE day = 7""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Boy WHERE day = 7""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Boy WHERE day = 7""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-7-Boy")],
            [InlineKeyboardButton(Choice2, callback_data="2-7-Boy")],
            [InlineKeyboardButton(Choice3, callback_data="3-7-Boy")],
            [InlineKeyboardButton(Choice4, callback_data="4-7-Boy")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)

        boy_section(update,context)

    if (update.message.text == "🟣منواصلی🟣"):
        boy_section(update,context)    


    if (update.message.text == "🟠روزاول🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 1 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        mamad = c.fetchone()[0]
        conn.commit()
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 1""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 1""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 1""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 1""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-1-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-1-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-1-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-1-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
    
        girl_section(update,context)
    if (update.message.text == "🟠روزدوم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 2""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 2""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 2""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 2""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-2-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-2-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-2-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-2-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)

    if (update.message.text == "🟠روزسوم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 3 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 3""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 3""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 3""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 3""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-3-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-3-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-3-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-3-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)

    if (update.message.text == "🟠روزچهارم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 4 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 4""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 4""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 4""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 4""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-4-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-4-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-4-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-4-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)


    if (update.message.text == "🟠روزپنجم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 2 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 5""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 5""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 5""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 5""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-5-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-5-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-5-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-5-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)


    if (update.message.text == "🟠روزششم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 6 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 6""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 6""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 6""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 6""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-6-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-6-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-6-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-6-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)


    if (update.message.text == "🟠روزهفتم🟠"):

        record = '''SELECT quest FROM Girl WHERE day = 7 '''
        c.execute(record)
        # c.execute('''SELECT quest FROM commanders_quest WHERE day = 1 ''')
        conn.commit()
        mamad = c.fetchone()[0]
        # context.bot.send_message(chat_id= update.message.chat_id,text=listToString(c.fetchone()))
        Choice_1 = """SELECT choice1 FROM Girl WHERE day = 7""" 
        c.execute(Choice_1)
        Choice1 = c.fetchone()[0]
        print(Choice1)
        print(type(Choice1))
        
        Choice_2 = """SELECT choice2 FROM Girl WHERE day = 7""" 
        c.execute(Choice_2)
        Choice2 = c.fetchone()[0]
        print(Choice2)
        print(type(Choice2))
        
        Choice_3 = """SELECT choice3 FROM Girl WHERE day = 7""" 
        
        c.execute(Choice_3)
        Choice3 = c.fetchone()[0]
        print(Choice3)
        print(type(Choice3))
        
        Choice_4 = """SELECT choice4 FROM Girl WHERE day = 7""" 

        c.execute(Choice_4)
        Choice4 = c.fetchone()[0]
        print(Choice4)
        print(type(Choice4))
        keyboard = [
            [InlineKeyboardButton(Choice1, callback_data="1-7-Girl")],
            [InlineKeyboardButton(Choice2, callback_data="2-7-Girl")],
            [InlineKeyboardButton(Choice3, callback_data="3-7-Girl")],
            [InlineKeyboardButton(Choice4, callback_data="4-7-Girl")]] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id,video="https://hw7.cdn.asset.aparat.com/aparat-video/184b0b346c2303101a873cb1949eb79225716678-240p.mp4",timeout=10000,caption=mamad,reply_markup=reply_markup)
        girl_section(update,context)
        
    if (update.message.text == "🟠منواصلی🟠"):
        sons_section(update,context)

    if (update.message.text == "🟣پسران🟣"):
        boy_section(update,context)
    if (update.message.text == "🟠دختران🟠"):
        girl_section(update,context)
    if (update.message.text == "🟡بازگشت🟡"):
        battery(update,context)
    if (update.message.text == "🟦بازگشت🟦"):
        wives_section(update,context)
    if (update.message.text == "🟩بازگشت🟩"):
        father_section(update,context) 
    if (update.message.text == "🟪بازگشت🟪"):
        boy_section(update,context)
    if (update.message.text == "🟧بازگشت🟧"):
        girl_section(update,context)
    if (update.message.text == "🟥بازگشت🟥"):
        battery(update,context) 
    if (update.message.text == "❌بازگشت❌"):
        battery(update,context) 


def qa(update,context):
    text = """
    لطفا پرسش خود را در قالب یک پیام وارد کنید
    """

    custom_keyboard = [["❌بازگشت❌"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,text=text,reply_markup=reply_markup)

    message = """
    کاربر {} با شناسه کاربری {} پیام زیر را ارسال کرده است
    \n
    {}
    """.format(update.message.from_user.first_name,update.message.from_user.username,update.message.text)
    final = "%s\n%s"%(text,message)
    # context.bot.send_message(chat_id=update.message.chat_id,text=final)
    context.bot.send_message(chat_id="729561981",text=final) 
    return MAIN

def contact(update,context):

    text = """
    لطفا انتقاد و پیشنهاد خود را در قالب یک پیام وارد کنید
    """

    custom_keyboard = [["🟥بازگشت🟥"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,text=text,reply_markup=reply_markup)

    message = """
    کاربر {} با شناسه کاربری {} پیام زیر را ارسال کرده است
    \n
    {}
    """.format(update.message.from_user.first_name,update.message.from_user.username,update.message.text)
    final = "%s\n%s"%(text,message)
    # context.bot.send_message(chat_id=update.message.chat_id,text=final)
    context.bot.send_message(chat_id="1382509264",text=final) 
    
    return MAIN
def wives_section(update,context):

    custom_keyboard = [["🔵ثبت نام🔵"],
                       ["🔵سوالات🔵"],
                       ["🔵بازگشت🔵"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    # update.message.reply_text("",reply_markup=reply_markup)
    context.bot.send_message(chat_id = update.message.chat_id,text = "🔈لطفا یک گزینه را انتخاب کنید🔈",reply_markup=reply_markup)
    update.message.text
    return MAIN


    

def wive_quest(update,context):


    command = '''SELECT EXISTS(SELECT 1 FROM Mother_Members WHERE chat_id = ? LIMIT 1)'''
    datas = (str(update.message.chat_id))
    c.execute(command, (datas,))

    # c.execute(record)
    conn.commit()
    mamads = c.fetchone()[0]
    print(mamads)
    print(type(mamads))

    if(mamads == 1):
            
        get_day_from_api()

        custom_keyboard = []

        c.execute('''SELECT id FROM day''')
        day = []
        x = c.fetchall()
        print(len(x))
        i=1

        c.execute('''SELECT name FROM day''')
        back = "🔵منواصلی🔵"
        day.insert(len(day),back)
        
        for i in range(len(x)):
            day.append("🔵روز{}🔵".format(str(c.fetchone()[0])))
            
            custom_keyboard = [s.split(' ', 1) for s in day]

        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        get_mother_quest_from_api()
        context.bot.send_message(chat_id = update.message.chat_id, text=".",reply_markup=reply_markup)

    if (mamads == 0):
        
        text = """
        ⛔️شما در این گروه از مسابقه ثبت نام نکرده اید ⛔️
        لطفا ابتدا ثبت نام کنید
        \n
        """
        custom_keyboard = [["🔵منواصلی🔵"]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        update.message.reply_text(text,reply_markup=reply_markup)


    return MAIN


def wive_register(update,context):


    custom_keyboard = [["🟦بازگشت🟦"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,text=".",reply_markup=reply_markup)

    user = update.message.from_user
    chat_id = user['id']
    username = user['username']
    fname = user['first_name']
    lname = user['last_name']

    c.execute('''INSERT into Mother_Members(chat_id,username,fname,lname) values("{}","{}","{}","{}");'''.format(chat_id,username,fname,lname))
    c.execute('''DELETE FROM Mother_Members WHERE rowid NOT IN (SELECT min(rowid) FROM Mother_members GROUP BY chat_id)''')
    conn.commit()

    return MAIN

def father_section(update,context):
    custom_keyboard = [["🟢ثبت نام🟢"],
                       ["🟢سوالات🟢"],
                       ["🟢بازگشت🟢"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id = update.message.chat_id,text = "🔈لطفا یک گزینه را انتخاب کنید🔈",reply_markup=reply_markup)
    
    return MAIN



def father_quest(update,context):
    

    command = '''SELECT EXISTS(SELECT 1 FROM Father_Members WHERE chat_id = ? LIMIT 1)'''
    datas = (str(update.message.chat_id))
    c.execute(command, (datas,))

    # c.execute(record)
    conn.commit()
    mamads = c.fetchone()[0]
    print(mamads)
    print(type(mamads))

    if(mamads == 1):

        get_day_from_api()
        custom_keyboard = []
        # custom_keyboard= [["روز اول"],["روز دوم"]]   
        c.execute('''SELECT id FROM day''')
        day = []
        x = c.fetchall()
        print(len(x))
        i=1
        # get_day_from_api()
        c.execute('''SELECT name FROM day''')
        
        back = "🟢منواصلی🟢"
        day.insert(len(day),back)
        for i in range(len(x)):
            day.append("🟢روز{}🟢".format(str(c.fetchone()[0])))
            # day.append(listToString(c.fetchone()))
            custom_keyboard = [s.split(' ', 1) for s in day]
        #     # custom_keyboard= [['روز اول'],['روز دوم']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        get_father_quest_from_api()
        update.message.reply_text(".",reply_markup=reply_markup)

    if (mamads == 0):
        text = """
        ⛔️شما در این گروه از مسابقه ثبت نام نکرده اید ⛔️
        لطفا ابتدا ثبت نام کنید
        \n
        """
        custom_keyboard = [["🟢منواصلی🟢"]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        update.message.reply_text(text,reply_markup=reply_markup)


    return MAIN


def father_register(update,context):

    

    custom_keyboard = [["🟩بازگشت🟩"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    context.bot.send_message(chat_id=update.message.chat_id,text=".",reply_markup=reply_markup)


    # context.bot.send_message(chat_id=update.message.chat_id, text="لطفا شماره موبایل خود را وارد کنید", reply_markup=ForceReply(selective=True))
    print(update.message.text)
    mobile = update.message.text
    user = update.message.from_user
    print(user)
    chat_id = user['id']
    username = user['username']
    fname = user['first_name']
    lname = user['last_name']
    c.execute('''INSERT into Father_Members(chat_id,username,fname,lname,mobile) values("{}","{}","{}","{}","{}");'''.format(chat_id,username,fname,lname,mobile))
    c.execute('''DELETE FROM Father_Members WHERE rowid NOT IN (SELECT min(rowid) FROM Father_Members GROUP BY chat_id)''')
    conn.commit()

    return MAIN

def boy_section(update,context):
    custom_keyboard = [["🟣ثبت نام🟣"],
                       ["🟣سوالات🟣"],
                       ["🟣بازگشت🟣"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text("🔈لطفا یک گزینه را انتخاب کنید🔈",reply_markup=reply_markup)

    return MAIN

def boy_quest(update,context):

    command = '''SELECT EXISTS(SELECT 1 FROM Boy_Members WHERE chat_id = ? LIMIT 1)'''
    datas = (str(update.message.chat_id))
    c.execute(command, (datas,))

    # c.execute(record)
    conn.commit()
    mamads = c.fetchone()[0]
    print(mamads)
    print(type(mamads))

    if (mamads == 1):
        get_day_from_api()
        custom_keyboard = []
        # custom_keyboard= [["روز اول"],["روز دوم"]]   
        c.execute('''SELECT id FROM day''')
        day = []
        x = c.fetchall()
        print(len(x))
        i=1
        # get_day_from_api()
        c.execute('''SELECT name FROM day''')
        back = "🟣منواصلی🟣"
        day.insert(len(day),back)
        for i in range(len(x)):
            day.append("🟣روز{}🟣".format(str(c.fetchone()[0])))
            # day.append(listToString(c.fetchone()))
            custom_keyboard = [s.split(' ', 1) for s in day]
        #     # custom_keyboard= [['روز اول'],['روز دوم']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        get_boy_quest_from_api()
        update.message.reply_text(".",reply_markup=reply_markup)
    if (mamads == 0):
        text = """
        ⛔️شما در این گروه از مسابقه ثبت نام نکرده اید ⛔️
        لطفا ابتدا ثبت نام کنید
        \n
        """
        custom_keyboard = [["🟣منواصلی🟣"]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        update.message.reply_text(text,reply_markup=reply_markup)

    return MAIN

def boy_register(update,context):


    custom_keyboard = [["🟪بازگشت🟪"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,text=".",reply_markup=reply_markup)

    print(update.message.text)
    mobile = update.message.text
    user = update.message.from_user
    print(user)
    chat_id = user['id']
    username = user['username']
    fname = user['first_name']
    lname = user['last_name']
    c.execute('''INSERT into Boy_Members(chat_id,username,fname,lname,mobile) values("{}","{}","{}","{}","{}");'''.format(chat_id,username,fname,lname,mobile))
    c.execute('''DELETE FROM Boy_Members WHERE rowid NOT IN (SELECT min(rowid) FROM Boy_Members GROUP BY chat_id)''')
    conn.commit()
    
    if (update.message.text == "🔴بازگشت🔴"):
        return BOYS




def girl_section(update,context):
    custom_keyboard = [["🟠ثبت نام🟠"],
                       ["🟠سوالات🟠"],
                       ["🟠بازگشت🟠"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text("🔈لطفا یک گزینه را انتخاب کنید🔈",reply_markup=reply_markup)
    
    return MAIN

    # SELECT EXISTS(SELECT * FROM Girl_Members WHERE chat_id =8888  LIMIT 1)
    #  %s""" % ','.join(str(i))
def girl_quest(update,context):

    command = '''SELECT EXISTS(SELECT 1 FROM Girl_Members WHERE chat_id = ? LIMIT 1)'''
    datas = (str(update.message.chat_id))
    c.execute(command, (datas,))

    # c.execute(record)
    conn.commit()
    mamads = c.fetchone()[0]
    print(mamads)
    print(type(mamads))
    # conn.commit()
    if (mamads == 1):
        get_day_from_api()
        custom_keyboard = []
        # custom_keyboard= [["روز اول"],["روز دوم"]]   
        c.execute('''SELECT id FROM day''')
        day = []
        x = c.fetchall()
        print(len(x))
        i=1
        # get_day_from_api()
        c.execute('''SELECT name FROM day''')
        back = "🟠منواصلی🟠"
        day.insert(len(day),back)
        for i in range(len(x)):
            day.append("🟠روز{}🟠".format(str(c.fetchone()[0])))
            # day.append(listToString(c.fetchone()))
            custom_keyboard = [s.split(' ', 1) for s in day]
        #     # custom_keyboard= [['روز اول'],['روز دوم']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        get_girl_quest_from_api()
        update.message.reply_text(".",reply_markup=reply_markup)
        # return MAIN
    if (mamads == 0):
        text = """
        ⛔️شما در این گروه از مسابقه ثبت نام نکرده اید ⛔️
        لطفا ابتدا ثبت نام کنید
        \n
        """
        custom_keyboard = [["🟠منواصلی🟠"]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        update.message.reply_text(text,reply_markup=reply_markup)

    return MAIN
def girl_register(update,context):
    
    custom_keyboard = [["🟧بازگشت🟧"]]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,text=".",reply_markup=reply_markup)

    print(update.message.text)
    mobile = update.message.text
    user = update.message.from_user
    print(user)
    chat_id = user['id']
    username = user['username']
    fname = user['first_name']
    lname = user['last_name']
    c.execute('''INSERT into Girl_Members(chat_id,username,fname,lname,mobile) values("{}","{}","{}","{}","{}");'''.format(chat_id,username,fname,lname,mobile))
    c.execute('''DELETE FROM Girl_Members WHERE rowid NOT IN (SELECT min(rowid) FROM Girl_Members GROUP BY chat_id)''')
    conn.commit()


def sons_section(update,context):
    custom_keyboard = [["🟣پسران🟣"],
                       ["🟠دختران🟠"],
                       ["🟡بازگشت🟡"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text("🔈لطفا یک گزینه را انتخاب کنید🔈",reply_markup=reply_markup)
    
    return MAIN



def cancel(update,context):
    pass

def button(update,context):
    query = update.callback_query
    print(query.data)
    data = query.data

    ###############################################################
    #  Question day 1 Mother                                      #
    ###############################################################

    if (data == "1-1-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 1 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()


            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-1-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 1 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-1-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            
        else:
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
    if(data == "4-1-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 1"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Mother_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())



    ###############################################################
    #  Question day 2 Mother                                      #
    ###############################################################

    if (data == "1-2-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 2 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            sleep(2)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-2-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-2-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            sleep(2)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if(data == "4-2-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 2"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 3 Mother                                      #
    ###############################################################

    if (data == "1-3-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 3 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "2-3-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-3-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if(data == "4-3-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 3"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:

            sql_query = '''UPDATE Mother_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 4 Mother                                      #
    ###############################################################
    if (data == "1-4-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 4 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "2-4-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 4 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-4-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 4"""
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-4-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 4"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 5 Mother                                      #
    ###############################################################

    if (data == "1-5-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 5 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "2-5-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-5-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-5-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 5"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()

            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 6 Mother                                      #
    ###############################################################

    if (data == "1-6-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 6 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-6-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-6-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-6-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 6"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 7 Mother                                      #
    ###############################################################


    if (data == "1-7-Mother"):

        Answer_1 = """SELECT answer FROM Mother WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Mother WHERE day = 7 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-7-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Mother WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-7-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Mother WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-7-Mother"):
        Answer_1 = """SELECT answer FROM Mother WHERE day = 7"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Mother WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Mother_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Mother_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Mother_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################

    ###############################################################
    #  Question day 1 Father                                      #
    ###############################################################

    if (data == "1-1-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 1 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

        else:
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-1-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 1 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-1-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-1-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 1"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d1 = ? WHERE chat_id = ?'''
            d1="1"
            data = (d1,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 2 Father                                      #
    ###############################################################

    if (data == "1-2-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 2 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "2-2-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-2-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-2-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 2"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d2 = ? WHERE chat_id = ?'''
            d2="1"
            data = (d2,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    ###############################################################
    #  Question day 3 Father                                      #
    ###############################################################

    if (data == "1-3-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 3 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-3-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    if (data == "3-3-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-3-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 3"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d3 = ? WHERE chat_id = ?'''
            d3="1"
            data = (d3,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    ###############################################################
    #  Question day 4 Father                                      #
    ###############################################################
    
    if (data == "1-4-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 4 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-4-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 4 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-4-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-4-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 4"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d4 = ? WHERE chat_id = ?'''
            d4="1"
            data = (d4,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    ###############################################################
    #  Question day 5 Father                                      #
    ###############################################################

    if (data == "1-5-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 5 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()

            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-5-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-5-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-5-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 5"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d5 = ? WHERE chat_id = ?'''
            d5="1"
            data = (d5,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    ###############################################################
    #  Question day 6 Father                                      #
    ###############################################################

    if (data == "1-6-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 6 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()

            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-6-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-6-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-6-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 6"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d6 = ? WHERE chat_id = ?'''
            d6="1"
            data = (d6,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    ###############################################################
    #  Question day 7 Father                                      #
    ###############################################################


    if (data == "1-7-Father"):

        Answer_1 = """SELECT answer FROM Father WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Father WHERE day = 7 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()

            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()


            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-7-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Father WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-7-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Father WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-7-Father"):
        Answer_1 = """SELECT answer FROM Father WHERE day = 7"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Father WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Father_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Father_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            sql_query = '''UPDATE Father_Members SET d7 = ? WHERE chat_id = ?'''
            d7="1"
            data = (d7,query.message.chat_id)
            c.execute(sql_query,data)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################

    ###############################################################
    #  Question day 1 Boy                                      #
    ###############################################################

    if (data == "1-1-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 1 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-1-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 1 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-1-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-1-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 1"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


    ###############################################################
    #  Question day 2 Boy                                      #
    ###############################################################

    if (data == "1-2-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 2 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-2-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-2-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-2-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


    ###############################################################
    #  Question day 3 Boy                                      #
    ###############################################################

    if (data == "1-3-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 3 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-3-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-3-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-3-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())



    ###############################################################
    #  Question day 4 Boy                                      #
    ###############################################################

    if (data == "1-4-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 4 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-4-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 4 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-4-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-4-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 4"""
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


    ###############################################################
    #  Question day 5 Boy                                      #
    ###############################################################

    if (data == "1-5-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 5 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-5-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-5-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-5-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())




    ###############################################################
    #  Question day 6 Boy                                      #
    ###############################################################

    if (data == "1-6-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 6 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-6-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-6-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-6-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


    ###############################################################
    #  Question day 7 Boy                                         #
    ###############################################################


    if (data == "1-7-Boy"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Boy WHERE day = 7 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-7-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-7-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Boy WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-7-Boy"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Boy WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Boy_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Boy_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################

    ###############################################################
    #  Question day 1 Girl                                         #
    ###############################################################

    if (data == "1-1-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 1 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-1-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 1 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-1-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 1 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-1-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 1 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 1 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)

    ###############################################################
    #  Question day 2 Girl                                         #
    ###############################################################


    if (data == "1-2-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 2 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-2-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-2-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 2 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-2-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 2 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 2 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)


    ###############################################################
    #  Question day 3 Girl                                         #
    ###############################################################


    if (data == "1-3-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 3 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-3-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-3-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 3 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-3-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 3 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 3 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)



    ###############################################################
    #  Question day 4 Girl                                         #
    ###############################################################

    if (data == "1-4-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 4 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-4-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 4 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-4-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 4 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-4-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 4 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 4 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    


    ###############################################################
    #  Question day 5 Girl                                         #
    ###############################################################

    if (data == "1-5-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 5 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-5-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-5-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 5 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-5-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 5 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 5 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())




    ###############################################################
    #  Question day 6 Girl                                         #
    ###############################################################

    if (data == "1-6-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 6 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "2-6-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-6-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 6 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-6-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 6 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 6 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())



    ###############################################################
    #  Question day 7 Girl                                         #
    ###############################################################


    if (data == "1-7-Girl"):

        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "الف"):
            
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            Score_1 = """SELECT score FROM Girl WHERE day = 7 """ 
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            # print(m)
            query.answer()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)                
  
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)

    if (data == "2-7-Girl"):
        Answer_1 = """SELECT answer FROM Boy WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ب"):
            Score_1 = """SELECT score FROM Boy WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print(score)
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ' '.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if (data == "3-7-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 7 """ 
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "ج"):
            Score_1 = """SELECT score FROM Girl WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            conn.commit()
            print("quest score is  = {} ".format(score))
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            print("my score is {} ".format(my))
            conn.commit()
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            print("its query answer {}".format(query.answer()) )
            # query.edit_message_text(text="hi")
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید - امتیاز سوال برای شما منظور شد', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # context.bot.answer_callback_query(callback_query_id=query.id, text='you chose cat', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
    if(data == "4-7-Girl"):
        Answer_1 = """SELECT answer FROM Girl WHERE day = 7 """
        c.execute(Answer_1)
        answer = c.fetchone()[0]
        conn.commit()
        print("the answer for this quest is {}".format(answer))

        if (answer ==  "د"):
            Score_1 = """SELECT score FROM Girl WHERE day = 7 """
            c.execute(Score_1)
            score = c.fetchone()[0]
            print("quest score is  = {} ".format(score))
            conn.commit()
            My_Score = """SELECT score FROM Girl_Members WHERE chat_id = %s """ % ''.join(str(query.message.chat_id))
            c.execute(My_Score)
            my = c.fetchone()[0]
            conn.commit()
            print("my score is {} ".format(my))
            
            total_score = int(score) + int(my)
            print("total score is {} ".format(total_score))
            command = '''UPDATE Girl_Members SET score = ?  WHERE chat_id = ?'''
            
            datas = (total_score, query.message.chat_id)
            c.execute(command, datas)
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب کرده اید --- امتیاز سوال برای شما منظور شد', show_alert=True)
            # context.bot.editMessageReplyMarkup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=ReplyKeyboardRemove())
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        else:
            context.bot.answer_callback_query(callback_query_id=query.id, text='شما گزینه درست را انتخاب نکرده اید', show_alert=True)
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
            # query.edit_message_reply_markup(chat_id= query.message.chat_id, message_id= query.message.message_id,reply_markup=ReplyKeyboardRemove())


def main():
    updater = Updater("1357728588:AAGE0AdG08zTFxJ_0ZhfPWQB4r4bFwZWL7U")


    conv_handler = ConversationHandler(

        entry_points = [CommandHandler('start',start)],
        states = {
            MAIN: [MessageHandler(Filters.all,low)],
            QA : [MessageHandler(Filters.all,qa)],
            CONTACT : [MessageHandler(Filters.all,contact)],
            WIVES:  [MessageHandler(Filters.all,wives_section)],
            WIVE_QUEST : [MessageHandler(Filters.all,wive_quest)],
            WIVE_REG : [MessageHandler(Filters.all,wive_register)],
            FATHER: [MessageHandler(Filters.all,father_section)],
            FATHER_QUEST : [MessageHandler(Filters.all,father_quest)],
            FATHER_REG : [MessageHandler(Filters.all,father_register)],
            BOYS:   [MessageHandler(Filters.all,boy_section)],
            BOY_QUEST : [MessageHandler(Filters.all,boy_quest)],
            BOY_REG : [MessageHandler(Filters.all,boy_register)],            
            GIRLS:  [MessageHandler(Filters.all,girl_section)],
            GIRL_QUEST : [MessageHandler(Filters.all,girl_quest)],
            GIRL_REG :  [MessageHandler(Filters.all,girl_register)],
            SONS:  [MessageHandler(Filters.all,sons_section)],

            
            
            
        },
        
        fallbacks=[CommandHandler('cancel',cancel)])



    updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('start',start))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()



context.bot.remove_webhook()
time.sleep(0.1)
context.bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
