# # if message.chat.type == "private":
# # 	# private chat message
# #
# # if message.chat.type == "group":
# # 	# group chat message
# #
# # if message.chat.type == "supergroup":
# # 	# supergroup chat message
# #
# # if message.chat.type == "channel":
# # 	# channel message
#
#
# import os
# import telebot
# from telebot import types
# import time
# import requests
# from tinydb import TinyDB, Query
# import logging
#
# import database
#
# db = TinyDB('db.json')
#
# # logger = telebot.logger
# # telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
#
# image = 'https://res.cloudinary.com/afmdjango/image/upload/v1609893859/gurdjvtxmdnupiyf4rfm.webp'
# # document = 'https://res.cloudinary.com/afmdjango/image/upload/v1587142438/nhajgc6z5o3l5tavy0la.pdf'
#
# API_KEY = os.getenv('API_KEY')
#
# bot = telebot.TeleBot('1957271668:AAHfqUHXUN4qH8sGrRNc0jcT0MrznZ_UkLU')
#
#
# # command to respond to a greeting using the command word /greet
# @bot.message_handler(commands=['greet'])
# def greet(message):
#     bot.reply_to(message, 'Hi how is it going?')
#
#
# # command to respond to a greeting using the command word /hello
# @bot.message_handler(commands=['hello'])
# def hello(message):
#     bot.send_message(message.chat.id, 'Hi how is it going 👋?')
#
#
# # command to send file using the command word /file
# @bot.message_handler(commands=['file'])
# def file(message):
#     bot.send_document(message.chat.id, image, caption="Thanks, that's the file you requested for")
#
#
# # Handler filters all categories that a user could send in a chat
# @bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'text', 'location',
#                                                                'contact', 'sticker'])
# def message_path(message):
#     global_result = []
#
#     if message.text is not None and message.text.lower() == '/start' or message.text.lower() in ['hello', 'hi',
#                                                                                                  'hey', 'good morning',
#                                                                                                  'good afternoon',
#                                                                                                  'good evening', '👋']:
#         # Introduction message when one start with a greeting
#         intro_message = f"Hello *{message.from_user.first_name}* 👋, Welcome!\
#                         \nLet's get started, what can I help you with today?\
#                         \n[1]. Book request\
#                         \n[2]. Book Feedback\
#                         \n[3]. Contact us"
#
#         # set up markup for keyboard
#         markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
#         book_request_btn = types.KeyboardButton('Book request')
#         book_feedback_btn = types.KeyboardButton('Book Feedback')
#         contact_btn = types.KeyboardButton('Contact')
#         markup.add(book_request_btn, book_feedback_btn, contact_btn)
#
#         # send message, pop up the custom keyboard (Book request and Book Feedback)
#         bot.send_message(message.chat.id, intro_message, parse_mode="Markdown", reply_markup=markup)
#
#     #
#     if "book request" in message.text.lower() or message.text.lower() == '1':
#         # set up markup for keyboard
#         markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
#         book_request_btn = types.KeyboardButton('search by Book title')
#         book_feedback_btn = types.KeyboardButton('search by Book author')
#         markup.add(book_request_btn, book_feedback_btn)
#
#         # send message, pop up the custom keyboard (search by Book title OR search by Book author)
#         bot.send_message(message.chat.id, "Alright, you can choose to search by Book title "
#                                           "or Authors name, which are you going for?", reply_markup=markup)
#
#     # from Book request branch
#     if 'book title' in message.text.lower():
#         markup = types.ForceReply(selective=False)
#         bot.send_message(message.chat.id, "Please enter the title of the book you're trying to get! 🙂"
#                                           "\n *PLEASE USE THE BELOW FORMAT* 👇 \
#                                            \n \
#                                            \n \
#                                            \n *Title: book title* (e.g. Title: God's General) \
#                                            \n \
#                                            \n`Make sure to put the word 'Title:' with the colon first`.",
#                          parse_mode="Markdown", reply_markup=markup)
#
#     result = []
#     if "title:" in message.text.lower():
#         bot.send_message(message.chat.id, "Searching the dataBase for Matches...")
#
#         book_title_ = message.text.lower().split()
#         book_title_.pop(0)
#         book_title__ = book_title_
#         book_title = ""
#         for word in book_title__:
#             book_title = book_title + word
#             book_title = book_title + " "
#
#         book_title = book_title.strip()
#
#         response = requests.get(f"http://127.0.0.1:8000/api/book/?title={book_title}")
#
#         #
#         # result = []
#         data = response.json()['queryset']
#         if not data:
#             bot.send_message(message.chat.id, f"I'm sorry, I could'nt find any book in my database that marches your "
#                                               f"search '{book_title.capitalize()}'!")
#         else:
#             # title: God's general
#
#             for index, item in enumerate(data):
#                 result_dict = {'user_id': f"{message.from_user.id}", 'rank': index + 1,
#                                'id': item['id'], 'title': item['title'], 'author': item['author'], 'file': item['file']}
#                 result.append(result_dict)
#             message_text = ""
#
#             # global_result = result
#
#             for item in result:
#                 line = f"\n{item['rank']}.   {item['title']} by {item['author']}"
#                 message_text = message_text + line
#
#             print(message_text)
#
#             if len(result) > 1:
#
#                 markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
#                                                    input_field_placeholder="Trying Placeholder")
#                 _1 = types.KeyboardButton('1')
#                 _2 = types.KeyboardButton('2')
#                 _3 = types.KeyboardButton('3')
#                 _4 = types.KeyboardButton('4')
#                 _5 = types.KeyboardButton('5')
#                 _6 = types.KeyboardButton('6')
#                 _7 = types.KeyboardButton('7')
#                 _8 = types.KeyboardButton('8')
#                 _9 = types.KeyboardButton('9')
#
#                 markup.add(_1, _2, _3, _4, _5, _6, _7, _8, _9)
#
#                 bot.send_message(message.chat.id, "*Which of this do you said you want?* \n"
#                                                   f"{message_text}",
#                                  parse_mode="Markdown", reply_markup=markup)
#             elif len(result) == 1:
#
#                 markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
#                                                    input_field_placeholder="Trying Placeholder")
#                 db.insert({'user_id': f"{message.from_user.id}", 'file_id': result[0]['id'], 'file': result[0]['file'],
#                            'status': 'pending'})
#
#                 _yes = types.KeyboardButton('Yes, exactly 😊')
#                 _no = types.KeyboardButton('No, not this 😌')
#                 markup.add(_yes, _no)
#                 msg = bot.send_message(message.chat.id, "*Do you mean this?* \n"
#                                                         f"{message_text}",
#                                        parse_mode="Markdown", reply_markup=markup)
#                 bot.register_next_step_handler(msg, download_file)
#             print("line 156", result)
#
#
# def download_file(message):
#     try:
#
#         pass
#     except Exception as e:
#         bot.reply_to(message, "Oops something went wrong!")
#
#     if message.text is not None and 'yes, exactly' in message.text.lower():
#         User = Query()
#         db_search = db.search(User.user_id == message.from_user.id)
#
#         print("db_search: ", db_search)
#         # download and send document
#         bot.send_message(message.chat.id, "Downloading...")
#         # print(result)
#         bot.send_document(message.chat.id, data=result[0]['file'],
#                           caption=f"{result[0]['title']} by {result[0]['author']}")
#
#     #
#     #
#     #
#     # get response and do SEARCH LOOKUP, and return list of possible marches with their ID
#     #
#     #
#     #
#
#     if "book feedback" in message.text.lower() or message.text.lower() == '2':
#         # set up markup for keyboard
#         markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True,
#                                            input_field_placeholder="book title, feedback")
#         bot.send_message(message.chat.id, "wow!, please write your feedback in this format: \n*book title, feedback*",
#                          parse_mode="Markdown", reply_markup=markup)
#
#     # else:
#     #     bot.send_message(message.chat.id,
#     #                      "Sorry i could not process what you request for, let try again.")
#
#
# #     while True:  # Don't end the main thread.
# #         bot.send_message(message.chat.id, "What's the author name?_")
# #         if 'Roberts ' in message.text:
# #             bot.send_document(message.chat.id, document, caption="Thanks, that's the file you requested for")
# #
# #         pass
# #
# bot.enable_save_next_step_handlers(delay=1)
#
# bot.load_next_step_handlers()
#
# while True:
#     try:
#         bot.polling()
#     except Exception as e:
#         time.sleep(5)
#
#         # response = requests.get("http://127.0.0.1:8000/api/download/?id=8")
#         # file_ = response.json()['queryset'][0]['file']
#         # file_title = response.json()['queryset'][0]['title']
#         #
#         # print(file_)
#         # print(file_title)
#         # # test_file = 'http://res.cloudinary.com/pycodet/image/upload/Purpose_Driven_Life.pdf'
#         #
#         # bot.send_message(message.chat.id, "Request is processing...")
#         # bot.send_document(message.chat.id, file_, caption=file_title)
#
#
