import os
import telebot
from telebot import types
import time
import datetime
import requests
from tinydb import TinyDB, Query
import random

db = TinyDB('db.json')

# document = 'https://res.cloudinary.com/afmdjango/image/upload/v1587142438/nhajgc6z5o3l5tavy0la.pdf'

API_KEY = os.getenv('API_KEY')

# Register bot with your unique Key (each bot has it own API Key, so if you want to kill a bot and use another,
# you just change the key)
bot = telebot.TeleBot('1957271668:AAHfqUHXUN4qH8sGrRNc0jcT0MrznZ_UkLU')


# command to respond to a greeting using the command word /hello
@bot.message_handler(commands=['feedback'])
def run_feedback_fun(message):
    user_input_feedback(message)


# Greeting Function
def greet():
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:
        return 'Good morning'
    elif 12 <= currentTime.hour < 18:
        return 'Good afternoon'
    else:
        return 'Good evening'


# Handler filters all categories of messages that a user could send in a chat
@bot.message_handler(func=lambda message: True, content_types=['audio', 'video',
                                                               'document', 'text', 'location',
                                                               'contact', 'sticker'])
def message_path(message):
    if message.text is not None and message.text.lower() == '/start' or message.text.lower() in ['hello', 'hi',
                                                                                                 'hey', 'good morning',
                                                                                                 'good afternoon',
                                                                                                 'good evening', '👋']:
        # Introduction message when one start with a greeting or start command

        greet_text = greet()
        welcome_msg_list = [f"Hello, *{greet_text} {message.from_user.first_name}* 👋 and Welcome!\
                        \nLet's get started, what can I help you with today?\
                        \n📬 Book request\
                        \n📃 Book Feedback\
                        \n📞. Contact us",

                            f"Holla! *{greet_text} {message.from_user.first_name}* 👋, It nice to have you here!\
                        \nWhat can I help you with today?\
                        \n📬 Book request\
                        \n📃 Book Feedback\
                        \n📞. Contact us",

                            f"You're Welcome *{message.from_user.first_name}* ❤ and *{greet_text}*,\
                        \nWhat brings you to me 😉, what can I help you with today?\
                        \n📬 Book request\
                        \n📃 Book Feedback\
                        \n📞. Contact us"
                            ]

        # randomly pick a message from list of reply types and assign it as message to be sent to user
        intro_message = random.choice(welcome_msg_list)

        # set up markup for keyboard, this is what forms the custom key of available options that a user has to select
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        book_request_btn = types.KeyboardButton('Book request')
        book_feedback_btn = types.KeyboardButton('Book Feedback')
        contact_btn = types.KeyboardButton('Contact')
        markup.add(book_request_btn, book_feedback_btn, contact_btn)

        # send message, pop up the custom keyboard (Book request and Book Feedback)
        msg = bot.send_message(message.chat.id, intro_message, parse_mode="Markdown", reply_markup=markup)
        bot.register_next_step_handler(msg, bot_ability_option)
    #


