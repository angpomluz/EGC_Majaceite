from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
from django.views.generic import TemplateView
from django.conf import settings
from base import mods
import visualizer.views
from voting.models import *

BOT_USER_ACCESS_TOKEN= 'xoxb-1541218143492-1535266194915-UQI55HlBMyrnGYwriL4VThn6'
VERIFICATION_TOKEN='yi1ydbfn1xMrjJ1YAVH7MVUz'

@csrf_exempt
def event_hook(request):
    client = slack.WebClient(BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))
    
    if json_dict['token'] != VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    
    if 'event' in json_dict:
        event_msg = json_dict['event']
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)
    
    if event_msg['text'] == '-saludame':
        user = event_msg['user']
        channel = event_msg['channel']
        response_msg = ":wave:, Hello <@%s>" % event_msg['text']
        client.chat_postMessage(channel=channel, text=response_msg)
        return HttpResponse(status=200)

    if event_msg['text'] == '-help':
        user = event_msg['user']
        channel = event_msg['channel']
        response_msg = """Hola <@%s>, estos son los comandos disponibles:\n -help \n -saludame \n -res_vX (donde X es el id de la votacion) \n
                            Todos los comando deben incluir el guion para que el bot lo entienda como comando""" % user
        client.chat_postMessage(channel=channel, text=response_msg)
        return HttpResponse(status=200)
   
    if "-res_v" in event_msg['text']:
        channel = event_msg['channel']
        voting_id = event_msg['text'][6:]
        objeto_voting=Voting.objects.get(id=voting_id)
        something = objeto_voting.postproc
        listed_values=[]
        for s in something:
            values_list=[]
            for v in s.values():
                values_list.append(v)
            listed_values.append(values_list)
        options_number = len(listed_values)
        unmensaje = "Estos son los resultados de la votacion %s:\n" % voting_id
        i=0
        while i < options_number:
            unmensaje = unmensaje + "-->Opcion %d: (%s) -- Votos obtenidos: (%s)\n\n" % (i, listed_values[i][2], listed_values[i][3])
            i = i+1
        response_msg = unmensaje
        client.chat_postMessage(channel=channel, text=response_msg)
        return HttpResponse(status=200)
    return HttpResponse(status=200)
