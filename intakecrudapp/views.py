from django.shortcuts import render,redirect,HttpResponse
from .forms import WaterIntakeForm
from .models import WaterInke
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Sum
import datetime

# Create your views here.

#CREATE

@login_required(login_url='/loginpage/')

def intake_add(request):
    today = timezone.now().date()
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            if WaterInke.objects.filter(user = request.user , date = today).exists():
                return render(request,'intakecreate.html',{'form':form,'error':"You have already added today's Water Intake Quantity!"})
            else:
                temp = form.save(commit=False)
                temp.user = request.user
                temp.date = today
                form.save()
                return redirect('list')     
    else:
        form = WaterIntakeForm()
    return render(request,'intakecreate.html',{'form':form})

#RETRIEVE

@login_required(login_url='/loginpage/')
def intake_list(request):
    intake = WaterInke.objects.filter(user = request.user)
    paginator = Paginator(intake,1)

    page_number = request.GET.get('page') #on click the page number to get
    page_obj = paginator.get_page(page_number)

    return render(request,'intakeList.html',{'page_obj':page_obj})

#UPDATE

@login_required(login_url='/loginpage/')
def intake_update(request,pk):
    data = WaterInke.objects.get(pk = pk,user = request.user)
    newtime = timezone.localtime().now().time()
    print(newtime)
    if request.POST:
        form = WaterIntakeForm(request.POST,instance=data)
        if form.is_valid():
            inst = form.save(commit=False) 
            inst.time = newtime #Adding new time
            form.save()
            return redirect('list')
        
    else:
        form = WaterIntakeForm(instance=data)
    
    return render(request,'intakeUpdate.html',{'form':form})

#DELETE

@login_required(login_url='/loginpage/')
def intake_delete(request,pk):
    data = WaterInke.objects.get(pk = pk , user = request.user)
    
    if request.method == 'GET':
        data.delete()
        return redirect('list')
    else:
        print(request.user)
        return redirect('list')
    # return render(request,'intakeDelete.html',{'user':request.user})

#DIFFERENCE CALC

@login_required(login_url='/loginpage/')
def calculate_difference(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        return JsonResponse({'error': 'Please select both fields'}, status=400)

    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        water_intake_start = WaterInke.objects.filter(user=request.user, date=start_date).aggregate(total=Sum('quantity'))
        water_intake_end = WaterInke.objects.filter(user=request.user, date=end_date).aggregate(total=Sum('quantity'))

        start_total = water_intake_start['total'] or 0
        end_total = water_intake_end['total'] or 0
        
        difference = end_total - start_total
        
        return JsonResponse({'difference': "{:.2f}".format(difference)})
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

#For rendering the differ.html

@login_required(login_url='/loginpage/')   
def view_calc(request):
    return render(request,'differ.html')
        