def bot_ability_option(message):
    if message.text is not None and "book request" in message.text.lower():
        if "book request" in message.text.lower() or "No, please" in message.text.lower():
            # set up markup for keyboard
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            book_request_btn = types.KeyboardButton('by Book title')
            book_feedback_btn = types.KeyboardButton('by Book author')
            markup.add(book_request_btn, book_feedback_btn)

            # send message, pop up the custom keyboard (search by Book title OR search by Book author)
            reply_list = ["Alright, that is why i'm here! Would you like to search by Book title "
                          "or Authors name?",
                          "Perfect, which method would you like to search by, 'Book title' OR 'Author\'s name'?",
                          "Brilliant!, You can choose to search by 'Book title' OR Book 'Author's name', which one "
                          "are you "
                          "going for?"]
            bot_response = random.choice(reply_list)
            msg = bot.send_message(message.chat.id, bot_response, reply_markup=markup)
            bot.register_next_step_handler(msg, search_by_book_attrib)

        elif "book feedback" in message.text.lower() or "/feedback" in message.text.lower():
            contact_reply = [
                "Thanks for reaching out. \
                \n\nKindly send your feedback to us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite",

                "Lovely..Thanks for reaching out. \
                \n\nKindly send your feedback to us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite"
            ]

            response = random.choice(contact_reply)
            bot.send_message(message.chat.id, response, parse_mode="Markdown")

        elif "contact" in message.text.lower() or "/feedback" in message.text.lower():
            contact_reply = [
                "Thanks for reaching out. \
                \n\nYou can contact us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite",

                "Lovely..Thanks for reaching out. \
                \n\nKindly contact us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite"
            ]
            response = random.choice(contact_reply)
            bot.send_message(message.chat.id, response, parse_mode="Markdown")

        else:
            remove_markup = types.ReplyKeyboardRemove()
            response = "Opps, you're expected to choose either to Request for a Book, Give a Feedback on a " \
                       "book, or to Contact us. /start "
            bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=remove_markup)


def search_by_book_attrib(message):
    if message.text is not None and 'book title' in message.text.lower():
        markup = types.ForceReply(selective=False, input_field_placeholder="Book title. e.g God's general")

        reply_list = ["Please what's the *Title* of the book of the book you're trying to get? 🙂",
                      "Alright, kindly enter the title of the Book! 🙂",
                      "Brilliant!, What's is the Title of the book you're searching for?",
                      "Ok, i can help you with that, but i'll need to know the *Book's title*. 🙂"]

        bot_response = random.choice(reply_list)
        msg = bot.send_message(message.chat.id, bot_response,
                               parse_mode="Markdown", reply_markup=markup)
        bot.register_next_step_handler(msg, user_input_book_title)

    elif message.text is not None and "book author" in message.text.lower():
        markup = types.ForceReply(selective=False, input_field_placeholder="Author's name. e.g Roberts Liardon")

        reply_list = ["Please what's the name of the *Author* of the book you're trying to get? 🙂",
                      "Alright, kindly enter the name of the Author! 🙂",
                      "Brilliant!, What's is the Author's name of the book you're searching for?",
                      "Ok, i can help you with that, but i'll like to know the *Authors name*. 🙂"]
        bot_response_ = random.choice(reply_list)
        msg = bot.send_message(message.chat.id, bot_response_,
                               parse_mode="Markdown", reply_markup=markup)
        bot.register_next_step_handler(msg, user_input_book_author)
    elif message.text is not None and "feedback" in message.text.lower():
        bot.register_next_step_handler(user_input_feedback)
    else:
        bot.register_next_step_handler(search_by_book_attrib)


def user_input_feedback(message):
    try:
        if "title:" in message.text.lower() or message.text.lower() == '/start':
            contact_reply = [
                "Thanks for reaching out. \
                \n\nKindly send your feedback to us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite",

                "Lovely..Thanks for reaching out. \
                \n\nKindly send your feedback to us through any of our endpoint below! \
                \n*Email:* pycodet@gmail.com \
                \n*Telegram:* https://t.me/taiwoadegite"
            ]

            response = random.choice(contact_reply)
            bot.send_message(message.chat.id, response, parse_mode="Markdown")

    except Exception as exc:
        print('Something went wrong in feedback section')
        print(exc)
        bot.reply_to(message, "Oops an EXCEPTION happened!, Let try it "
                              "again. Please click /start")


