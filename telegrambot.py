import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode
import pysynth as ps
import ast


mybot = telebot.TeleBot("5644935913:AAE4YBHxDDH0cIW7RaPByTJbNjTUfnFwiNg")


@mybot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    mybot.reply_to(message, f"سلام {name}، خوش اومدی.برای آشنایی با ربات روی /help کلیک کن")



mymarkup = telebot.types.ReplyKeyboardMarkup(row_width=1 ,  resize_keyboard=True )
btn1 = telebot.types.KeyboardButton('New Game')
btn2 = telebot.types.KeyboardButton('New Command')

SONG = ()
NOTE = ''
STRETCH = ''

mymarkup.add(btn1,btn2)


@mybot.message_handler(commands=['game'])
def game(message):
    mybot.reply_to(message, 'یک عدد حدس بزن بین 0 و 50')
    mybot.register_next_step_handler(message, game_play)


bot_num = random.randint(0, 50)


def game_play(message):
    if int(message.text) == bot_num:
        mybot.send_message(message.chat.id, 'درست حدس زدی! برنده شدی:)')
        mybot.number = random.randint(0, 20)
        mes = mybot.send_message(message.chat.id, 'برای یازی مجدد New Game رو بزن', reply_markup=mymarkup)
        mybot.register_next_step_handler(mes, game)
        mybot.register_next_step_handler(mes, show)

    elif int(message.text) > bot_num:
        mybot.send_message(message.chat.id, 'بیا پایین ')
        mybot.register_next_step_handler(message, game_play)

    elif int(message.text) < bot_num:
        mybot.send_message(message.chat.id, 'برو بالا')
        mybot.register_next_step_handler(message, game_play)



@mybot.message_handler(commands=['age'])
def Birthday(message):
    a = {}
    mybot.reply_to(message, 'تاریخ تولد را وارد کن:\n مثلا: 1401/1/1')
    mybot.register_next_step_handler(message, age)


def age(message):
    b = message.text.split('/')
    print(b)
    print(JalaliDatetime.now())
    age = JalaliDatetime.now() - JalaliDatetime(int(b[0]), int(b[1]), int(b[2]))

    mybot.send_message(message.chat.id, f'این شخص {age}  است')


@mybot.message_handler(['voice'])
def voice(message):
    mybot.reply_to(message, 'یک جمله انگیلیسی برام بفرست')
    mybot.register_next_step_handler(message, converttxtvc)


def converttxtvc(message):
    language = 'en'
    myobj = gTTS(text=message.text, lang=language, slow=False)
    myobj.save("voice.mp3")
    voice = open('voice.mp3', 'rb')
    mybot.send_voice(message.chat.id, voice)

@mybot.message_handler(['max'])
def input_nums(message):
    mybot.reply_to(message, 'لیست اعداد رو وارد کن\nمثلا: 1,2,3,4')
    mybot.register_next_step_handler(message, max_finder)


def max_finder(message):
    mynumberes = message.text.split(',')
    list = []
    for i in mynumberes:
        list.append(int(i))
    mybot.send_message(message.chat.id, f'بیشترین مقدار {max(list)} است')

@mybot.message_handler(['argmax'])
def input_nums(message):
    mybot.reply_to(message, 'لیست اعداد رو وارد کن\nمثلا: 1,2,3,4')
    mybot.register_next_step_handler(message, argmax_finder)


def argmax_finder(message):
    mynumberes = message.text.split(',')
    list = []
    for i in mynumberes:
        list.append(int(i))
    mybot.send_message(message.chat.id, f' اندیس بیشترین مقدار {list.index(max(list))} است')
    


@mybot.message_handler(['qrcode'])
def inputsen(message):
    mybot.reply_to(message, 'یک جمله برام بنویس')
    mybot.register_next_step_handler(message, makeqrcode)

def makeqrcode(message):
    img = qrcode.make(message.text)
    img.save('qrcode.png')
    image = open('qrcode.png', 'rb')
    mybot.send_photo(message.chat.id, image)


