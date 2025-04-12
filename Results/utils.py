# utils.py
from io import BytesIO
from django.shortcuts import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os

def generate_result_pdf(result):
    template_path = 'results/result_pdf.html'
    context = {'result': result}
    
    template = get_template(template_path)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={result.roll_no}_result.pdf'
    
    pdf_status = pisa.CreatePDF(html, dest=response)
    
    if pdf_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response