def user_input_book_title(message):
    try:
        if message.text is not None or "title:" in message.text.lower():
            bot.send_message(message.chat.id, "Searching the dataBase for Matches...")
            print(message.text.lower())

            book_title = message.text.lower()

            response = requests.get(f"https://christianbooks-bot-api.herokuapp.com/api/book/?title={book_title}")

            result = []
            data = response.json()['queryset']
            if not data:
                markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
                book_title_key = types.KeyboardButton('by Book title')
                book_author_key = types.KeyboardButton('by Book Author')
                stop_command_key = types.KeyboardButton('/stop')
                markup.add(book_title_key, book_author_key, stop_command_key)

                msg = bot.send_message(message.chat.id,
                                       f"I'm sorry, I could'nt find any book in my database that marches your "
                                       f"search '{book_title.capitalize()}'!"
                                       f"\nPlease check your input and try again or you search by Author instead.",
                                       reply_markup=markup)

                bot.register_next_step_handler(msg, search_by_book_attrib)
            else:
                for index, item in enumerate(data):
                    result_dict = {'user_id': f"{message.from_user.id}", 'rank': index + 1,
                                   'id': item['id'], 'title': item['title'], 'author': item['author'],
                                   'file': item['file']}
                    result.append(result_dict)

                message_text = ""
                # global_result = result

                print("line 199: ", result)
                for item in result:
                    line = f"\n{item['rank']}.   {item['title']} by {item['author']}"
                    message_text = message_text + line

                if len(result) == 1:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                                       input_field_placeholder="Trying Placeholder")
                    db.insert(
                        {'user_id': f"{message.from_user.id}", 'file_id': result[0]['id'], 'file': result[0]['file'],
                         'file_title': f"{result[0]['title']}", 'file_author': f"{result[0]['author']}",
                         'status': 'pending'})

                    _yes = types.KeyboardButton('Yes, exactly 😊')
                    _no = types.KeyboardButton('No, not this 😌')

                    markup.add(_yes, _no)
                    msg = bot.send_message(message.chat.id, "*Do you mean this?* \n"
                                                            f"{message_text}",
                                           parse_mode="Markdown", reply_markup=markup)
                    bot.register_next_step_handler(msg, download_file_from_single_list)

                elif len(result) > 1:
                    db.insert_multiple(result)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                                       input_field_placeholder="Trying Placeholder")
                    result_length = len(result)

                    _1 = types.KeyboardButton('1')
                    _2 = types.KeyboardButton('2')
                    _3 = types.KeyboardButton('3')
                    _4 = types.KeyboardButton('4')
                    _5 = types.KeyboardButton('5')
                    _6 = types.KeyboardButton('6')
                    _7 = types.KeyboardButton('7')
                    _8 = types.KeyboardButton('8')
                    _9 = types.KeyboardButton('9')
                    _10 = types.KeyboardButton('10')
                    _11 = types.KeyboardButton('11')
                    _12 = types.KeyboardButton('12')
                    _13 = types.KeyboardButton('13')
                    _14 = types.KeyboardButton('14')
                    _15 = types.KeyboardButton('15')
                    _16 = types.KeyboardButton('16')
                    _17 = types.KeyboardButton('17')
                    _18 = types.KeyboardButton('18')
                    _19 = types.KeyboardButton('19')
                    _20 = types.KeyboardButton('20')

                    if result_length <= 5:
                        markup.add(_1, _2, _3, _4, _5)
                    elif result_length <= 20:
                        markup.add(_6, _7, _8, _9, _10)
                    elif result_length <= 20:
                        markup.add(_11, _12, _13, _14, _15, _16, _17, _18, _19, _20)

                    msg = bot.send_message(message.chat.id, "*Which of this do you said you want?* \n"
                                                            f"{message_text}",
                                           parse_mode="Markdown", reply_markup=markup)
                    bot.register_next_step_handler(msg, down_load_file_from_multiple_list)

    except Exception as exc:
        print('Something went wrong in search by title section')
        print(exc)
        bot.reply_to(message, "Oops an EXCEPTION happened!, Let try it "
                              "again. Please click /start")