def add_note():
    global SONG
    global NOTE
    global STRETCH
    if NOTE == 'Do':
        NOTE = 'c'
    elif NOTE == 'Re':
        NOTE = 'd'
    elif NOTE == 'Mi':
        NOTE = 'e'
    elif NOTE == 'Fa':
        NOTE = 'f'
    elif NOTE == 'Sol':
        NOTE = 'g'
    elif NOTE == 'La':
        NOTE = 'a'
    else:
        NOTE = 'b'
    if STRETCH == 'Whole':
        STRETCH = 1
    elif STRETCH == 'Half':
        STRETCH = 2
    elif STRETCH == 'Quarter':
        STRETCH = 4
    elif STRETCH == 'Eighth':
        STRETCH = 8
    else:
        STRETCH = 16
    SONG += ((NOTE, STRETCH),)
    NOTE = ''
    STRETCH = ''


def set_note(name):
    global NOTE
    NOTE = name


def set_stretch(stroke):
    global STRETCH
    STRETCH = stroke


def empty_song():
    global SONG
    SONG = ()

@mybot.message_handler(commands=['song'])
def song_func(m):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    btn1 = telebot.types.KeyboardButton('شروع')
    markup.add(btn1)
    m = mybot.send_message(m.chat.id, 'شروع کنید. در آخر دکمه اتمام رو بزنید.', reply_markup=markup)
    mybot.register_next_step_handler(m, so1)


def so1(m):
    if not m.text.startswith('/'):
        if m.text != 'شروع':
            set_stretch(m.text)
        if STRETCH != '' and NOTE != '':
            add_note()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=4)
        btn1 = telebot.types.KeyboardButton('Do')
        btn2 = telebot.types.KeyboardButton('Re')
        btn3 = telebot.types.KeyboardButton('Mi')
        btn4 = telebot.types.KeyboardButton('Fa')
        btn5 = telebot.types.KeyboardButton('Sol')
        btn6 = telebot.types.KeyboardButton('La')
        btn7 = telebot.types.KeyboardButton('Si')
        btn8 = telebot.types.KeyboardButton('اتمام')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        msg = mybot.send_message(m.chat.id, 'note:', reply_markup=markup)
        mybot.register_next_step_handler(msg, so2)
    else:
        mybot.reply_to(m, 'لطفا نت مورد نظر را وارد کنید',
                     reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
        mybot.send_message(m.chat.id, 'منتظر پیغام شما هستم')


def so2(m):
    if not m.text.startswith('/'):
        if not m.text == 'اتمام':
            set_note(m.text)
            markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
            btn1 = telebot.types.KeyboardButton('Whole')
            btn2 = telebot.types.KeyboardButton('Half')
            btn3 = telebot.types.KeyboardButton('Quarter')
            btn4 = telebot.types.KeyboardButton('Eighth')
            btn5 = telebot.types.KeyboardButton('Sixteenth')
            markup.add(btn1, btn2, btn3, btn4, btn5)
            msg = mybot.send_message(m.chat.id, 'stretch:', reply_markup=markup)
            mybot.register_next_step_handler(msg, so1)
        else:
            try:
                if len(SONG) >= 1:
                    mybot.send_message(m.chat.id, 'آهنگ شما',
                                     reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
                    ps.make_wav(SONG, fn="song.wav")
                    empty_song()
                    song = open('song.wav', 'rb')
                    mybot.send_voice(m.chat.id, song)
                else:
                    mybot.send_message(m.chat.id, 'دوباره انجامش بدیم؟',
                                     reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
            except:
                mybot.send_message(m.chat.id, 'خطایی در برنامه وجود دارد',
                                 reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
    else:
        mybot.reply_to(m, 'لطفا نت مورد نظر رو وارد کنید',
                     reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
        mybot.send_message(m.chat.id, 'منتظر پیغام شما هستم')








@mybot.message_handler(commands= ['help'])
def show(message):
    mybot.reply_to(message, 'لطفا انتخاب کنید:\n/game بازی اعداد\n/age محاسبه سن.\n/voice تبدیل جمله به صوت\n/max پیدا کردن بیشترین مقدار در لیست اعداد\n/argmax پیدا کردن اندیس بیشترین مقدار در لیست اعداد\n/qrcode تبدیل جمله به QR code\n/song ساخت آهنگ')


mybot.polling()