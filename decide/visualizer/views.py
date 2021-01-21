import json
import datetime
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from census.models import Census
from store.models import Vote
from .utils import readCSV

from base import mods
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from voting.models import *
from django.template import Template,Context,loader
from django.template.loader import get_template
import csv
import xml.etree.ElementTree as XT

# from visualizer.utils import render_to_pdf


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'
    # EndPoint to download results
    def downloadResults(request):
        #options={"Unreal Engine":5,"Unity":2,"Wave Engine":1}
        Vote=Voting.objects.get(pk=(request.GET["VotID"]))
        if not Vote.start_date:
            raise Http404
        elif not Vote.end_date:
            raise Http404
        elif not Vote.tally:
            raise Http404
        elif request.GET["Formato"]=="csv":
            listed_values=[]
            for d in Vote.postproc:
                Values=[]
                for v in d.values():
                    Values.append(v)
                listed_values.append(Values)
            response=HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            writer.writerow(['Votes','Number','Option','postproc'])
            for value in listed_values:
                writer.writerow(value)
            response['Content-Disposition']= 'attachment; filename="votingResults.csv"'
            return response
        # elif request.GET["Formato"]=="pdf":
        #     listed_values=[]
        #     for d in Vote.postproc:
        #         Values=[]
        #         for v in d.values():
        #             Values.append(v)
        #         listed_values.append(Values)
        #     context = {
        #     "voting_id": request.GET["VotID"],
        #     "voting_name": Vote.name,
        #     "voting_question": Vote.question,
        #     "data": listed_values,
        #     }
        #     pdf = render_to_pdf('visualizer/votingpdf.html', context)
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="votingpdf.pdf"'
        #     return response
        elif request.GET["Formato"]=="json":
            response=JsonResponse({'results':Vote.postproc})
            response['Content-Disposition']= 'attachment; filename="votingResults.json"'
            return response
        elif request.GET["Formato"]=="xml":
            
            data= XT.Element('Results')
            votes=XT.SubElement(data,'votes')
            numbers=XT.SubElement(data,'numbers')
            opts=XT.SubElement(data,'options')
            postprocs=XT.SubElement(data,'postprocs')
            listed_values=[]
            for d in Vote.postproc:
                Values=[]
                for v in d.values():
                    Values.append(v)
                listed_values.append(Values)
            for i in range(0,len(listed_values)):
                v=XT.SubElement(votes,'vote')
                v.set('name','v' + str(i))
                v.text=str(listed_values[i][0])
                n=XT.SubElement(numbers,'number')
                n.set('name','n'+str(i))
                n.text=str(listed_values[i][1])
                o=XT.SubElement(opts,'option')
                o.set('name','o'+str(i))
                o.text=str(listed_values[i][2])
                p=XT.SubElement(postprocs,'postproc')
                p.set('name','p'+str(i))
                p.text=str(listed_values[i][3])

            stringData=XT.tostring(data)
            response=HttpResponse(stringData,content_type='text/xml')
            response['Content-Disposition']= 'attachment; filename="votingResults.xml"'
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
        r = mods.get('voting', params={'id': vid})
        if len(r) > 0:
            voting = json.dumps(r[0])
        else:
            raise Http404 
        
        #num_censed = Census.objects.filter(voting_id=vid).count()
        #num_voted = Vote.objects.filter(voting_id=vid).count()
        
        #Load mock users from csv
        read_users = readCSV('visualizer/resources/EGCusers.csv')
        
        #Calculating num of censed users and num of censed who voted
        censed_users = [u['voted'] for u in read_users]
        num_censed=len(censed_users)
        num_voted=0
        for vote in censed_users:
            if int(vote) == 1:
                num_voted +=1
       
        #Percent of censed people who voted
        percent_voted = int(num_voted*100/num_censed)
        #Percent of censed people who not voted
        percent_not_voted = 100 - percent_voted
        
        #Calculating votes by gender
        genvotes_raw = [voter['gender'] for voter in read_users]
        dict_genvotes_raw={'Male':0,'Female':0,'Non Binary':0}
        for vote in genvotes_raw:
            dict_genvotes_raw[vote] +=1
        
        gender_votes = list(dict_genvotes_raw.values())
        
        
        #Calculating votes by age
        age_range = [18,25,35,55,65]
        birthdates = [user['birthdate'] for user in read_users]
        votes_by_age = get_votes_by_age(age_range,birthdates)
        
        #Calculate votes by work_status
        work_status_raw = [voter['work_status'] for voter in read_users]
        dict_work_status_raw={'Emp':0,'Unemp':0}
        for vote in work_status_raw:
            dict_work_status_raw[vote] +=1
        
        work_status_votes = list(dict_work_status_raw.values())
        
        context['work_status'] = work_status_votes
        
        #Loading the context with data and returning it back
        context['num_censed']=num_censed
        context['num_voted'] = num_voted
        context['percent_voted']=[percent_voted,percent_not_voted]
        context['votes_by_age']=list(votes_by_age.values())
        context['gender_votes']=gender_votes
        
        

        # Aquí hacemos del json un diccionario
        voting_information = json.loads(voting)
        postproc = voting_information["postproc"]

        if postproc:
            # Metemos en data y labels la información necesaria
            a = 0
            labels = []; data = []

            while a < len(postproc):
                option = postproc[a]
                labels.append(option["option"])
                data.append(option["votes"])
                a += 1

            # La añadimos al context
            context['data'] = data
            context['labels'] = labels
            context['voting'] = voting
            context['VotId'] = vid
        else:
            context['notally'] = "Lo sentimos, pero lesta votación no ha sido empezada, o no ha sido finalizada, y/o los resultados no han sido contados. Por favor, asegurese que la votación está finalizada y contada antes de acceder a esta página"

        return context
    
# Receives a range of ages and a list of birthdates and
# 
# Parameters:   age_range   -> The range of ages for clasify the birthdates
#               birthdates  -> List of strings in format mm/dd/yyyy
#
# Returns: a dictionary containing the number of people in each age range
def get_votes_by_age(age_range,birthdates):
    
    ages=[]
    #Mapping date strings to ages
    for bs in birthdates:
        ages.append(calculate_age(bs,True))
 
    #filling up the return list with zeros
    res = dict(zip(age_range,[0]*len(age_range)))
    
    #iteriting the list and clisifiing the values
    for age in ages:
        for ar in reversed(age_range):
            if age >= ar:
                res[ar] += 1
            
    return res

# Calculate de age from a birthdate
# 
# Parameters:   born        -> var containing the birhthdate
#               is_string   -> determine if the born var is string or date type
#
# Returns: The age calculated from the born parameter
def calculate_age(born, is_string=False):
    
    if is_string:
         born = datetime.strptime(born, "%d/%m/%Y").date()
        
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
