# -*- coding: utf-8 -*-
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
    context.bot.sendMessage(
        update.message.chat_id, text='¡Hola! si no sabes cómo funciona el bot, prueba a mandarme /help')


def help(update, context):
    context.bot.sendMessage(update.message.chat_id, text='Los comandos disponibles son: /start (saludo), /help (ayuda, muestra los comandos disponibles), /voting *votingID* (muestra el resultado de la votación que se le pida. IMPORTANTE la votación debe estar con el tally para que el bot la reconozca. Ej: /voting 1), /error (muestra la traza del error en caso de que hubiese alguno)')


# method for the custom command - gets a voting by its ID and puts it into a text
def getVoting(votingId):
    objeto_voting = Voting.objects.get(id=votingId)
    something = objeto_voting.postproc
    listed_values = []
    for s in something:
        values_list = []
        for v in s.values():
            values_list.append(v)
        listed_values.append(values_list)
    options_number = len(listed_values)
    unmensaje = "Estos son los resultados de la votacion %s:\n" % votingId
    i = 0
    while i < options_number:
        unmensaje = unmensaje + "-->Opcion %d: (%s) -- Votos obtenidos: (%s)\n\n" % (
            i, listed_values[i][2], listed_values[i][3])
        i = i+1
    return unmensaje


# custom command
def voting(update, context):
    votingId = update.message.text.replace('/voting ', '')
    context.bot.sendMessage(update.message.chat_id, text=getVoting(votingId))


def error(update, context, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    # dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    dp = DjangoTelegramBot.getDispatcher(
        '1478165863:AAGTc2kVAoGTI1-pZck4ZvkNYho2ldB_NX8')  # get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # custom command
    dp.add_handler(CommandHandler("voting", voting))

    # log all errors
    dp.add_error_handler(error)
