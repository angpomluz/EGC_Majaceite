import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

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
import json
import xml.etree.ElementTree as XT

from visualizer.utils import render_to_pdf


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
        elif request.GET["Formato"]=="pdf":
            listed_values=[]
            for d in Vote.postproc:
                Values=[]
                for v in d.values():
                    Values.append(v)
                listed_values.append(Values)
            context = {
            "voting_id": request.GET["VotID"],
            "voting_name": Vote.name,
            "voting_question": Vote.question,
            "data": listed_values,
            }
            pdf = render_to_pdf('visualizer/invoice.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            return response
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

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            context['VotId'] = vid
        except:
            raise Http404

        return context
