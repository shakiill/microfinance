from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os

from apps.loan.models import LoanApplication, ApplicationProduct, Guarantor, Asset, FinancialRecord, CheckInfo

def download_application_details(request, pk):
    # Fetch the loan application
    application = get_object_or_404(LoanApplication, pk=pk)

    # Fetch related details
    products = ApplicationProduct.objects.filter(loan_application=application)
    guarantors = Guarantor.objects.filter(loan_application=application)
    assets = Asset.objects.filter(loan_application=application)
    financial_records = FinancialRecord.objects.filter(loan_application=application)
    check_info = CheckInfo.objects.filter(loan_application=application)

    # Render HTML template
    html_string = render_to_string('application_download.html', {
        'application': application,
        'products': products,
        'guarantors': guarantors,
        'assets': assets,
        'financial_records': financial_records,
        'check_info': check_info,
    })

    # Create PDF
    html = HTML(string=html_string)
    css = CSS(string='''
        @page {
            margin: 1.5cm;
            @top-center {
                content: "Loan Application Details";
            }
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
            }
        }
        body { 
            font-family: Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.4;
        }
        table { 
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        th, td { 
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .header { 
            text-align: center;
            margin-bottom: 20px;
            font-size: 18pt;
        }
        .section-title { 
            background-color: #f2f2f2;
            padding: 10px;
            font-weight: bold;
            margin-top: 20px;
        }
    ''')

    # Generate PDF
    pdf_bytes = html.write_pdf(stylesheets=[css])

    # Create HTTP response
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="loan_application_{pk}_details.pdf"'

    return response