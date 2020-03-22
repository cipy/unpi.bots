#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import telegram
from telegram.ext import Updater, CommandHandler
from secrets import TELEGRAM_ROBOT_TOKEN

import operator
import logging
import random
import atexit
import time

from functools import wraps

now = time.localtime()
# run only during weekdays
# if now.tm_wday > 4: exit()


@atexit.register
def goodbye():
    print("")
    print("@exit logic: Saving state...")
    # TODO: saving state here if required
    print("@exit login: Done.")

def errorAction(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(bot, update, **kwargs)

    return command_func

@send_typing_action
def helloAction(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

@send_typing_action
def salutAction(bot, update):
    update.message.reply_text(
        'Salut {}'.format(update.message.from_user.first_name))

@send_typing_action
def helpAction(bot, update):
    update.message.reply_text('Hello {}, I understand the following commands:\n{}'.format(
        update.message.from_user.first_name,
        '\n'.join([
        "/hello - Greetings!",
        "/help - this (help) text",
        "Please note: this RO.bot is used only in Romanian by https://www.unpi.ro/english!" ]) ))

@send_typing_action
def menuAction(bot, update, args): pass


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(TELEGRAM_ROBOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('hello', helloAction))
updater.dispatcher.add_handler(CommandHandler('salut', salutAction))
updater.dispatcher.add_handler(CommandHandler('menu', menuAction, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('help', helpAction))

updater.dispatcher.add_error_handler(errorAction)
updater.start_polling()
updater.idle()
