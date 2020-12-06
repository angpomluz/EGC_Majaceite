import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
        try:
            r = mods.get('voting', params={'id': vid})
            voting = json.dumps(r[0])

            # Aquí hacemos del json un diccionario
            voting_information = json.loads(voting)
            postproc = voting_information["postproc"]

            # Metemos en data y labels la información necesaria
            a = 0; b = 0
            labels = []; data = []

            while a < len(postproc):
                option = postproc[a]
                labels.append(option["option"])
                a += 1
                
            while b < len(postproc):
                option = postproc[b]
                data.append(option["votes"])
                b += 1

            # La añadimos al context
            context['voting'] = voting
            context['data'] = data
            context['labels'] = labels
        except:
            raise Http404

        return context
