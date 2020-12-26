import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from census.models import Census
from store.models import Vote

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
        num_censed = Census.objects.filter(voting_id=vid).count()
        num_voted = Vote.objects.filter(voting_id=vid).count()
       
        #Percent of censed people who voted
        percent_voted = int(num_voted*100/num_censed)
        #Percent of censed people who not voted
        percent_not_voted = 100 - percent_voted
        
        context['num_censed']=num_censed
        context['num_voted'] = num_voted
        context['percent_voted']=[percent_voted,percent_not_voted]
        
        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