def user_input_book_author(message):
    try:

        if message.text is not None or "author:" in message.text.lower():
            bot.send_message(message.chat.id, "Searching the dataBase for Matches...")
            book_author = message.text.lower()

            response = requests.get(f"https://christianbooks-bot-api.herokuapp.com/api/book/?author={book_author}")

            result = []
            data = response.json()['queryset']
            print(data)

            if not data:
                markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
                book_title_key = types.KeyboardButton('by Book title')
                book_author_key = types.KeyboardButton('by Book Author')
                stop_command_key = types.KeyboardButton('/stop')
                markup.add(book_title_key, book_author_key, stop_command_key)

                msg = bot.send_message(message.chat.id,
                                       f"I'm sorry, I could'nt find any book in my database that marches your "
                                       f"search '{book_author.capitalize()}'!"
                                       f"\nPlease check your input carefully and try again or you search by Author "
                                       f"instead.",
                                       reply_markup=markup)

                bot.register_next_step_handler(msg, search_by_book_attrib)
            else:
                for index, item in enumerate(data):
                    result_dict = {'user_id': f"{message.from_user.id}", 'rank': index + 1,
                                   'id': item['id'], 'title': item['title'], 'author': item['author'],
                                   'file': item['file']}
                    result.append(result_dict)

                message_text = ""
                # global_result = result

                print("line 155: ", result)
                for item in result:
                    line = f"\n{item['rank']}.   {item['title']} by {item['author']}"
                    message_text = message_text + line

                if len(result) == 1:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                                       input_field_placeholder="Trying Placeholder")
                    db.insert(
                        {'user_id': f"{message.from_user.id}", 'file_id': result[0]['id'], 'file': result[0]['file'],
                         'file_title': f"{result[0]['title']}", 'file_author': f"{result[0]['author']}",
                         'status': 'pending'})

                    _yes = types.KeyboardButton('Yes, exactly 😊')
                    _no = types.KeyboardButton('No, not this 😌')

                    markup.add(_yes, _no)
                    msg = bot.send_message(message.chat.id, "*Do you mean this?* \n"
                                                            f"{message_text}",
                                           parse_mode="Markdown", reply_markup=markup)
                    bot.register_next_step_handler(msg, download_file_from_single_list)

                elif len(result) > 1:
                    db.insert_multiple(result)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                                       input_field_placeholder="Trying Placeholder")

                    _1 = types.KeyboardButton('1')
                    _2 = types.KeyboardButton('2')
                    _3 = types.KeyboardButton('3')
                    _4 = types.KeyboardButton('4')
                    _5 = types.KeyboardButton('5')
                    _6 = types.KeyboardButton('6')
                    _7 = types.KeyboardButton('7')
                    _8 = types.KeyboardButton('8')
                    _9 = types.KeyboardButton('9')

                    markup.add(_1, _2, _3, _4, _5, _6, _7, _8, _9)

                    msg = bot.send_message(message.chat.id, "*Which of this would you like to get?* \n"
                                                            f"{message_text}",
                                           parse_mode="Markdown", reply_markup=markup)
                    bot.register_next_step_handler(msg, down_load_file_from_multiple_list)

    except Exception as exc:
        print('Something went wrong in search by author section')
        bot.reply_to(message, "Oops! an EXCEPTION happened, Let try it"
                              "again. Please click /start")


def down_load_file_from_multiple_list(message):
    try:
        if message.text is not None:
            User = Query()
            query_rank = db.search(User.rank == int(message.text))
            print(query_rank)
            bot.reply_to(message, "Fetching Document...")
            document = query_rank[0]['file']
            caption = f"{query_rank[0]['title']} by {query_rank[0]['author']}"
            bot.send_document(message.chat.id, document, caption=caption)
            db.remove(User.user_id == f'{message.from_user.id}')

            reply_list = [
                "would that be all for now?",
                "Thanks, is that all?",
                "Do have a nice reading. I guess that's all?"
            ]
            response = random.choice(reply_list)

            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            yes_btn = types.KeyboardButton('Yes, Thanks!')
            no_btn = types.KeyboardButton('No, please')

            markup.add(yes_btn, no_btn)
            # Sleep for 2 seconds, then send message, pop up the custom keyboard (Book request and Book Feedback)
            time.sleep(2)
            msg = bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
            bot.register_next_step_handler(msg, end_trend_or_go_back)

        else:
            User = Query()
            db.remove(User.user_id == f'{message.from_user.id}')
    except Exception as e:
        print(e)
        bot.reply_to(message, "Oops something went wrong!, input is not in the list i showed you. If you like to try "
                              "again click /start")


