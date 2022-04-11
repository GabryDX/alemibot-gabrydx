import asyncio
import secrets
import random
import html
import os
import io
import re

import inspirobot
from PIL import Image, ImageEnhance, ImageOps

from typing import List

from pyrogram import filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from bot import alemiBot

from util import batchify
from util.permission import is_allowed, is_superuser
from util.message import ProgressChatAction, edit_or_reply, is_me, send_media
from util.text import order_suffix
from util.getters import get_text
from util.command import filterCommand
from util.decorators import report_error, set_offline, cancel_chat_action
from util.help import HelpCategory

import logging
logger = logging.getLogger(__name__)

HELP = HelpCategory("QUOTE")
INTERRUPT = False


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand("quote", list(alemiBot.prefixes)))
@report_error(logger)
@set_offline
@cancel_chat_action
async def quote_cmd(client, message):
	"""send stupid quote image

	Code comes from https://github.com/SamHDev/inspiro.
	"""
	msg = message
	reply_to = message.message_id
	if message.reply_to_message is not None:
		msg = message.reply_to_message

	quote = inspirobot.generate()  # Generate Image
	# print(quote.url)  # Print the url
	try:
		await send_media(client, message.chat.id, quote.url,
						 reply_to_message_id=reply_to)
	except Exception as ex:
		await edit_or_reply(message, "`[!] → ` " + str(ex))
