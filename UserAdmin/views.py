from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Company.models import Company
# Create your views here.
def index(request):
    return render(request, 'UserAdmin/index.html')

def company(request):
    if request.method == "GET":
        companies = Company.objects.all()
        count = 30
        paginator = Paginator(companies, 30) 
        page_number = request.GET.get('page')
    
        try:
            page = paginator.get_page(page_number)
            try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
            except: count = (30 * (int(1) if page_number  else 1) ) - 30
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page = paginator.page(1)
            count = (30 * (int(1) if page_number  else 1) ) - 30
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page = paginator.page(paginator.num_pages)
            count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30
        
        print(page)
        context = {
            'companies' : page
        }
        return render(request, 'UserAdmin/company.html', context=context)