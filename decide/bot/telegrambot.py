# -*- coding: utf-8 -*-
# Example code for telegrambot.py module
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from base import mods
import visualizer.views
from voting.models import *

import logging
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    context.bot.sendMessage(update.message.chat_id, text='Hi!')


# method custom command
def getVoting(votingId):
    objeto_voting = Voting.objects.get(id=votingId)
    something = objeto_voting.postproc
    listed_values=[]
    for s in something:
        values_list=[]
        for v in s.values():
            values_list.append(v)
        listed_values.append(values_list)
    options_number = len(listed_values)
    unmensaje = "Estos son los resultados de la votacion %s:\n" % votingId
    i=0
    while i < options_number:
        unmensaje = unmensaje + "-->Opcion %d: (%s) -- Votos obtenidos: (%s)\n\n" % (i, listed_values[i][2], listed_values[i][3])
        i = i+1
    return unmensaje


# custom command
def voting(update, context):
    votingId = update.message.text.replace('/voting ', '')
    context.bot.sendMessage(update.message.chat_id, text=getVoting(votingId))


# def startgroup(update, context):
#     context.bot.sendMessage(update.message.chat_id, text='Hi!')


# def me(update, context):
#     context.bot.sendMessage(update.message.chat_id, text='Your information:\n{}'.format(update.effective_user))


# def chat(update, context):
#     context.bot.sendMessage(update.message.chat_id, text='This chat information:\n {}'.format(update.effective_chat))


# def forwarded(update, context):
#     context.bot.sendMessage(update.message.chat_id, text='This msg forwaded information:\n {}'.format(update.effective_message))


# def help(update, context):
#     context.bot.sendMessage(update.message.chat_id, text='Help!')


# def echo(update, context):
#     update.message.reply_text(update.message.text)


def error(update, context, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    # dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    dp = DjangoTelegramBot.getDispatcher('1478165863:AAGTc2kVAoGTI1-pZck4ZvkNYho2ldB_NX8')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # custom command
    dp.add_handler(CommandHandler("voting", voting))
    # dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("startgroup", startgroup))
    # dp.add_handler(CommandHandler("me", me))
    # dp.add_handler(CommandHandler("chat", chat))
    # dp.add_handler(MessageHandler(Filters.forwarded , forwarded))

    # # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)