def download_file_from_single_list(message):
    try:
        if message.text is not None and "yes, exactly" in message.text.lower():
            User = Query()

            bot.reply_to(message, "Fetching Document...")
            query_list = db.search(User.user_id == f'{message.from_user.id}')

            document = query_list[0]['file']
            caption = f"{query_list[0]['file_title']} by {query_list[0]['file_author']}"

            bot.send_document(message.chat.id, document, caption=caption)

            reply_list = [
                "would that be all for now?",
                "Thanks, is that all?",
                "Do have a nice reading. I guess that's all?"
            ]
            response = random.choice(reply_list)

            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            yes_btn = types.KeyboardButton('Yes, Thanks!')
            no_btn = types.KeyboardButton('No, please')

            markup.add(yes_btn, no_btn)
            # Sleep for 2 seconds, then send message, pop up the custom keyboard (Book request and Book Feedback)
            time.sleep(2)
            msg = bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)

            # remove record from noSQL database 'db.json'
            db.remove(User.user_id == f'{message.from_user.id}')

            bot.register_next_step_handler(msg, end_trend_or_go_back)

        elif message.text is not None and "no, not this" in message.text.lower():
            User = Query()

            msg = bot.send_message(message.chat.id, "Oops..., sorry about that, Let try again. Please click /start")
            db.remove(User.user_id == f'{message.from_user.id}')
            bot.register_next_step_handler(msg, message_path)

    except Exception as e:
        bot.reply_to(message, "Oops something went wrong!, let try again. Please click /start")


def end_trend_or_go_back(message):
    if message.text is not None:
        if "yes" in message.text.lower():
            last_msg = "\n" \
                       "\nThanks and do have a good day!. 👋" \
                       "\nPlease do well to tell your friends about me."
            bot.send_message(message.chat.id, last_msg)
        elif "no" in message.text.lower():
            msg = bot.send_message(message.chat.id, "redirecting...")

            # Introduction message when one start with a greeting or start command
            welcome_msg_list = ["Alright!\
                                    \nwhat would you have me do for you again 😊? \
                                    \n📬 Book request\
                                    \n📃 Book Feedback\
                                    \n📞. Contact us",

                                f"Ok! \
                                    \nwhat would you have me do for you again? 😉\
                                    \n📬 Book request\
                                    \n📃 Book Feedback\
                                    \n📞. Contact us",

                                f"Sweet! ❤,\
                                    \nwhat would you have me do for you again?\
                                    \n📬 Book request\
                                    \n📃 Book Feedback\
                                    \n📞. Contact us"
                                ]

            # randomly pick a message from list of reply types and assign it as message to be sent to user
            intro_message = random.choice(welcome_msg_list)

            # set up markup for keyboard, this is what forms the custom key of available options that a user has to
            # select
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            book_request_btn = types.KeyboardButton('Book request')
            book_feedback_btn = types.KeyboardButton('Book Feedback')
            contact_btn = types.KeyboardButton('Contact')
            markup.add(book_request_btn, book_feedback_btn, contact_btn)

            # send message, pop up the custom keyboard (Book request and Book Feedback)
            msg = bot.send_message(message.chat.id, intro_message, parse_mode="Markdown", reply_markup=markup)
            bot.register_next_step_handler(msg, bot_ability_option)


bot.enable_save_next_step_handlers(delay=1)

bot.load_next_step_handlers()

while True:
    try:
        bot.polling()
    except Exception as e:
        time.sleep(5)
