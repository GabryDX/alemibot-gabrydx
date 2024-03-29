import os

from alemibot import alemiBot

from PyDictionary import PyDictionary
from udpy import UrbanClient

from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO

from pyrogram.enums import ChatAction, ParseMode

from alemibot.util.command import _Message as Message
from alemibot.util import (
	batchify, tokenize_json, sep, get_user, is_allowed, edit_or_reply, ProgressChatAction, filterCommand,
	report_error, set_offline, cancel_chat_action, HelpCategory
)

import logging
logger = logging.getLogger(__name__)

HELP = HelpCategory("APICALLS-BIS")

recognizer = sr.Recognizer()
dictionary = PyDictionary()
UClient = UrbanClient()

ERROR_MESSAGE = "<code>[!] → </code> "


@HELP.add(sudo=False)
@alemiBot.on_message(is_allowed & filterCommand(["transcribe"], options={
	"lang": ["-l", "-lang"]
}))
@report_error(logger)
@set_offline
@cancel_chat_action
async def transcribe2_cmd(client: alemiBot, message: Message):
	"""transcribes a voice message
	Reply to a voice message to transcribe it. It uses Google Speech Recognition API.
	It will work without a key but usage may get limited. You can try to get a free key here:
	http://www.chromium.org/developers/how-tos/api-keys
	If you have an API key, add it to your config under category [transcribe] in a field named \"key\".
	You can specify speech recognition language with `-l` (using `RFC5646` language tag format :`en-US`, `it-IT`, ...)
	"""
	await client.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
	msg = await edit_or_reply(message, "<code>→ </code> Working...")
	path = None
	lang = message.command["lang"] or get_user(message).language_code or "en-US"
	file_format = (message.reply_to_message.audio and message.reply_to_message.audio.file_name) or \
				  (message.audio and message.audio.file_name)
	if message.reply_to_message and (message.reply_to_message.voice or message.reply_to_message.audio):
		path = await client.download_media(message.reply_to_message)
	elif message.voice or message.audio:
		path = await client.download_media(message)
	else:
		return await edit_or_reply(message, ERROR_MESSAGE + " No audio given")
	if file_format:
		file_format = file_format.split(".")[-1].lower()
		if file_format == "opus":
			try:
				AudioSegment.from_file(path, codec="opus").export("data/voice.wav", format="wav")
			except:
				AudioSegment.from_file(path, codec="webm").export("data/voice.wav", format="wav")
		elif file_format == "mp3":
			AudioSegment.from_mp3(path).export("data/voice.wav", format="wav")
		elif file_format == "flv":
			AudioSegment.from_wav(path).export("data/voice.wav", format="wav")
		elif file_format == "ogg":
			AudioSegment.from_ogg(path).export("data/voice.wav", format="wav")
		elif file_format == "wav":
			AudioSegment.from_wav(path).export("data/voice.wav", format="wav")
	else:
		AudioSegment.from_ogg(path).export("data/voice.wav", format="wav")
	os.remove(path)
	voice = sr.AudioFile("data/voice.wav")
	with voice as source:
		audio = recognizer.record(source)
	out = "<code> → </code>" + recognizer.recognize_google(audio, language=lang,
						key=client.config.get("transcribe", "key", fallback=None))
	await edit_or_reply(msg, out)
