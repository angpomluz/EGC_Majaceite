from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

# Render a pdf view from a template and the group of variables that the template needs
# 
# Parameters: template_src -> Path to the html template file
#             context_dict -> Array of variables that the template uses to retrieve data from the voting
# Returns: returns a http response with the pdf in an application format that can be downloaded as it is requested
#          if the pdf render has any error, this method will return None
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

# Read a csv file from a local given path
# 
# Parameters: filepath -> Path to the csv file
# Returns: returns a list of dictionaries, each dictionary represents a row of the csv
# cotaining as pairs key/value the column name and his val
def readCSV(filepath):
    
    result = []
    
    with open(filepath,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            result.append({'username':row[0],'birthdate':row[1],'gender':row[2],'voted':row[3], 'work_status':row[4]})
            
    return result
    