from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None
import csv

#Read a csv file from a given path
def readCSV(filepath):
    
    result = []
    
    with open(filepath,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            result.append({'username':row[0],'birthdate':row[1],'gender':row[2],'voted':row[3]})
            
    return result
    