import inspirobot

from alemibot import alemiBot

from alemibot.util import (
	filterCommand, get_user, is_me, edit_or_reply, send_media,
	sudo, is_allowed, report_error, set_offline, cancel_chat_action, HelpCategory
)

import logging
logger = logging.getLogger(__name__)

HELP = HelpCategory("QUOTE")
INTERRUPT = False


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand("quote"))
@report_error(logger)
@set_offline
@cancel_chat_action
async def quote_cmd(client, message):
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
