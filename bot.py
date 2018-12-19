import telebot
import re
from time import gmtime, strftime
from src.dbmongo import mdb
from src.redis import redis

print(f"init bot")
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
mongo = mdb(os.getenv("MONGODB_HOST"), os.getenv("MONGODB_PORT"), "remembal")
store = redis(os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"))

@bot.message_handler(commands=['start'])
def start(message) -> None:
	message.text = f"Hello. Bot for sending messages in group chats. Usages - /help."
	bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['help'])
def start(message) -> None:
	message.text = f"Available commands - /setmsg, /stopsending"
	bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['eday'])
def download(message) -> None:
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text=f"+1 Hour", callback_data=f"+1_hour"))
	keyboard.add(types.InlineKeyboardButton(text=f"-1 Hour", callback_data=f"-1_hour"))
	keyboard.add(types.InlineKeyboardButton(text=f"+5 Minutes", callback_data=f"+5_minutes"))
	keyboard.add(types.InlineKeyboardButton(text=f"-5 Minutes", callback_data=f"-5_minutes"))
	keyboard.add(types.InlineKeyboardButton(text=f"Done", callback_data=f"done"))
	store.delete_data_in_store(message.from_user.username)
	store.save_data_in_store(message.from_user.username,
				 {'chat_id': message.chat.id,
				  'u_id': message.from_user.id,
				  'text': message.text,
				  'data': strftime("H:%M:", gmtime())})

	bot.send_message(message.chat.id, f"{strftime("%H:%M:", gmtime())}", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call) -> None:
	if call.message:
		if call.data.find("+1_hour") != -1:
			bot.send_message(call.message.chat.id, f"+1 hour")
			set_data_in_store(username, "+1", "hour")
		if call.data.find("-1_hour") != -1:
			bot.send_message(call.message.chat.id, f"-1 hour")
			set_data_in_store(username, "-1", "hour")
		if call.data.find("+5_minutes") != -1:
			bot.send_message(call.message.chat.id, f"+5 minutes")
			set_data_in_store(username, "+5", "minutes")
		if call.data.find("-5_minutes") != -1:
			bot.send_message(call.message.chat.id, f"-5 minutes")
			set_data_in_store(username, "-5", "minutes")
		if call.data.find("done") != -1:
			bot.send_message(call.message.chat.id, f"Done")
			set_data_in_store(username, "0", "done")

def set_data_in_store(username, data, time_type) -> None:
	obj = store.get_full_obj_from_store(username)
	store.delete_data_in_store(username)
	if data.find("done") != -1:
		#save in db
		return
	hours, minutes = edit_time(obj['data'])
	if data.find("+") != -1:
		if time_type.find("hour"):
			hours += 1
		else:
			minutes += 1
	if data.find("-") != -1:
		if time_type.find("hour"):
			hours -= 1
		else:
			minutes -= 1
	if hours >= 24:
		hours -= 24
	if minutes >= 60:
		minutes -= 60
	obj['data'] = f"{hours}:{minutes}"
	store.save_data_in_store(username, obj)

#TODO: rewrite reqexp
def edit_time(str_time) -> int, int:
	hours = re.findall(r'[0-2][0-9]:', str_time)
	minutes = re.findall(r':[0-5][0-9]', str_time)
	return int(hours[:len(hours)-1]), int(minutes[1:])

if __name__ == '__main__':
	try:
		bot.polling(none_stop = True)
	except Exception as e:
		print(f"bot has been falling {e}")
		time.sleep(5)
