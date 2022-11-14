import inspirobot
import requests

from alemibot import alemiBot

from alemibot.util import (
	filterCommand, get_user, is_me, edit_or_reply, send_media,
	sudo, is_allowed, report_error, set_offline, cancel_chat_action, HelpCategory
)

import logging

from .BrainyQuoteApi import get_random_quote, get_random_quote_author

logger = logging.getLogger(__name__)

HELP = HelpCategory("QUOTE")
INTERRUPT = False


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand(["brainyquote"], options={
	"topic": ["-t", "-topic"], "author": ["-a", "-author"]
}))
@report_error(logger)
@set_offline
@cancel_chat_action
async def brainyquote_cmd(client, message):
	"""send quote message either random or chosen
	between a category or an author

	quotes come from https://www.brainyquote.com/.
	"""
	msg = message
	reply_to = message.id
	if message.reply_to_message is not None:
		msg = message.reply_to_message

	topic = message.command["topics"]
	author = message.command["author"]

	if topic:
		quote = get_random_quote(topic)
	elif author:
		quote = get_random_quote_author(author)
	else:
		quote = get_random_quote()

	quote_list = quote.split("\n")
	quote_text = "\n".join(quote_list[:-1])
	quote_aut = quote_list[-1]
	quote = quote_text.strip() + "\n\n__" + quote_aut + "__"

	if quote:
		await edit_or_reply(msg, quote)
	else:
		await edit_or_reply(message, "`[!] → ` Something went wrong! Try Again!")


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand("quote"))
@report_error(logger)
@set_offline
@cancel_chat_action
async def quote_cmd(client, message):
	"""send random quote message

	Code comes from https://geekflare.com/random-quote-python-code/ and
	quotes come from https://quote-garden.herokuapp.com/api/v3/quotes/random.
	"""
	msg = message
	reply_to = message.id
	if message.reply_to_message is not None:
		msg = message.reply_to_message
	try:
		# making the get request
		response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
		if response.status_code == 200:
			# extracting the core data
			json_data = response.json()
			data = json_data['data']

			# getting the quote from the data
			quote = data[0]['quoteText']
			if "quoteAuthor" in data[0]:
				quote += "\n\n__" + data[0]["quoteAuthor"] + "__"
			await edit_or_reply(msg, quote)
		else:
			await edit_or_reply(message, "`[!] → ` Error while getting quote")
	except:
		await edit_or_reply(message, "`[!] → ` Something went wrong! Try Again!")


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand("quote_img"))
@report_error(logger)
@set_offline
@cancel_chat_action
async def quote_img_cmd(client, message):
	"""send stupid quote image

	Code comes from https://github.com/SamHDev/inspiro.
	"""
	msg = message
	reply_to = message.id
	if message.reply_to_message is not None:
		msg = message.reply_to_message

	quote = inspirobot.generate()  # Generate Image
	# print(quote.url)  # Print the url
	try:
		await send_media(client, message.chat.id, quote.url, reply_to_message_id=reply_to)
	except Exception as ex:
		await edit_or_reply(message, "`[!] → ` " + str(ex))
