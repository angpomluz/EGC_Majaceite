import json
import datetime
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from census.models import Census
from store.models import Vote
from .utils import readCSV

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
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
        
        #Loading the context with data and returning it back
        context['num_censed']=num_censed
        context['num_voted'] = num_voted
        context['percent_voted']=[percent_voted,percent_not_voted]
        context['votes_by_age']=list(votes_by_age.values())
        context['gender_votes']=gender_votes
        
        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
    
# Receives a range of ages and a list of birthdates and returns a list containing
# the number of people in each age range
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

def calculate_age(born, is_string=False):
    
    if is_string:
         born = datetime.datetime.strptime(born, "%d/%m/%Y").date()
        
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
