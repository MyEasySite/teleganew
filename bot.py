import telebot
import random
from config import API_TOKEN
from telebot import types
import os

def numf(message):
	num = str(random.randint(0, 100))
	bot.send_message(message.chat.id, num)
	if num == "100":
		bot.send_message(message.chat.id, "ПОВЕЗЛО ПОВЕЗЛО")
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECWnZgslCRG3X2fdSIfbOfVHPrukgFGgACpQ4AAoFdmEnFRfv59ibsoB8E')

def text_doc(message):
	i = 0
	while i < 5:
		i += 1
		filename = "doc\\%.d.txt" % i
		with open(filename, 'r', encoding='utf-8') as f:
			bot.send_message(message.chat.id,f.read())



bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎲 Рандомное число до 100")
	item2 = types.KeyboardButton("😊 Как дела?")
	item3 = types.KeyboardButton("🏞 Картинка")
	item4 = types.KeyboardButton("Моя история")

	markup.add(item1, item2, item3, item4)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🎲 Рандомное число до 100':
			# bot.send_message(message.chat.id, 'Если ты сможешь выбить "100", тебя ждет прикалдес')
			bot.send_message(message.chat.id, numf(message))

		elif message.text == '🏞 Картинка':
			all_files_in_directory = os.listdir('images')
			file = random.choice(all_files_in_directory)
			doc = open('images' + '/' + file, 'rb')
			bot.send_photo(message.chat.id, doc)

		# elif message.text == 'Моя история':
		# 	all_files_in_directory = os.listdir('doc')
		# 	file = random.choice(all_files_in_directory)
		# 	doc = open('doc' + '/' + file, 'r')
		# 	bot.send_message(message.chat.id, doc)
		# 	doc.close()

		elif message.text == 'Моя история':
			bot.send_message(message.chat.id, text_doc(message))


		elif message.text == '😊 Как дела?':
			markup = types.InlineKeyboardMarkup()
			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
			item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
			markup.add(item1, item2)
			bot.send_message(message.chat.id, 'Я живой еще, а ты как сам?', reply_markup=markup)

		else:
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECWnJgsk9xwHK3o7Fflw0O8V50uULlVAACAQsAAiFckEk_AZ94Qh9ych8E')
			bot.send_message(message.chat.id, 'Что ты несешь?')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="По матеше 3+ получил?", parse_mode='Markdown')
				bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAECWnBgsk65pKQ2M4zCBik5KC4GydXqbgACuw0AAhE6mEmvdVVTiLtfPx8E')
				bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
			elif call.data == 'bad':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ДО не будет!", parse_mode='Markdown')
				bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAECWm5gskyWSUbkyHVwcPhRsih3kq1_fAACQg4AAoz-kEncyg3pquNyTx8E')

			# show alert
			# bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
			# 	text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop=True)